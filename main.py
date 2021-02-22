#!/usr/bin/python3
import os
import re
import semver
from github import Github


def main():
    """ The main method executed. """

    # Github  variables
    github_token = os.environ.get('GITHUB_TOKEN')
    github_repository = os.environ.get('GITHUB_REPOSITORY')
    github_ref = os.environ.get('GITHUB_REF')

    # Input variables
    input_release_branch_pattern = os.environ.get('INPUT_RELEASE_BRANCH_PATTERN', '')
    input_maintenance_branch_pattern = os.environ.get('INPUT_MAINTENANCE_BRANCH_PATTERN', '')
    input_version = os.environ.get('INPUT_VERSION', '')

    # Format input variables
    release_branch_pattern = '^releases/trigger(-(?P<version>[0-9]+[.][0-9]+[.][0-9]+(.*)))?$'
    if input_release_branch_pattern != '':
        release_branch_pattern = input_release_branch_pattern
    maintenance_branch_pattern = '^maintenances/(?P<major>[0-9]+)[.](?P<minor>[0-9]+)[.]x$'
    if input_maintenance_branch_pattern != '':
        maintenance_branch_pattern = input_maintenance_branch_pattern

    # Post-process date-time.
    if not github_ref.startswith('refs/heads/'):
        raise Exception('The process should be triggered from a branch.')

    # Get the release branch name.
    release_source_branch_name = github_ref.removeprefix('refs/heads/')

    # Get the release version
    release_source_branch_name_match = re.match(release_branch_pattern, release_source_branch_name)
    if not release_source_branch_name_match:
        raise Exception(f'Release branch name {release_source_branch_name} does not match the given pattern.')
    if 'version' not in release_source_branch_name_match.groupdict():
        raise Exception('Release branch pattern does not have a version capturing group.')
    if input_version == '' and not release_source_branch_name_match.group('version'):
        raise Exception('Input version not provided and cannot extract it from branch name.')

    release_version = input_version if input_version != '' else release_source_branch_name_match.group('version')

    # Parse release version and get additional info.
    release_semver = semver.VersionInfo.parse(release_version)

    # Get repo.
    github = Github(github_token)
    github_repo = github.get_repo(github_repository)

    # Check if tag already exists or not.
    for github_tag in github_repo.get_tags():
        if github_tag.name.lower() == release_version.lower():
            raise Exception('A tag with this version already exists.')

    # Check if maintenance branch exists.
    release_target_branch_name = github_repo.default_branch
    for github_branch in github_repo.get_branches():
        maintenance_branch_name_match = re.match(maintenance_branch_pattern, github_branch.name)
        if maintenance_branch_name_match:
            if 'major' in maintenance_branch_name_match.groupdict() and str(release_semver.major) != maintenance_branch_name_match.group('major'):
                continue
            if 'minor' in maintenance_branch_name_match.groupdict() and str(release_semver.minor) != maintenance_branch_name_match.group('minor'):
                continue
            release_target_branch_name = github_branch.name

    # Return output variables.
    print(f'::set-output name=version::{release_version}')
    print(f'::set-output name=major_version::{release_semver.major}')
    print(f'::set-output name=minor_version::{release_semver.minor}')
    print(f'::set-output name=patch_version::{release_semver.patch}')
    print(f'::set-output name=prerelease_version::{release_semver.prerelease if release_semver.prerelease else ""}')
    print(f'::set-output name=build_version::{release_semver.build if release_semver.build else ""}')
    print(f'::set-output name=is_prerelease::{"true" if release_semver.prerelease else "false"}')
    print(f'::set-output name=source_branch::{release_source_branch_name}')
    print(f'::set-output name=target_branch::{release_target_branch_name}')


if __name__ == '__main__':
    main()

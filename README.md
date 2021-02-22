![Build](https://github.com/julb/action-prepare-release/workflows/Build/badge.svg)

# GitHub Action to prepare releases

The GitHub Action for preparing releases using a GitOps approach and get variables.

- Extract release version from the branch name
- Block release if a tag with that version already exists.
- Identify if there is a maintenance branch or not linked to that release.
- Output utility vars such as:
  ** Release version,
  ** Major/minor/patch/prerelease/build version,
  ** Source branch name,
  ** Target branch name where release commits should be merged (maintenance branch or default branch).

## Usage

### Example Workflow file

- 1st example: Version is given by release branch and there is a maintenance branch
  ** Release branch is: `releases/trigger-1.0.0`
  ** Maintenance branch is: `maintenances/1.0.x`

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Compute release variables
        id: release_vars
        uses: julb/action-prepare-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Print outputs
        run: |
          echo ${{ steps.release_vars.outputs.version }} # 1.0.0
          echo ${{ steps.release_vars.outputs.major_version }} # 1
          echo ${{ steps.release_vars.outputs.minor_version }} # 0
          echo ${{ steps.release_vars.outputs.patch_version }} # 0
          echo ${{ steps.release_vars.outputs.prerelease_version }}  # ''
          echo ${{ steps.release_vars.outputs.build_version }} # ''
          echo ${{ steps.release_vars.outputs.is_prerelease }} # 'false'
          echo ${{ steps.release_vars.outputs.source_branch }} # 'releases/trigger-1.0.0'
          echo ${{ steps.release_vars.outputs.target_branch }} # maintenances/1.0.x
```

- 2nd example: Version is given by parameter and there is a maintenance branch
  ** Release branch is: `releases/trigger`
  ** Maintenance branch is: `maintenances/1.0.x`

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Compute release variables
        id: release_vars
        uses: julb/action-prepare-release@v1
        with:
          version: 1.0.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Print outputs
        run: |
          echo ${{ steps.release_vars.outputs.version }} # 1.0.0
          echo ${{ steps.release_vars.outputs.major_version }} # 1
          echo ${{ steps.release_vars.outputs.minor_version }} # 0
          echo ${{ steps.release_vars.outputs.patch_version }} # 0
          echo ${{ steps.release_vars.outputs.prerelease_version }}  # ''
          echo ${{ steps.release_vars.outputs.build_version }} # ''
          echo ${{ steps.release_vars.outputs.is_prerelease }} # 'false'
          echo ${{ steps.release_vars.outputs.source_branch }} # 'releases/trigger'
          echo ${{ steps.release_vars.outputs.target_branch }} # maintenances/1.0.x
```

- 3rd example: Version is given by parameter and there is not a maintenance branch
  ** Release branch is: `releases/trigger`
  ** No maintenance branch

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Compute release variables
        id: release_vars
        uses: julb/action-prepare-release@v1
        with:
          version: 1.0.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Print outputs
        run: |
          echo ${{ steps.release_vars.outputs.version }} # 1.0.0
          echo ${{ steps.release_vars.outputs.major_version }} # 1
          echo ${{ steps.release_vars.outputs.minor_version }} # 0
          echo ${{ steps.release_vars.outputs.patch_version }} # 0
          echo ${{ steps.release_vars.outputs.prerelease_version }}  # ''
          echo ${{ steps.release_vars.outputs.build_version }} # ''
          echo ${{ steps.release_vars.outputs.is_prerelease }} # 'false'
          echo ${{ steps.release_vars.outputs.source_branch }} # 'releases/trigger'
          echo ${{ steps.release_vars.outputs.target_branch }} # 'main'
```

### Inputs

| Name                         | Type   | Default                                                          | Description                                                                                                                                                                                                 |
| ---------------------------- | ------ | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `version`                    | string | `Not set`                                                        | Version to release. To specify if version should not be extracted from release branch.                                                                                                                      |
| `release_branch_pattern`     | regexp | `^releases\/trigger(-(?P<version>[0-9]+\.[0-9]+\.[0-9]+(.*)))?$` | Regexp which enables to verify that the branch is a release one. Capturing group named `version` enables to extract version from the branch name.                                                           |
| `maintenance_branch_pattern` | regexp | `maintenances/(?P<major>[0-9]+)\.(?P<minor>[0-9]+)\.x$`          | Regexp which enables to match a maintenance branch in the repository. If such a branch matches, it will be selected as a target for release commits. Otherwise, the default repository branch will be used. |

### Outputs

| Name                 | Type   | Description                                               |
| -------------------- | ------ | --------------------------------------------------------- |
| `version`            | string | The released version.                                     |
| `major_version`      | string | The released major version.                               |
| `minor_version`      | string | The released minor version.                               |
| `patch_version`      | string | The released patch version.                               |
| `prerelease_version` | string | The released prerelease version.                          |
| `build_version`      | string | The released build version.                               |
| `source_branch`      | string | The release branch name.                                  |
| `target_branch`      | string | The target branch where release commits should be merged. |

## Contributing

This project is totally open source and contributors are welcome.

When you submit a PR, please ensure that the python code is well formatted and linted.

```
$ make install.dependencies
$ make format
$ make lint
```

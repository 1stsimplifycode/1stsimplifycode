# 3D Contribution Calendar — implementation and security

The requested Marketplace project is [Auto 3D Contributions](https://github.com/marketplace/actions/auto-3d-contributions), sourced from [offensive-vk/auto-contributions](https://github.com/offensive-vk/auto-contributions).

## What it does
Generates SVG isometric representations of historical contribution activity. It does **not** create an interactive VR scene or prove the quality of engineering contributions.

## Workflow design
A *manual-trigger only* workflow is proposed in `.github/workflows/profile-3d.yml`. It uses the third-party action's tagged `v7-beta` version, with permissions restricted to repository contents. It attempts to generate `profile-3d-contrib/profile-night-view.svg` and commit it if generated.

**Security:** This third-party action is not GitHub-certified. Review its code and dependencies before approving or running it. Do not inject a personal access token or grant access to private repositories merely to fill in a contribution graphic. The normal repository-scoped `GITHUB_TOKEN` is the proposed credential.

## Publishing
1. Review and merge the profile pull request after inspecting the workflow.
2. Navigate to the profile repository's **Actions** tab.
3. Run **Generate profile 3D contributions** manually.
4. Confirm that the generated SVG is nonempty, correct, and committed before embedding `profile-3d-contrib/profile-night-view.svg` in your README.

The Marketplace documentation's example uses `uses: ./` for a local action; a profile repository generally does not contain that action code. This proposed workflow instead references the third-party action's repository directly.

**Current status:** Configuration prepared; generation and GitHub Actions execution have not been verified. The profile README intentionally avoids referencing a nonexistent image.

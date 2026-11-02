# Repository import status

This GitHub repository currently contains the onboarding and governance scaffold. The complete v5.60.3 course-pack archive has **not yet been imported into the Git tree** through the available GitHub connector workflow.

The source archive exists as a separate 4.53 MB ZIP artifact and contains 1,645 entries. The GitHub connector used for this import can create text files and Git objects, but does not provide a direct local-directory or binary-archive push action. Therefore the current repository should not be represented as containing all academy modules yet.

## Complete the import from a local clone

1. Download the v5.60.3 archive from the project maintainer's retained release artifact.
2. Extract it locally and inspect its contents for sensitive data and third-party licensing constraints.
3. Copy the contents of the extracted `healthcare_data_analyst_academy_v5.60.3/` directory into the root of this repository, preserving paths.
4. Keep the repository-level onboarding and policy files; reconcile duplicate README, catalog, security, data policy, license notice, changelog and workflow files rather than blindly overwriting them.
5. Run the maintained test suite and documentation checks locally.
6. Commit the imported source tree in one reviewed commit.

Do not publish the repository publicly until the owner has reviewed data, assets, dependencies and license rights. This repository's visibility is currently private.

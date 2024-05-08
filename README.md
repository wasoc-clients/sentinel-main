# sentinel-baseline
Sentinel CI/CD main repo

## Using this codespace

On creation / prebuild the devcontainer should have `./scripts/install.sh` run to pull in various content sources. As an analyst updating content for agencies, the `./scripts/update_repos.py` script can be used to transform and deploy content across all repositories this codespace has permissions to.

## Backlog

- [ ] Create some sample content with azure deploy buttons similar to https://github.com/Azure/Azure-Sentinel/tree/master/Playbooks/Change-Incident-Severity
- [ ] Define tailoring process for grabbing content from client workspace, then adjusting it and making re-deployable through a deploy to azure button (as a precursor to full CI/CD integrated repos)
- [ ] Document how to use codespace
  - [x] How to make agency repos
  - [ ] Investigate building analytics rules as ARM json templates from kql queries
  - [ ] How to import / process content - discovery needed to determine is it better to extract/transform templates from packages json or to convert yaml to json with the powershell script in the [sample repo from MS](https://github.com/SentinelCICD/RepositoriesSampleContent/blob/main/Detections/ConvertAnalyticsRuleFromYamlToArm.ps1)
  - [ ] Structure of folders
- [ ] Establish workflow for standard sentinel solutions
- [ ] Establish workflow for 'tuning' an existing rule using an arm template export
- [ ] Establish workflow for configuring main pipelines that can be run by repo users
- [ ] Notebook UI stuff?

## Content sources

The `Azure-Sentinel` repo has all the solutions in the content hub in both package and source yaml form. Defining a script in this repository that 'refreshes content' easily is a fairly high value target as it will mean we can readily update a large amount of detection logic with a small effort from an analyst weekly.

## Repository management

Repositories should be created under the [wasoc-clients](https://github.com/orgs/wasoc-clients/repositories) organisation on github by an organisation owner. Default privileges should be:

- SOC team and agency delegates can 'maintain' repository
- Admins can manage permissions

Likely would have a standardised process as part of onboarding, roughly following these steps:

- Create a repository named `sentinel-{{agency alias}}`, e.g. `sentinel-dpc` and ensure it is private. Add the team `WASOC Admins` with maintain access to the repository initially (agency can be added at a later point once they are ready to deploy content).
- [Launch a new sentinel-main codespace](https://codespaces.new/wasoc-clients/sentinel-main) which will ask for permissions to any new repositories, and then run `./scripts/update-repos.py` from the command line to deploy the initial template content.
- Review content looks ok and ask agency to deploy to their sentinel environment after granting them maintain privileges to the repository.


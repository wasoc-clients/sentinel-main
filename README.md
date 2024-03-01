# sentinel-baseline
Sentinel CI/CD main repo

## Backlog

- [ ] Document how to use codespace
  - [x] How to make agency repos
  - [ ] How to import / process content
  - [ ] Structure of folders
- [ ] Establish workflow for standard sentinel solutions
- [ ] Establish workflow for 'tuning' an existing rule using an arm template export
- [ ] Establish workflow for configuring main pipelines that can be run by repo users
- [ ] Notebook UI stuff?

## Repository management

Repositories should be created under the [wasoc-clients](https://github.com/orgs/wasoc-clients/repositories) organisation on github by an organisation owner. Default privileges should be:

- SOC team and agency delegates can 'maintain' repository
- Admins can manage permissions

Likely would have a standardised process as part of onboarding, roughly following these steps:

- Create a repository named `sentinel-{{agency alias}}`, e.g. `sentinel-dpc` and ensure it is private. Add the team `WASOC Admins` with maintain access to the repository initially (agency can be added at a later point once they are ready to deploy content).
- [Launch a new sentinel-main codespace](https://codespaces.new/wasoc-clients/sentinel-main) which will ask for permissions to any new repositories, and then run `./scripts/update-repos.py` from the command line to deploy the initial template content.
- Review content looks ok and ask agency to deploy to their sentinel environment after granting them maintain privileges to the repository. 


#!/usr/bin/env python
from subprocess import run
from pathlib import Path
import json, zipfile

GITHUB_ORG = "wasoc-clients"
solutions = {
    "Web Session Essentials": ["CommandInURL"]
}

def update_agency_repo(name):
    agency_suffix = name.replace("sentinel-", "")
    git_dir = Path(f"target-repos/{name}/.git")
    if not git_dir.exists():
        run(["gh", "repo", "clone", f"{GITHUB_ORG}/{name}", f"target-repos/{name}"]) # should only need to run the first time
    else:
        run(f"cd target-repos/{name} && git pull", shell=True) # Pull any updated content if e.g. codespace checkout hasn't been updated since agency looked at
    run(["rsync", "-avr", "--delete", "--exclude", ".git", "--exclude", f"{agency_suffix}-overrides", "templates/base/", f"target-repos/{name}/"], check=True) # copy over updated template stuff
    overrides_dir = Path(f"target-repos/{name}/{agency_suffix}-overrides")
    if overrides_dir.exists() and overrides_dir.is_dir():
        print(overrides_dir)
        run(["rsync", "-avr", f"{overrides_dir}/", f"target-repos/{name}/"], check=True) # copy back agency 'overrides' that we may have put in place to tune 'wasoc' content for a specific agency.
    # Git should be smart enough to not commit any modified time but same content files.
    run(f"cd target-repos/{name} && git add . && git commit -am 'updated content' && git push", shell=True) # commit and push changes (probs needs better error logging)


def load_sentinel_content():
    solutions_path = Path("external-content/Azure-Sentinel/Solutions")
    for key, items in solutions.items():
        package_zip = list((solutions_path / key / "Package").glob("*.zip"))[-1] # grab latest zip from package folder
        arm_template = json.load(zipfile.ZipFile(package_zip).open("mainTemplate.json"))
        new_item = arm_template.copy()
        for resource_name in items:
            for resource in arm_template["resources"]:
                if "description" in resource["properties"] and resource["properties"]["description"].startswith(resource_name):
                    new_item["resources"] = resource["properties"]["mainTemplate"]["resources"]
                    for sub_resource in new_item["resources"]: # may need to remove metadata resource thing if causes issues deploying
                        if sub_resource["type"].endswith("AlertRuleTemplates"):
                            sub_resource["type"] = sub_resource["type"].replace("AlertRuleTemplates", "AlertRule")
                            sub_resource["location"] = "[resourceGroup().location]"
                    new_item["parameters"] = { "workspace": { "type": "String" } }
        return new_item
        # print(zip.namelist())
        # TODO: find items in the arm resource template, and see how hard they are to make 'deployable' rules that sentinel ci/cd will push for us.
        # Error to debug on deploying: {"code":"InvalidTemplate","message":"Deployment template validation failed: 'The template resource '32c08696-2e37-4730-86f8-97d9c8b184c9' for type 'Microsoft.OperationalInsights/workspaces/providers/alertRules' at line '197' and column '81' has incorrect segment lengths. A nested resource type must have identical number of segments as its resource name. A root resource type must have segment length one greater than its resource name. Please see https://aka.ms/arm-syntax-resources for usage details.'."}



if __name__ == "__main__":
    # Repositories this codespace has permissions to update
    repos = json.loads(run(["gh", "repo", "list", f"{GITHUB_ORG}", "--json", "name"], capture_output=True).stdout.decode("utf8"))
    for repo in repos:
        name = repo["name"]
        if name.endswith("-main") or not name.startswith("sentinel-"): # Ignore main template repo and any repo not starting with `sentinel-`
            continue
        try:
            update_agency_repo(name)
        except Exception as e:
            print(e)
            continue
    

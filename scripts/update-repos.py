#!/usr/bin/env python
from subprocess import run
import json

repos = json.loads(run(["gh", "repo", "list", "wasoc-clients", "--json", "name"], capture_output=True).stdout.decode("utf8"))
for repo in repos:
    name = repo["name"]
    if name.endswith("-main") or not name.startswith("sentinel-"): # Ignore main template repo and any repo not starting with `sentinel-`
        continue
    run(["gh", "repo", "clone", f"wasoc-clients/{name}", f"target-repos/{name}"]) # should only need to run the first time
    run(f"cd target-repos/{name} && git pull", shell=True) # Pull any updated content if e.g. codespace checkout hasn't been updated since agency looked at
    run(["rsync", "-avr", "--exclude", ".git", "templates/base/", f"target-repos/{name}/"]) # copy over updated template stuff
    # copy back agency 'overrides' that we may have put in place to tune 'wasoc' content for a specific agency.
    # e.g. cp target-repos/{name}/{agencysuffix}-override target-repos/{name}/
    # Git should be smart enough to not commit any modified time but same content files.
    run(f"cd target-repos/{name} && git add . && git commit -am 'updated content' && git push", shell=True) # commit and push changes (probs needs better error logging)

#!/usr/bin/env python
from subprocess import run
import json

repos = json.loads(run(["gh", "repo", "list", "wasoc-clients", "--json", "name"], capture_output=True).stdout.decode("utf8"))
for repo in repos:
    name = repo["name"]
    if name.endswith("-main") or not name.startswith("sentinel-"): # Ignore main template repo and any repo not starting with `sentinel-`
        continue
    run(["gh", "repo", "clone", f"wasoc-clients/{name}", f"target-repos/{name}"]) # should only need to run the first time
    run(["rsync", "-avr", "--exclude", ".git", "templates/base/", f"target-repos/{name}/"]) # copy over updated template stuff
    run(f"cd target-repos/{name} && git add . && git commit -am 'updated content' && git push", shell=True) # commit and push changes (probs needs better error logging)

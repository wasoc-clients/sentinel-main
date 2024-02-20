#!/usr/bin/env python
from subprocess import run
import json

repos = json.loads(run(["gh", "repo", "list", "wasoc-clients", "--json", "url"], capture_output=True).stdout.decode("utf8"))
for repo in repos:
    url = repo["url"]
    if url.endswith("-main"):
        continue
    print(url)
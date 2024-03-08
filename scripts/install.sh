#!/bin/bash
# below should only need to run once
mkdir external-content target-repos
gh repo clone SentinelCICD/RepositoriesSampleContent external-content/SentinelCICD-Template -- --depth 1
gh repo clone Azure/Azure-Sentinel external-content/Azure-Sentinel -- --depth 1
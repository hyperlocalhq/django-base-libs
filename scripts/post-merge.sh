#! /usr/bin/env bash
# notify NewRelic of new deployment to production

## prevent referencing undefined variables (which default to "")
set -o nounset
## ignore failing commands
set -o errexit

display_usage() {
    echo "Usage: $0 commit_hash"
    exit 1
}

if [ $# -eq 0 ]; then
    display_usage
    exit 1
fi

# check whether user had supplied -h or --help . If yes display usage
if [[ ( "$1" == "--help") ||  "$1" == "-h" ]]; then
    display_usage
    exit 0
fi

REVISION=${1}

curl \
-H "x-api-key:dfffb2b48abee5204529774c5acef511e512f8a763ea144" \
-d "deployment[application_id]=470332" \
-d "deployment[description]=New version of the app was deployed" \
-d "deployment[revision]=${REVISION}" \
https://api.newrelic.com/deployments.xml

# -d "deployment[changelog]=Changelog" \
# -d "deployment[user]=User" \

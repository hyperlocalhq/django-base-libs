#! /usr/bin/env bash
## MIT © Sindre Sorhus - sindresorhus.com

## git hook to run a command after `git pull` if a specified file was changed
## Run `chmod +x post-merge` to make it executable then put it into `.git/hooks/`.

## This particular hook notifies NewRelic of a new deployment to the production repo

## prevent referencing undefined variables (which default to "")
set -o nounset
## ignore failing commands
set -o errexit

newrelic_api_key=dfffb2b48abee5204529774c5acef511e512f8a763ea144
newrelic_application_id=470332

commit_description=$(git log -1 --pretty=format:%s)
commit_author=$(git log -1 --pretty=format:%cn)
## abbreviated commit SHA:
commit_revision=$(git log -1 --pretty=format:%h)
## full commit SHA:
# commit_revision=$(git log -1 --pretty=format:%H)

## Where to store the log information about the updates
LOGFILE=./post-merge.log

##  Record the fact that a merge was performed
echo -e "Performed merge at $( date +'%Y-%m-%dT%H:%M:%SZ' )" >> ${LOGFILE}
echo " - New SHA: ${commit_revision}" >> ${LOGFILE}

curl \
    --header "x-api-key:${newrelic_api_key}" \
    --data "deployment[application_id]=${newrelic_application_id}" \
    --data "deployment[description]=${commit_description}" \
    --data "deployment[user]=${commit_author}" \
    --data "deployment[revision]=${commit_revision}" \
    https://api.newrelic.com/deployments.xml 1>> ${LOGFILE} 2>&1

echo "Notified NewRelic about new deployment" >> ${LOGFILE}
echo "" >> ${LOGFILE}

echo "post-merge hook notified NewRelic about new deployment"

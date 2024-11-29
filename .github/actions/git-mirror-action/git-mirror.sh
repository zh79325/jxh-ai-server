#!/bin/sh

set -e

SOURCE_REPO=$1
DESTINATION_REPO=$2
SOURCE_DIR=$(basename "$SOURCE_REPO")
DRY_RUN=$3

GIT_SSH_COMMAND="ssh -v"

echo "SOURCE=$SOURCE_REPO"
echo "DESTINATION=$DESTINATION_REPO"
echo "DRY RUN=$DRY_RUN"

git clone --mirror "$SOURCE_REPO" "$SOURCE_DIR" && cd "$SOURCE_DIR"
git lfs fetch --all
rm -rf .gitattributes
git remote set-url --push origin "$DESTINATION_REPO"
git fetch -p origin
# Exclude refs created by GitHub for pull request.
git for-each-ref --format 'delete %(refname)' refs/pull | git update-ref --stdin

if [ "$DRY_RUN" = "true" ]
then
    echo "INFO: Dry Run, no data is pushed"
    git push --mirror --dry-run
    #git lfs push --all origin main
else
    git push --mirror
    #git lfs push --all origin main
fi

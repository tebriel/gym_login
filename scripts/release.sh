#!/usr/bin/env bash

set -euox pipefail

API_TOKEN=${API_TOKEN?Github API Token must be set}
NOW=${1?Must set tag for release}
REPO_URL=https://api.github.com/repos/tebriel/gym_login/releases
TAG_NAME=$(date +%s)
COMMITISH=$(git rev-parse HEAD)
NAME="Release: ${TAG_NAME}"
BODY="Auto Release"
ASSET_NAME="assets.tar.gz"

REL_DIR=$(mktemp -d)
cp -R release ${REL_DIR}

pushd ${REL_DIR}

sed -i .orig -e 's/:latest/:'"${NOW}"'/' release/docker-compose.yml
rm release/docker-compose.yml.orig

RELEASE_JSON="
    {
        \"tag_name\": \"${TAG_NAME}\",
        \"target_commitish\": \"${COMMITISH}\",
        \"name\": \"${NAME}\",
        \"body\": \"${BODY}\"
    }
    "

tar cvzf ${ASSET_NAME} release

UPLOAD_URL=$(curl -XPOST \
    -H "Authorization: token ${API_TOKEN}" \
    -d "${RELEASE_JSON}" \
    ${REPO_URL} | jq ".upload_url" | sed -e 's/{?name,label}//' -e 's/"//g')

curl -XPOST \
    -H "Authorization: token ${API_TOKEN}" \
    -H "Content-Type: application/compressed-tar" \
    --data-binary "@${ASSET_NAME}" \
    "${UPLOAD_URL}?name=${ASSET_NAME}"

popd
rm -r ${REL_DIR}

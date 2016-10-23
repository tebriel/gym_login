#!/usr/bin/env bash

set -euox pipefail

API_TOKEN=${API_TOKEN?Github API Token must be set}
REPO_URL=https://api.github.com/repos/tebriel/gym_login/releases
TAG_NAME=$(date +%s)
COMMITISH=$(git rev-parse HEAD)
NAME="Release: ${TAG_NAME}"
BODY="Auto Release"

RELEASE_JSON="
    {
        \"tag_name\": \"${TAG_NAME}\",
        \"target_commitish\": \"${COMMITISH}\",
        \"name\": \"${NAME}\",
        \"body\": \"${BODY}\"
    }
    "

curl -XPOST \
    -H "Authorization: token ${API_TOKEN}" \
    -d "${RELEASE_JSON}" \
    ${REPO_URL}

#!/usr/bin/env bash
set -e -x

if ! [ -z ${DOCKER_IMAGE+x} ]; then
  export CLOUD_CONTAINER_NAME=travis-dev-wheels
  pip install wheelhouse_uploader
  python -m wheelhouse_uploader upload --local-folder \
    ${TRAVIS_BUILD_DIR}/dist/ ${CLOUD_CONTAINER_NAME}
  fi
fi

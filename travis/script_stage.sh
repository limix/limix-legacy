#!/usr/bin/env bash
set -e -x

if [ -z ${DOCKER_IMAGE+x} ]; then
  python setup.py sdist
  pip install dist/`ls dist | grep -i -E '\.(gz)$' | head -1` -vvv
  pushd /
  python -c "import sys; import limix_legacy; sys.exit(limix_legacy.test())"
  popd
else
  docker run --rm -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/travis/build-wheels.sh
  ls wheelhouse/
fi

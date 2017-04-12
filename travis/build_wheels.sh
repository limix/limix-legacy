#!/bin/bash
set -e -x

yum install -y atlas-devel libffi libffi-devel

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    if [[ $PYBIN == *"p26"* ]] || [[ $PYBIN == *"p33"* ]] || \
       [[ $PYBIN == *"p34"* ]]; then
        continue
    fi
    "${PYBIN}/pip" install Cython numpy
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/limix_legacy*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    if [[ $PYBIN == *"p26"* ]] || [[ $PYBIN == *"p33"* ]] \
        || [[ $PYBIN == *"p34"* ]]; then
        continue
    fi
    "${PYBIN}/pip" install limix_legacy -f /io/wheelhouse
    "${PYBIN}/pip" install pytest
    cd "$HOME"
    "${PYBIN}/python" -c "import sys; import limix_legacy; sys.exit(limix_legacy.test())"
done

from pkg_resources import DistributionNotFound as _DistributionNotFound
from pkg_resources import get_distribution as _get_distribution

from . import io
from .mtSet import MTSet
from .varDecomp import VarianceDecomposition

try:
    __version__ = _get_distribution('limix-legacy').version
except _DistributionNotFound:
    __version__ = 'unknown'



def test():
    import os
    p = __import__('limix_legacy').__path__[0]
    src_path = os.path.abspath(p)
    old_path = os.getcwd()
    os.chdir(src_path)

    try:
        return_code = __import__('pytest').main(['-q', '--doctest-modules'])
    finally:
        os.chdir(old_path)

    if return_code == 0:
        print("Congratulations. All tests have passed!")

    return return_code


__all__ = ['io']

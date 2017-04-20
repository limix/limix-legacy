from pkg_resources import DistributionNotFound as _DistributionNotFound
from pkg_resources import get_distribution as _get_distribution

from . import io

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
        return_code = __import__('pytest').main([
            '-q', '--doctest-modules',
            '--ignore=modules/dirIndirVD_commented_forDistrib.py',
            '--ignore=modules/social_data_HSmice_paper.py',
            '--ignore=deprecated/io/genotype_reader.py',
            '--ignore=deprecated/io/output_writer.py',
            '--ignore=deprecated/io/phenotype_reader.py',
            '--ignore=io/genotype_reader.py',
            '--ignore=io/output_writer.py',
            '--ignore=io/phenotype_reader.py',
        ])
    finally:
        os.chdir(old_path)

    if return_code == 0:
        print("Congratulations. All tests have passed!")

    return return_code


__all__ = ['io']

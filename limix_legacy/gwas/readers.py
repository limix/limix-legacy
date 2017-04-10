import h5py
import dask.array as da
import dask.dataframe as dd
import pandas as pd

from numpy.testing import assert_allclose, assert_equal


if __name__ == '__main__':

    # GEN files (dosage)
    df = read_gen('example')
    assert_equal(df['sample']['sample_id'][1], '1A1')
    assert_equal(df['sample']['age'][0], 4)
    assert_allclose(df['genotype']['1A4']['AB'][0], 0.0207)

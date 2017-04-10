from __future__ import division

import pytest
from numpy import concatenate, dot, empty, log, set_printoptions, array
from numpy.linalg import eigvalsh, matrix_rank, norm
from numpy.random import RandomState
from numpy.testing import assert_, assert_allclose

from lmm_core import DoubleBlockScan, SingleBlockScan
from numpy_sugar import epsilon
from numpy_sugar.linalg import lstsq, plogdet, rsolve, solve, sum2diag


def _get_phenotype(n):
    random = RandomState(2)
    return random.randn(n)


def _get_full_rank_K(n):
    random = RandomState(0)
    K = random.randn(n, n)
    K = dot(K, K.T)
    sum2diag(K, 1e-3, out=K)
    K /= K.diagonal().mean()
    assert matrix_rank(K) == n
    return K


def _get_low_rank_K(n):
    random = RandomState(0)
    K = random.randn(n, 1)
    K = dot(K, K.T)
    K /= K.diagonal().mean()
    assert matrix_rank(K) < n
    return K


def _get_badly_conditioned_K():
    K = array([[
        168.15039615, 188.40616494, 52.00891469, 150.5850811, -68.07484624,
        -100.09532827, -97.3057006, -20.95518674, 45.68255616, -44.90563005
    ], [
        188.40616494, 435.59562531, 130.49010606, 218.45267545, -87.50616204,
        -156.6060063, -226.25366219, -108.71144653, 84.78503486, -76.32761492
    ], [
        52.00891469, 130.49010606, 198.31915517, 262.60532168, -148.58017968,
        -15.50103445, 160.47120622, 60.4489757, 15.59598317, 77.56958248
    ], [
        150.5850811, 218.45267545, 262.60532168, 429.49508489, -236.54330753,
        -41.91289812, 127.5960376, 65.22176261, 36.34812068, 70.54849002
    ], [
        -68.07484624, -87.50616204, -148.58017968, -236.54330753, 147.17658965,
        21.19795614, -103.26996429, -38.94025205, -3.12553141, -44.81814848
    ], [
        -100.09532827, -156.6060063, -15.50103445, -41.91289812, 21.19795614,
        120.71975905, 104.82333062, 83.51631399, -21.41772336, 73.32909002
    ], [
        -97.3057006, -226.25366219, 160.47120622, 127.5960376, -103.26996429,
        104.82333062, 516.06458343, 228.84407241, -52.29159718, 204.56724198
    ], [
        -20.95518674, -108.71144653, 60.4489757, 65.22176261, -38.94025205,
        83.51631399, 228.84407241, 163.75464039, -6.13436299, 118.81762097
    ], [
        45.68255616, 84.78503486, 15.59598317, 36.34812068, -3.12553141,
        -21.41772336, -52.29159718, -6.13436299, 26.36138838, -10.74028695
    ], [
        -44.90563005, -76.32761492, 77.56958248, 70.54849002, -44.81814848,
        73.32909002, 204.56724198, 118.81762097, -10.74028695, 104.46287768
    ]])
    return K


def _get_full_column_covariate(n, p, seed=1):
    random = RandomState(seed)
    G = random.randn(n, p)
    G = (G - G.mean(0)) / G.std(0)
    assert matrix_rank(G) == p
    return G


def _get_low_column_covariate(n, p, seed=1):
    random = RandomState(1)
    G = empty((n, p))
    G[:] = random.randn(n, 1)
    G = (G - G.mean(0)) / G.std(0)
    assert matrix_rank(G) < G.shape[1]
    return G


def test_gwas_single_block_full_rank_K():
    y = _get_phenotype(10)
    K = _get_full_rank_K(10)
    G = _get_full_column_covariate(10, 2)

    scan = SingleBlockScan([y, rsolve(K, y)], [G, rsolve(K, G)], plogdet(K))
    assert_allclose(scan.beta, [-0.5822643333748893, -0.3186171189150498])
    assert_allclose(scan.var(), 8.2116648457402555)
    assert_allclose(scan.var(reml=True), 10.264581057175318)
    assert_allclose(scan.lml(), -17.6545789375957)
    assert_allclose(scan.lml(reml=True), -18.19683064556113)


def test_gwas_single_block_low_rank_K():
    y = _get_phenotype(10)
    K = _get_low_rank_K(10)
    G = _get_full_column_covariate(10, 2)

    scan = SingleBlockScan([y, rsolve(K, y)], [G, rsolve(K, G)], plogdet(K))
    assert_(scan.lml() >= 164)
    assert_(scan.lml(reml=True) >= 135.03121298755426)


def test_gwas_single_block_full_rank_K_low_colrank_covariate():
    y = _get_phenotype(10)
    K = _get_full_rank_K(10)
    G = _get_low_column_covariate(10, 5)

    scan = SingleBlockScan([y, rsolve(K, y)], [G, rsolve(K, G)], plogdet(K))
    assert_allclose(scan.lml(), -15.55519276844987)
    assert_allclose(scan.lml(reml=True), -9.74311405765727)


def test_gwas_single_block_low_rank_K_low_colrank_covariate():
    y = _get_phenotype(10)
    K = _get_low_rank_K(10)
    G = _get_low_column_covariate(10, 5)

    scan = SingleBlockScan([y, rsolve(K, y)], [G, rsolve(K, G)], plogdet(K))
    assert_(scan.lml() >= 164)
    assert_(scan.lml(reml=True) >= 83)

def test_gwas_single_block_badly_conditioned_K():
    y = _get_phenotype(10)
    K = _get_badly_conditioned_K()
    G = _get_full_column_covariate(10, 2)

    scan = SingleBlockScan([y, rsolve(K, y)], [G, rsolve(K, G)], plogdet(K))
    assert_allclose(scan.lml(), 3.1179719536880484)
    assert_allclose(scan.lml(reml=True), -2.7452042164467456)

def _compare_the_two(y, K, G0, G1, reml):
    scan = DoubleBlockScan((y, rsolve(K, y)), (G0, rsolve(K, G0)), plogdet(K))
    scan.set_second_block(G1, rsolve(K, G1))
    alpha, beta = scan.beta
    beta = concatenate((alpha, beta))

    G01 = concatenate((G0, G1), axis=1)

    left = dot(G01.T, rsolve(K, dot(G01, beta)))
    right = dot(G01.T, rsolve(K, y))
    e0 = norm(left - right)
    var0 = scan.var(reml)
    lml0 = scan.lml(reml)

    scan = SingleBlockScan([y, rsolve(K, y)], [G01, rsolve(K, G01)],
                           plogdet(K))
    left = dot(G01.T, rsolve(K, dot(G01, scan.beta)))
    right = dot(G01.T, rsolve(K, y))
    e1 = norm(left - right)
    var1 = scan.var(reml)
    lml1 = scan.lml(reml)

    assert_allclose(e0, e1, atol=1e-6)
    if var0 + var1 >= 100 * epsilon.small:
        assert_allclose(var0, var1, atol=1e-6)
        assert_allclose(lml0, lml1, atol=1e-6)


def test_gwas_double_block_full_ranks():
    y = _get_phenotype(20)
    K = _get_full_rank_K(20)
    G0 = _get_full_column_covariate(20, 2, seed=0)
    G1 = _get_full_column_covariate(20, 2, seed=1)
    _compare_the_two(y, K, G0, G1, reml=False)
    _compare_the_two(y, K, G0, G1, reml=True)


def test_gwas_double_block_lowK():
    y = _get_phenotype(20)
    K = _get_low_rank_K(20)
    G0 = _get_full_column_covariate(20, 2, seed=0)
    G1 = _get_full_column_covariate(20, 2, seed=1)
    _compare_the_two(y, K, G0, G1, reml=False)
    _compare_the_two(y, K, G0, G1, reml=True)


def test_gwas_double_block_repeated_covariate():
    y = _get_phenotype(20)
    K = _get_full_rank_K(20)
    G0 = _get_full_column_covariate(20, 2, seed=0)
    _compare_the_two(y, K, G0, G0, reml=False)
    _compare_the_two(y, K, G0, G0, reml=True)


def test_gwas_double_block_low_ranks_repeat():
    y = _get_phenotype(20)
    K = _get_low_rank_K(20)
    G0 = _get_low_column_covariate(20, 2, seed=0)
    _compare_the_two(y, K, G0, G0, reml=False)
    _compare_the_two(y, K, G0, G0, reml=True)

def test_gwas_double_block_badly_conditioned():
    y = _get_phenotype(10)
    K = _get_badly_conditioned_K()
    G0 = _get_low_column_covariate(10, 2, seed=0)
    G1 = _get_low_column_covariate(10, 2, seed=5)
    _compare_the_two(y, K, G0, G1, reml=False)
    _compare_the_two(y, K, G0, G1, reml=True)


if __name__ == '__main__':
    pytest.main(["-q", "-s"])

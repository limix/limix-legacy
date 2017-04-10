"""LMM testing code"""
import unittest
import scipy as SP
import numpy as np
import sys
from limix_legacy.core.covar import FixedCov
from limix_legacy.utils.check_grad import mcheck_grad
from limix_legacy.core.type.exception import NotArrayConvertibleError

class TestFixed(unittest.TestCase):
    def setUp(self):
        pass

    def test_input(self):
        FixedCov(np.eye(10))
        with self.assertRaises(NotArrayConvertibleError):
            FixedCov("Ola meu querido.")

        A = np.asarray([[np.inf], [1.]], dtype=float)
        with self.assertRaises(ValueError):
            FixedCov(A)

if __name__ == '__main__':
    unittest.main()

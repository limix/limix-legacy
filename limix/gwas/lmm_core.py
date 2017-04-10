from __future__ import division

import logging

from numpy import concatenate, dot, log, pi, zeros
from numpy.linalg import LinAlgError
from numpy_sugar import epsilon
from numpy_sugar.linalg import ddot, economic_svd, lstsq, plogdet

_l2pi = log(2 * pi)


class SingleBlockScan(object):
    def __init__(self, ys, Gs, logdetK=None):
        self._ys = ys
        self._Gs = Gs
        self._GtKG = dot(Gs[0].T, Gs[1])
        self._logdetK = logdetK
        self._beta = None
        self._var = dict(reml=None, ml=None)

    def _nk(self, reml):
        if reml:
            if self._Gs[0].shape[1] >= len(self._ys[0]):
                msg = "The number of covariates cannot"
                msg += " be equal or larger than the number of individuals."
                raise ValueError(msg)
            return len(self._ys[0]) - self._Gs[0].shape[1]
        return len(self._ys[0])

    @property
    def beta(self):
        if self._beta is not None:
            return self._beta

        try:
            self._beta = lstsq(self._GtKG, dot(self._Gs[0].T, self._ys[1]))
        except LinAlgError as e:
            logging.getLogger().warning(str(e))
            self._beta = zeros(self._Gs[0].shape[1])

        return self._beta

    def var(self, reml=False):
        if reml:
            v = self._var['reml']
        else:
            v = self._var['ml']

        if v is not None:
            return v

        left = self._ys[0] - dot(self._Gs[0], self.beta)
        right = self._ys[1] - dot(self._Gs[1], self.beta)
        v = max(epsilon.tiny, dot(left, right) / self._nk(reml))
        return v

    def lml(self, reml=False):
        v = self.var(reml)
        nk = self._nk(reml)
        r = -nk * _l2pi - self._logdetK - nk * log(v) - nk
        if reml:
            r += plogdet(dot(self._Gs[0].T, self._Gs[0]))
            r -= plogdet(self._GtKG)
        return r / 2


class DoubleBlockScan(object):
    def __init__(self, ys, Gs, logdetK=None):
        self._ys = ys
        self._logdetK = logdetK
        self._beta = None
        self._var = dict(reml=None, ml=None)
        self._block = dict()
        self._block[0] = {
            'G': Gs[0],
            'KiG': Gs[1],
            'GtKiG': dot(Gs[0].T, Gs[1])
        }
        self._block[1] = {'G': None, 'KiG': None, 'GtiKG': None}
        A = self._block[0]['GtKiG']
        self._AG0ty = lstsq(A, dot(Gs[0].T, self._ys[1]))

    def set_second_block(self, G, KiG):
        self._block[1] = {'G': G, 'KiG': KiG, 'GtKiG': dot(G.T, KiG)}
        self._beta = None
        self._var = dict(reml=None, ml=None)

    def _nk(self, reml):
        if reml:
            k = self._block[0]['G'].shape[1] + self._block[1]['G'].shape[1]
            if k >= len(self._ys[0]):
                msg = "The number of covariates cannot"
                msg += " be equal or larger than the number of individuals."
                raise ValueError(msg)
            return len(self._ys[0]) - k
        return len(self._ys[0])

    @property
    def beta(self):
        AG0ty = self._AG0ty

        if self._block[1]['G'] is None:
            return AG0ty, None

        A = self._block[0]['GtKiG']
        B = dot(self._block[0]['KiG'].T, self._block[1]['G'])
        C = self._block[1]['GtKiG']

        W = C - dot(B.T, lstsq(A, B))
        USV = economic_svd(W)
        SiV = ddot(1 / USV[1], USV[2], left=True)

        G1ty = dot(self._block[1]['G'].T, self._ys[1])

        BtAG0ty = dot(B.T, AG0ty)

        beta0 = AG0ty + lstsq(A, dot(B, dot(USV[0], dot(SiV, BtAG0ty - G1ty))))
        beta1 = dot(USV[0], dot(SiV, G1ty - BtAG0ty))

        return beta0, beta1

    def var(self, reml=False):
        if reml:
            v = self._var['reml']
        else:
            v = self._var['ml']

        if v is not None:
            return v

        beta0, beta1 = self.beta

        left = self._ys[0] - dot(self._block[0]['G'], beta0)
        right = self._ys[1] - dot(self._block[0]['KiG'], beta0)

        if beta1 is not None:
            left -= dot(self._block[1]['G'], beta1)
            right -= dot(self._block[1]['KiG'], beta1)

        return max(1e-300, dot(left, right) / self._nk(reml))

    def lml(self, reml=False):
        v = self.var(reml)
        nk = self._nk(reml)
        r = -nk * _l2pi - self._logdetK - nk * log(v) - nk
        if reml:
            X = concatenate((self._block[0]['G'], self._block[1]['G']), axis=1)
            r += plogdet(dot(X.T, X))
            KiX = concatenate(
                (self._block[0]['KiG'], self._block[1]['KiG']), axis=1)
            r -= plogdet(dot(X.T, KiX))
        return r / 2

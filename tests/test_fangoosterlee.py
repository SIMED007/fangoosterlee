#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testing suite for COS method.

"""
from __future__ import print_function, division

import os
import sys
import unittest as ut
import numpy as np

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(),\
    os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from fangoosterlee.fangoosterlee import cosmethod, cfinverse
from fangoosterlee.examples import (GBM, GBMParam, VarGamma, VarGammaParam,
                        Heston, HestonParam)

class COSTestCase(ut.TestCase):
    """Test COS method."""

    def test_gbm(self):
        """Test GBM model."""

        price, strike = 100, 90
        riskfree, maturity = 0, 30/365

        sigma = .15

        model = GBM(GBMParam(sigma=sigma), riskfree, maturity)
        premium = cosmethod(model, price=price, strike=strike,
                            maturity=maturity, riskfree=riskfree, call=True)

        self.assertEqual(premium.shape, (1,))

        strike = np.exp(np.linspace(-.1, .1, 10))
        premium = cosmethod(model, price=price, strike=strike,
                            maturity=maturity, riskfree=riskfree, call=True)

        self.assertEqual(premium.shape, strike.shape)

    def test_vargamma(self):
        """Test VarGamma model."""

        price, strike = 100, 90
        riskfree, maturity = 0, 30/365

        nu = .2
        theta = -.14
        sigma = .25

        param = VarGammaParam(theta=theta, nu=nu, sigma=sigma)
        model = VarGamma(param, riskfree, maturity)
        premium = cosmethod(model, price=price, strike=strike,
                            maturity=maturity, riskfree=riskfree, call=True)

        self.assertEqual(premium.shape, (1,))

        strike = np.exp(np.linspace(-.1, .1, 10))
        premium = cosmethod(model, price=price, strike=strike,
                            maturity=maturity, riskfree=riskfree, call=True)

        self.assertEqual(premium.shape, strike.shape)


    def test_heston(self):
        """Test Heston model."""

        price, strike = 100, 90
        riskfree, maturity = 0, 30/365

        lm = 1.5768
        mu = .12**2
        eta = .5751
        rho = -.0
        sigma = .12**2

        param = HestonParam(lm=lm, mu=mu, eta=eta, rho=rho, sigma=sigma)
        model = Heston(param, riskfree, maturity)
        premium = cosmethod(model, price=price, strike=strike,
                            maturity=maturity, riskfree=riskfree, call=True)

        self.assertEqual(premium.shape, (1,))

        strike = np.exp(np.linspace(-.1, .1, 10))
        premium = cosmethod(model, price=price, strike=strike,
                            maturity=maturity, riskfree=riskfree, call=True)

        self.assertEqual(premium.shape, strike.shape)

    def test_cfinverse(self):
        """Test Fourier inversion."""

        riskfree, maturity = 0, 30/365
        sigma = .15
        points = int(1e4)

        model = GBM(GBMParam(sigma=sigma), riskfree, maturity)

        grid, density = cfinverse(model.charfun, points=points)

        self.assertEqual(grid.shape, (points,))
        self.assertEqual(density.shape, (points,))


if __name__ == '__main__':
    ut.main()

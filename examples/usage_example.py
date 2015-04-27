#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage examples of Fang-Oosterlee COS method
-------------------------------------------

"""
from __future__ import division, print_function

import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from fangoosterlee import (GBM, GBMParam, VarGamma, VarGammaParam,
                           Heston, HestonParam, ARG, ARGParam)
from fangoosterlee import cosmethod


def single_premium():
    """Test COS method for floats.

    """
    price, strike = 100, 90
    riskfree, maturity = 0, 30/365
    sigma = .15
    moneyness = np.log(strike/price) - riskfree * maturity

    model = GBM(GBMParam(sigma=sigma), riskfree, maturity)
    premium = cosmethod(model, moneyness=moneyness, call=True)
    print(premium)

    nu = .2
    theta = -.14
    sigma = .25
    param = VarGammaParam(theta=theta, nu=nu, sigma=sigma)
    model = VarGamma(param, riskfree, maturity)
    premium = cosmethod(model, moneyness=moneyness, call=True)
    print(premium)

    lm = 1.5768
    mu = .12**2
    eta = .5751
    rho = -.0
    sigma = .12**2
    param = HestonParam(lm=lm, mu=mu, eta=eta, rho=rho, sigma=sigma)
    model = Heston(param, riskfree, maturity)
    premium = cosmethod(model, moneyness=moneyness, call=True)
    print(premium)

    rho = .55
    delta = .75
    mu = .2**2/365
    sigma = .2**2/365
    phi = -.0
    theta1 = -16.0
    theta2 = 20.95
    param = ARGParam(rho=rho, delta=delta, mu=mu, sigma=sigma,
                     phi=phi, theta1=theta1, theta2=theta2)
    model = ARG(param, riskfree, maturity)
    premium = cosmethod(model, moneyness=moneyness, call=True)
    print(premium)


def multiple_premia_gbm(nobs=2000):
    """Test COS method on the grid.

    """
    sigma = .15

    price = 1
    strike = np.exp(np.linspace(-.1, .1, nobs))
    riskfree, maturity = 0, 30/365
    moneyness = np.log(strike/price) - riskfree * maturity

    model = GBM(GBMParam(sigma=sigma), riskfree, maturity)
    premium = cosmethod(model, moneyness=moneyness, call=True)
    plt.plot(strike, premium)
    plt.show()


def multiple_premia_heston(nobs=2000):
    """Test COS method on the grid.

    """
    lm = 1.5768
    mu = .12**2
    eta = .5751
    rho = -.0
    sigma = .12**2

    price = 1
    strike = np.exp(np.linspace(-.1, .1, nobs))
    maturity = 30/365
    riskfree = .01 * np.ones(nobs)
    moneyness = np.log(strike/price) - riskfree * maturity

    param = HestonParam(lm=lm, mu=mu, eta=eta, rho=rho, sigma=sigma)
    model = Heston(param, riskfree, maturity)
    premium = cosmethod(model, moneyness=moneyness, call=True)
    plt.plot(strike, premium)
    plt.show()


if __name__ == '__main__':

    sns.set_context('notebook')
    single_premium()
#    multiple_premia_gbm()
#    multiple_premia_heston(1000)

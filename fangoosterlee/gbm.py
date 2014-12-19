#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Geometric Brownian Motion
=========================

"""

import numpy as np

__all__ = ['GBM']


def CFGBM(u, P):
    # Geometric Brownian Motion characteristic function
    # u is N-vector
    # T,r,sigma,nu,theta are scalars
    # returns N-vector
    T = P['T']
    r = P['r']
    sigma = P['sigma']

    # N-vector
    return np.exp(u * r * T * 1j - u**2 * sigma**2 * T / 2)


class GBM(object):

    """Geometric Brownian Motion.

    Attributes
    ----------
    sigma
        Annualized volatility

    Methods
    -------
    charfun
        Characteristic function

    """

    def __init__(self, sigma, riskfree, maturity):
        """Initialize the class.

        Parameters
        ----------
        sigmma
            Annualized volatility

        """
        self.sigma = sigma
        self.riskfree = riskfree
        self.maturity = maturity

    def charfun(self, arg):
        """Characteristic function.

        Parameters
        ----------
        arg : array_like
            Grid to evaluate the function
        riskfree : float
            Risk-free rate, annualized
        maturity : float
            Fraction of a year

        Returns
        -------
        array_like
            Values of characteristic function

        """
        return np.exp(arg * self.riskfree * self.maturity * 1j
                      - arg**2 * self.sigma**2 * self.maturity / 2)

    def cos_restriction(self):

        # Truncation rate
        L = 100 # scalar
        c1 = self.riskfree * self.maturity
        c2 = self.sigma**2 * self.maturity

        a = c1 - L * np.sqrt(c2) # scalar
        b = c1 + L * np.sqrt(c2) # scalar

        return L, c1, c2, a, b

# -*- coding: utf-8 -*-
"""
ABSTRACT: This is a 3 sector model : bank, household, and production.
* Everything is stock-flow consistent, but capital is not created by real products
* The model is driven by offer
* Negociation by philips is impacted by the profit
* Loans from banks are limited by solvability
TYPICAL BEHAVIOR : convergent oscillation around a solow point / debt crisis

LINKTOARTICLE : Goodwin, Richard, 1967. ‘A growth cycle’, in:
    Carl Feinstein, editor, Socialism, capitalism
    and economic growth. Cambridge, UK: Cambridge University Press.

Created on Wed Jul 21 15:11:15 2021

@author: Paul Valcke
"""

import numpy as np

# ---------------------------
# user-defined function order (optional)


# ---------------------------
# user-defined model
# contains parameters and functions of various types


_LOGICS = {
    'differential': {
        'employment': {
            'func': lambda employment, g, alpha, n: employment * (g - alpha - n),
            'com': 'reduced 3variables dynamical expression'
        },
        'omega': {
            'func': lambda omega, phillips, inflation, gammai, alpha: omega * (phillips - (1 - gammai)*inflation-alpha),
            'com': 'reduced 3variables dynamical expression',
        },
        'd': {
            'func': lambda d, kappa, pi, g, inflation: kappa - pi - d*(g+inflation),
            'com': 'no solvability in loans'
        }
    },
    'statevar': {
        'phillips': {
            'func': lambda phi0, phi1, employment: (-phi0 + phi1 / (1 - employment)**2),
            'com': 'salary negociation on employement and profit',
        },
        'g': {
            'func': lambda kappa, nu, delta: kappa / nu - delta,
            'com': 'Goodwin explicit Growth',
        },
        'pi': {
            'func': lambda omega, r, d: 1. - omega - r * d,
            'com': 'Goodwin relative profit',
        },
        'kappa': {
            'func': lambda k0, k1, k2, pi: k0 + k1 * np.exp(k2 * pi),
            'com': 'Relative GDP investment through relative profit',
        },
        'inflation': {
            'func': lambda mu, eta, omega: eta*(mu*omega-1),
            'com': 'Markup dynamics',
        },
    },
    'parameter': {},
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
        'employment': 0.95,
        'omega': 0.90,
        'd': 2,
        'alpha': 0.02,
        'n': 0.025,
        'nu': 3,
        'delta': .005,
        'phinull': .04,
        'k0': -0.0065,
        'k1': np.exp(-5),
        'k2': 20,
        'r': 0.03, },
    'com': ' Default run'},
}
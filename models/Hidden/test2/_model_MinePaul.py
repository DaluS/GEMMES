# -*- coding: utf-8 -*-
"""
ABSTRACT : This is a mine-depleting model

TYPICAL BEHAVIOR :
LINKTOARTICLE :

@author: Paul Valcke
"""

import numpy as np


from pygemmes._models import Funcs


__r0 = 1000
_LOGICS = {
    'differential': {
        # COUPLING ODE
        'R': {
            'func': lambda Y, intensity: -Y*intensity,
            'com': 'Only removed by production',
            'initial': __r0*0.9,
            'units':'Units',
        },
    },
    'statevar': {
        'Quality': {
            'func': lambda R0, R, qRslope: np.log(R0/(R0-R))*(1/qRslope),
            'definition': 'quality of best resource',
            'com': 'exponential distribution',
            'units':'',
        },
        'nuMine': {
            'func': lambda nu0, Quality, a: nu0/(Quality*a),
            'com': 'impact of quality on production',
            'definition': 'return of capital of mining sector',
            'units':'y',
        },
        'Gamma': {
            'func': lambda Gamma0, a, Quality, Gammabase: Gammabase + Gamma0/(Quality*a),
            'definition': 'Generalised EROI (recipie)',
            'com': 'based on quality',
            'units': '',
        },

    },
    'parameter': {
        'intensity': {
            'value': 0.8,
            'definition': 'part of output which is material',
            'units': ''
        },
        'qRslope': {
            'value': 1,
            'definition': 'slope in resource quality concentration',
            'units': ''
        },
        'Gamma0': {
            'value': 0.01,
            'definition': 'Quality-dependent EROI contribution',
            'units': ''
        },
        'Gammabase':  {
            'value': 0.01,
            'definition': 'Quality-independent EROI contribution',
            'units': ''
        },
        'R0': {
            'value': __r0,
            'definition': 'initial quantity of ressources'},
        'nu0': {
            'value': 7,
            'definition': 'nu at snapshot'}
    },
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {'default': {
    'fields': {
    },
    'com': ' Default run'},
}
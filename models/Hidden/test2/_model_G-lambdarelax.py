# -*- coding: utf-8 -*-
"""
DESCRIPTION :

    This is a small modificaiton of Goodwin : the perception of employement in
    the Phillips curve has a slight relaxation of a time taulamb : typically it takes
    two years for employement to impact salary negocation

LINKTOARTICLE: Nothing has been published

Created on Wed Jul 21 15:11:15 2021
@author: Paul Valcke
"""
import numpy as np
from pygemmes._models import Funcs

# ----------------------------------------------------------------------------
# We simply do a few modifications on a previous model : we load it as a basis
from pygemmes._models._model_G import _LOGICS as _LOGICS0
from copy import deepcopy
_LOGICS = deepcopy(_LOGICS0)

# We add our modifications
# We use lambda0 as the previous lambda measure (it is the instant employement felt)
_LOGICS['statevar']['lamb0'] = Funcs.Definitions.lamb

# We remove lambda from statevar as there is now inertia in it, We place it in 'ode'
_LOGICS['statevar'].pop('lambda', None)
_LOGICS['ode']['lambda'] = Funcs.Phillips.lambdarelax


_LOGICS['param']['taulamb'] = {'value': 1/2,
                               'definition': 'typical time for employement to impact salary nego'}

# ----------------------------------------------------------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'taulamb': {
        'fields': {
            'dt': 0.01,
            'Tmax': 10,
            'a': 1,
            'N': 1,
            'K': 2.7,
            'D': 0,
            'w': .5*1.2,
            'lambda': 0.9,
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
            'taulamb': 0.5,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'plotnyaxis': [{'x': 'time',
                           'y': [['lambda', 'lamb0'],
                                 ['omega'],
                                 ],
                            'idx':0,
                            'title':'',
                            'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            'plot3D': [{'x': 'lamb0',
                        'y': 'omega',
                        'z': 'lambda',
                        'cinf': 'time',
                        'cmap': 'jet',
                        'index': 0,
                        'title': ''}],
            'plotbyunits': [],
        },
    },
}
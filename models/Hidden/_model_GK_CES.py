"""Goodwin-Keen CES model"""
# ################ IMPORTS ##################################################

from chimes.libraries import Funcs, importmodel, merge_model, fill_dimensions
import numpy as np  # (if you need exponential, pi, log, of matrix products...)
from chimes.libraries import Operators as O
_DESCRIPTION = """
* **Article :** Batisdas []
* **Author  :** []
* **Coder   :** Paul Valcke

This is a small modificaiton of Goodwin : the Leontiev optimised function has been
replaced by a CES (its generalisation).
It closes the phase-space on omeg

"""

_LOGICS_GK, _PRESETS0, _SUPPLEMENTS = importmodel('GK')

# We write the fields we want to add/modify
_LOGICS_CES = {
    'statevar': {
        # Characteristics of a CES
        'cesLcarac': Funcs.ProductionWorkers.cesLcarac,
        'cesYcarac': Funcs.ProductionWorkers.cesYcarac,
        'omegacarac': Funcs.ProductionWorkers.omegacarac,

        # From it are deduced optimised quantities
        'nu': Funcs.ProductionWorkers.CES_Optimisednu,
        'l': Funcs.ProductionWorkers.CES_Optimisedl,

        # From it are deduced Labor and Output
        'Y': Funcs.ProductionWorkers.CES_OptimisedY,
        'L': Funcs.ProductionWorkers.CES_OptimisedL,
    },
}

_LOGICS = merge_model(_LOGICS_GK, _LOGICS_CES, verb=False)

# ---------------------------
# List of presets for specific interesting simulations
_PRESETS = {
    'CES': {
        'fields': {
            'dt': 0.01,
            'Tsim': 100,

            'a': 1,
            'N': 1,
            'K': 2.75,
            'D': 0,
            'w': .80,

            'alpha': 0.02,
            'n': 0.025,
            'delta': .005,
            'phinull': 0.1,

            'CESexp': 1000,
            'A': 1 / 3,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['employment', 'lamb0'],
                              ['omega'],
                              ],
                        'idx': 0,
                        'title': '',
                        'lw': 1}],
            'XY': [{'x': 'employment',
                    'y': 'omega',
                    'color': 'time',
                    'idx': 0}],
            '3D': [{'x': 'lamb0',
                    'y': 'omega',
                    'z': 'employment',
                    'cinf': 'time',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [],
        },
    },
}

# -*- coding: utf-8 -*-
"""
This is a basic Goodwin model :
    * Two sectors
    * Exogenous technical progress, exogenous population
    * Capital accumulation through investment of profits
    * Consumption through salary
    * Salary-Profit through Philips curve
    * No money, no inflation
    * No loan possibility

The interesting things :
    * growth is an emergent property
    * Economic cycles (on employment and wage share) are an emergent property
    * trajectories are closed in the phasespace (lambda, omega) employment - wageshare

Link : https://en.wikipedia.org/wiki/Goodwin_model_(economics) (notations differs)


@author: Paul Valcke
"""

from pygemmes._models import Funcs

# ---------------------------
# user-defined model
# contains parameters and functions of various types
_LOGICS = {
    'differential': {
        # Exogenous entries in the model
        'a': Funcs.Productivity.exogenous,
        'N': Funcs.Population.exp,

        # Stock-flow consistency
        'K': Funcs.Kappa.kfromIr,

        # Price Dynamics
        'w': {
            'func': lambda phillips, w,pi : w * phillips,
            'com': 'Phillips impact (no negociation)'
        }
    },

    # Intermediary relevant functions
    'statevar': {
        # Production function and its employement
        'Y': Funcs.ProductionWorkers.Leontiev_Optimised.Y,
        'L': Funcs.ProductionWorkers.Leontiev_Optimised.L,

        # Parametric behavior functions
        'phillips': Funcs.Phillips.div,
        'I': Funcs.Kappa.ifromnobank,
        'Ir': Funcs.Kappa.irfromI,

        # Intermediary variables with their definitions
        'pi': Funcs.Definitions.pi,
        'employment': Funcs.Definitions.employment,
        'omega': Funcs.Definitions.omega,
        'GDP': Funcs.Definitions.GDPmonosec,

        # Costs per unit produced
        'c': Funcs.Inflation.costonlylabor,

        # Stock-Flow consistency
        'Pi': {
            'func': lambda GDP, w, L, r, D: GDP - w * L,
            'com': 'Profit for production-Salary', },

        # Auxilliary for practical purpose
        'g': {
            'func': lambda I, K, delta: (I - K * delta)/K,
            'com': 'relative growth rate'},
    },
    'parameter': {},
    'size': {},
}


# ---------------------------
# List of presets for specific interesting simulations

_PRESETS = {
    'default': {
        'fields': {
            'dt': 0.011,
            'a': 1.01,
            'N': 1.01,
            'K': 2.91,
            'D': 0.01,
            'w': .5*1.19,
            'alpha': 0.021,
            'n': 0.0251,
            'nu': 31,
            'delta': .0051,
            'phinull': 0.11,
        },
        'com': (
            'This is a run that should give simple '
            'convergent oscillations'),
        'plots': {
            'timetrace': [{}],
            'nyaxis': [{'x': 'time',
                        'y': [['lambda', 'omega'],
                              ['K'],
                              ],
                        'idx':0,
                        'title':'',
                        'lw':1}],
            'phasespace': [{'x': 'lambda',
                            'y': 'omega',
                            'color': 'time',
                            'idx': 0}],
            '3D': [{'x': 'lambda',
                    'y': 'omega',
                    'z': 'time',
                    'cinf': 'pi',
                    'cmap': 'jet',
                    'index': 0,
                    'title': ''}],
            'byunits': [],
        },
    },
    'many-orbits': {
        'fields': {
            'dt': 0.01,
            'a': 1,
            'N': 1,
            'K': 2.9,
            'D': 0,
            'w': [.5, .5*1.2, .5*1.3, .5*1.5, .5*1.7],
            'alpha': 0.02,
            'n': 0.025,
            'nu': 3,
            'delta': .005,
            'phinull': 0.1,
        },
        'com': (
            'Shows many trajectories'),
        'plots': {
            'timetrace': [{'keys': ['lambda', 'omega']}],
            'nyaxis': [],
            'phasespace': [{'x': 'lambda',
                           'y': 'omega',
                            'idx': 0}],
            '3D': [],
            'byunits': [],
        },
    },
}
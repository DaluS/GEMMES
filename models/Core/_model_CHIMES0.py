'''Numerical core for multisectoral models'''

_DESCRIPTION = """
# **E**CONOMIC **C**ORE for **H**OLISTIC **I**NTERDISCIPLINARY **M**ODEL assessing **E**COLOGICAL **S**USTAINABILITY
* **Article :** https://www.overleaf.com/project/62fbdce83176c9784e52236c    
* **Author  :** Paul Valcke
* **Coder   :** Paul Valcke

## Description
The goal of **E-CHIMES** is:
* description of production with physical variables
* behavior of agents (price, investment) based on economic values
* Connexion to ecological systems through physical coupling (emissions, land use...)

It integrates :
* Nprod productive sector, by activity
* Material flow analysis integrated inside
* Loans dynamics for investment and cross-sector expanses
* Inventory fluctuations
* Inflation
* Adaptive use of capital

## What should be done ?
* Check u and i mechanism
"""
from pygemmes._models import Funcs, importmodel,mergemodel
from pygemmes._models import Operators as O
import numpy as np

def dotD( MtransactI, MtransactY, wL, rD, pC):
    return rD \
         + wL -pC \
         + O.ssum2(MtransactI - O.transpose(MtransactI)) \
         + O.ssum2(MtransactY - O.transpose(MtransactY))

_LOGICS = {
    'size': {
        'Nprod': {
            'list': ['MONO'],
        },
    },
    ###################################################################
    'differential': {
        ### MONETARY STOCK-FLOW CONSISTENCY
        'D': {
            'func': lambda dotD: dotD,
            'com': 'no shareholding',
            'definition': 'Debt of local sector',
            'units': '$',
            'size': ['Nprod'],
        },
        'Dh': {
            'func': lambda W, p, C: -W + O.sprod(p, C),
            'com': '',
            'definition': 'debt of households',
            'units': '$',
            'symbol': r'$D_{household}$'
        },

        ### PHYSICAL STOCK-FLOW CONSISTENCY
        'V': {
            'func': lambda dotV: dotV,
            'com': 'dynamics in dotV',
            'size': ['Nprod'],
            'units': 'units',
            'symbol': '$V$'
        },
        'K': {
            'func': lambda Ir, delta, K: Ir - delta * K,
            'com': 'depreciation proportional to u',
            'definition': 'Productive capital in physical units',
            'units': 'units',
            'size': ['Nprod'],
            'initial': 2.7,
        },

        ### PRICES
        'p': {
            'func': lambda p, inflation: p * inflation,
            'com': 'log on markup',
            'size': ['Nprod'],
            'units': '$.Units^{-1}',
        },
        'w0': {'func': lambda Phillips, w0, gammai, ibasket: w0 * (Phillips + gammai * ibasket),
              'com': 'exogenous',
               'definition': 'Wage caracteristic level',
               'units':'$.Humans^{-1}.y^{-1}',
               'initial':0.75,
              },

        ### BEHAVIOR
        'u0': {
            # 'func': lambda u: 0,
            'func': lambda u0, sigma, V, dotV: -sigma * (1 - u0) * (dotV / V),
            #'func': lambda u0, sigma, Y, dotV: -sigma * (1 - u0) * (dotV / Y),
            #'func': lambda u0, sigma, v0: -sigma * (1 - u0) * (1-1/v0),
            'com': 'commanding inventory',
            'definition': 'voluntary use of productive capital',
            'units': '',
            'size': ['Nprod'],
            'initial': 1,
        },

        ### EXOGENOUS SCALING
        'a0': {'func': lambda a0, alpha: a0 * alpha,
              'com': 'exogenous',
               'initial':1,
              },
        'N': {'func': lambda N, n: N * n,
              'com': 'exogenous',
              },
    },
    'statevar': {
        ### BY-SECTOR PRODUCTIVITY AND WAGE
        'w': {'func': lambda w0,z: w0*z,
              'com': 'Sector-adjusted wage',
              'size':['Nprod']},
        'a': {'func': lambda a0, b,nu,u : u*a0*b/nu,
              'com': 'Sector-adjusted productivity',
              'size':['Nprod']},

        ### USE AND ACCESSIBILITY
        'u': {'func': lambda u0: u0,
              'com': 'for the moment only voluntary limitation',
              'definition': 'Effective use of capital',
              'size': ['Nprod']},
        'nu': {'func': lambda nu0, u: nu0/u,
               'com': 'Adjusted by use of capital',
               'size': ['Nprod']},

        ### COST COMPONENTS
        'omega': {
            'func': lambda a, w, p:  w / (p* a),
            'com': 'By definition',
            'units': '',
            'size': ['Nprod'],
        },
        'Mgamma': {
            'func': lambda Gamma,p : Gamma*O.transpose(p)/p,
            'definition': 'weight of intermediate consumption from j',
            'units': '',
            'com': 'Matrix version',
            'symbol': r'$\gamma$',
            'size': ['Nprod','Nprod'],
        },
        'Mxi': {
            'func': lambda Xi, p,nu,delta: nu*delta*Xi * O.transpose(p) / p,
            'definition': 'weight of capital destruction from j',
            'units': '',
            'com': 'Matrix version',
            'symbol': r'$\xi$',
            'size': ['Nprod', 'Nprod'],
        },

        'c': {
            'func': lambda omega, Mgamma, Mxi, p: p * (omega + O.ssum2(Mgamma) + O.ssum2(Mxi)),
            'com': 'sum of components',
            'size': ['Nprod'],
            'units': '$.Units^{-1}',
        },

        ### Inflations
        'inflation': {
            'func': lambda inflationMarkup,inflationdotV: inflationMarkup+inflationdotV,
            'com': 'sum of inflation contributions',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': '$i$'
        },
        'inflationMarkup': {
            'func': lambda p, eta, mu0, c,: eta * np.log(mu0 * c / p),
            'com': 'log on markup',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': '$i^{\mu}$'
        },
        'inflationdotV': {
            'func': lambda chi, dotV, V: - chi *( dotV / V),
            'com': 'price adjustment to demand-offer on Y',
            'size': ['Nprod'],
            'units': 'y^{-1}',
            'symbol': '$i^{\dot{V}}$'
        },
        'basket': {
            'func': lambda p, C: p * C / O.sprod(p, C),
            'com': 'cannot be non-auxilliary',
            'definition': 'weight in consumption basket',
            'size': ['Nprod'],
            'units': '',
        },
        'ibasket': {
            'func': lambda inflation, basket: O.sprod(inflation, basket),
            'com': 'deduced from the basket',
            'definition': 'basket of good inflation',
            'units': 'y^{-1}',
            'symbol': r'$i_{Basket}$',
        },

        'L': {'func': lambda Y,a : Y/a,
              'com': 'logics in a',
              'size': ['Nprod'],
              },

        ### PHYSICAL FLUXES
        'Y': {'func': lambda nu, K: K / nu,
              'com': 'logics in nu',
              'size': ['Nprod'],
              },
        'Ir': {
            'func': lambda I,Xi,p: I/O.matmul(Xi,p),
            'com': 'deduced from monetary investment',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },
        'C': {
            'func': lambda W,Cpond,p: Cpond*W/p,
            'com': 'Consumption as full salary',
            'definition': 'flux of goods for household',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
        },
        'dotV': { 'func': lambda Y, Gamma, Ir, C, Xi: Y - O.matmul(O.transpose(Gamma), Y) - C - O.matmul(O.transpose(Xi), Ir),
            'com': 'stock-flow',
            'definition': 'temporal variation of inventory',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$\dot{V}$'
        },
        'deltaK': {
            'func': lambda K,delta : delta*K, 
            'com' : 'constant degradation',
            'definition': 'physical degraded of capital',
            'units': 'Units.y^{-1}',
            'size': ['Nprod'],
            'symbol': r'$(delta K)$'
        },
        
        # Matrix approach
        'Minter': {
            'func': lambda Y, Gamma: O.transpose(Gamma*Y) ,
            'definition': 'Physical from i to j through intermediary consumption',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$^\mathcal{R}\mathcal{M}^Y$'
        },
        'Minvest': {
            'func': lambda Ir, Xi:  O.transpose(Xi* Ir),
            'definition': 'Physical from i to j through investment',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'$^\mathcal{R}\mathcal{M}^{I}$'
        },
        'MtransactY': {
            'func': lambda p, Y, Gamma: Y * Gamma * O.transpose(p),
            'definition': 'Money from i to j through intermediary consumption',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'($^{\$}\mathcal{M}^{Y})$'
        },
        'MtransactI': {
            'func': lambda I, Xi, p: I * Xi * O.transpose(p) / (O.matmul(Xi, p)),
            'definition': 'Money from i to j through investment',
            'com': 'matrix expansion',
            'units': '$.y^{-1}',
            'size': ['Nprod', 'Nprod'],
            'symbol': r'($^{\$}\mathcal{M}^{I})$'
        },

        ### MONETARY FLUXES
        'wL': {
            'func': lambda w,L : w*L,
            'com': 'wage bill per sector',
            'definition': 'wage bill per sector',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'pC': {
            'func': lambda p,C: p *C,
            'com': 'explicit monetary flux',
            'definition': 'monetary consumption',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'I': {
            'func': lambda p, Y, kappa, Mxi: p * Y * (kappa + O.ssum2(Mxi)),
            'com': 'explicit monetary flux',
            'definition': 'monetary investment',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },

        'rD': {
            'func': lambda r,D: r*D,
            'com': 'explicit monetary flux',
            'definition': 'debt interests',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
        },
        'dotD': {
            'func': dotD,
            'com': 'explicit monetary flux',
            'definition': 'debt variation',
            'units': '$.y^{-1}',
            'size': ['Nprod'],
            'symbol':'$\dot{D}$',
        },

        ### LABOR-SIDE THEORY
        'W': {
            'func': lambda w, L, r, Dh: O.sprod(w, L) - r * Dh,
            'definition': 'Total income of household',
            'com': 'no shareholding, no bank possession',
            'units': '$.y^{-1}',
            'symbol': r'$\mathcal{W}$'
        },
        'rDh':{
            'func': lambda r,Dh : r*Dh,
            'definition': 'bank interests for household',
            'units': '$.y^{-1}',
        },
        'employmentAGG': {
            'func': lambda employment: O.ssum(employment),
            'com': 'Calculation with L',
            'units': '',
            'symbol': r'$\Lambda$'
        },
        'Phillips': {
            #'func': lambda employmentAGG, phi0, phi1: -phi0 + phi1 / (1 - employmentAGG) ** 2,
            'func': lambda employmentAGG, philinConst, philinSlope: philinConst + philinSlope * employmentAGG,
            'com': 'Local Phillips',
            'units': 'y^{-1}',
            'symbol': r'$\Phi(\lambda)$',
        },

        ### PROFITS AND INVESTMENTS
        'kappa': {
            'func': lambda pi, k0: k0 * pi,
            'com': 'LINEAR KAPPA FUNCTION',
            'units': '',
            'size': ['Nprod'],
        },
        'pi': {
            'func': lambda omega, Mgamma, Mxi, r, D, p, Y: 1 - omega - O.ssum2(Mgamma) - O.ssum2(Mxi) - r * D / (p * Y),
            'com': 'explicit form',
            'size': ['Nprod'],
            'units': '',
        },
        'rd': {'func': lambda r,D,p,Y : r*D/(p*Y),
               'com': 'explicit form',
               'definition': 'relative weight debt',
               'size': ['Nprod'],
               'units': ''},
        ################################################
        'gK': {
            'func': lambda Ir,K,delta : Ir/K - delta ,
            'definition': 'growth rate',
            'com': 'raw definition',
            'symbol': r'$g^K $',
            'size': ['Nprod'],
            'units': 'y^{-1}',
        },
        'ROC': {
            'func': lambda pi, nu,Xi,p: pi/(nu*O.matmul(Xi,p)/p),
            'definition': 'return on capital',
            'com': 'raw definition',
            'size': ['Nprod'],
            'units': 'y^{-1}',
        },
        'employment': {
            'func': lambda L,N: L/N,
            'com': 'Calculation with L',
            'units': '',
            'size': ['Nprod'],
            'symbol': r'$\lambda$'
        },
        'gamma': {
            'func': lambda Gamma, p: O.matmul(Gamma, p) / p,
            'definition': 'share of intermediary consumption',
            'com': 'raw definition',
            'units': '',
            'symbol': r'$\gamma$',
            'size': ['Nprod'],
        },
        'xi': {
            'func': lambda delta, nu, b, p, Xi: (delta * nu / b) * O.matmul(Xi, p) / p,
            'definition': 'relative capex weight',
            'com': 'explicit calculation',
            'units': '',
            'size': ['Nprod'],
            'symbol': r'$\xi$',
        },
        'reldotv': {
            'func': lambda dotV, Y, p, c: (c - p) * dotV / (p * Y),
            'com': 'calculated as inventorycost on production',
            'definition': 'relative budget weight of inventory change',
            'units': '',
            'size': ['Nprod'],
            'symbol': r'$\dot{v}$',
        },
        'reloverinvest': {
            'func': lambda kappa, pi: pi - kappa,
            'com': 'difference between kappa and pi',
            'units': '',
            'symbol': r'$(\kappa-\pi)$',
            'size': ['Nprod'],
            'definition': 'relative overinstment of the budget',
        },
    },
    'parameter': {
        ### SCALARS
        'alpha'  :{'value': 0.02,},
        'n'      :{'value': 0.025,},
        'phinull':{'value': 0.1,},
        'r'      :{'value': 0.03, },

        ### VECTORS
        'z': {'value':1,
              'definition': 'local wage ponderation',
              'size': ['Nprod']
              },
        'b': {'value':1,
                'definition': 'local productivity ponderation',
                'size':['Nprod']
                },
        'nu0': {'value':3,
                'definition': 'characteristic capital-to-output',
                'size':['Nprod']
                },
        'Cpond': {'value': .5,
              'definition': 'part of salary into consumption of the product',
              'size': ['Nprod']
              },
        'mu0': {'value': 1.3,
              'definition': '',
              'size': ['Nprod']
              },
        'delta': {'value': 0.005,
                  'size': ['Nprod']
                  },
        'deltah': {'value': 0.1,
                  'size': ['Nprod']
                  },
        'sigma': {'value': 1,
                  'size': ['Nprod']
                  },
        'gammai': {'value': 1,
                  },
        'eta': {'value': 0.5,
               'size': ['Nprod']
               },
        'chi': {'value': 1.5,
               'size': ['Nprod']
               },
        'b': {'value': 1,
              'size': ['Nprod']
              },
        'nu': {'value': 3,
               'size': ['Nprod']
               },

        ### MATRICES
        'Gamma': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod'],
            'units':'',
        },
        'Xi': {
            'value': 0.01,
            'size': ['Nprod', 'Nprod']
        },
    },
}

############################ SUPPLEMENTS ################################################
'''
Specific parts of code that are accessible
'''
def funcs(test):
    print(test)

_SUPPLEMENTS= {'Test':funcs}



############################ PRESETS #####################################################

dictMONOGOODWIN={
# Numerical structural
'Tmax'  : 50,
'Nprod' : ['Mono'],
'Tini'  : 0,

# Population
'n'     : 0.025, # MONOSECT
'N'     : 1    , # MONOSECT

# PRODUCTION-MATERIAL FLUXES #######
'K'    : 2.7,
'Gamma': 0.05,
'Xi'   : 1,
'nu'   : 3,
'delta': 0.05,
'b'    : 3,
'a0'    : 1, # MONOSECT
'alpha': 0.02, # MONOSECT
'u'    : 1,

# Inventory-related dynamics
'V'     : 1,
'sigma' : 0,  # use variation
'chi'   : 0,  # inflation variation

# investment
'k0': 1.,

# Debt-related
'Dh'    : 0, # MONOSECT
'D'     : [0],
'r'     : 0.03, # MONOSECT

# Wages-prices
'w0'     : 0.6, # MONOSECT
'p'     : 1,
'z'     : 1,
'mu0'   : 1.3,
'eta'   : 0.0,
'gammai': 0, # MONOSECT
'phinull':0.1, # MONOSECT

# Consumption theory
'Cpond' : [1],
}

preset_basis = {
'Tmax':50,
'dt':0.1,
'Nprod': ['Consumption','Capital'],
'nx':1,

'alpha' : 0.02,
'n'     : 0.025,
'phinull':0.1,

'gammai':0,
'r':0.03,
'a':1,
'N':1,
'Dh':0,
'w':0.8,

'sigma':[1,5],
'K': [2.,0.5],
'D':[0,0],
'u':[.95,.7],
'p':[1.5,3],
'V':[1,1],
'z':[1,.3],
'k0': 1.,

'Cpond':[1,0],

'mu0':[1.2,1.2],
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':[1,1],
'b':3,
'nu':3,

## MATRICES
'Gamma': [[0.05 ,0],
          [0    ,0]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
'Xi': [[0.01,1],
       [0.1,1]],
'rho': np.eye(2),
}

preset_basis2=preset_basis.copy()
preset_basis2['K'] = [2.3,0.5]
preset_basis2['u'] = [1,1]
preset_basis2['p'] = [1,1]
preset_basis2['z'] = [1,1]
#preset_basis2['Tmax'] = 50


withregion = preset_basis2.copy()
withregion['nr']=['USA','France','China']

preset_TRI = {
'Tmax':50,
'dt':0.1,
'Nprod': ['Consumption','Intermediate','Capital'],
'nx':1,

'alpha' : 0.02,
'n'     : 0.025,
'phinull':0.1,

'gammai':0,
'r':0.03,
'a':1,
'N':1,
'Dh':0,
'w':0.8,

'sigma':[1,5,5],
'K': [2.1,0.4,0.4],
'D':[0,0,0],
'u':[.95,.95,.95],
'p':[1,1,1],
'V':[1,1,1],
'z':1,
'k0': 1.,
'Cpond':[1,0,0],
'mu0':1.2,
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':1,
'b':3,
'nu':3,

## MATRICES
'Gamma': [[0.0,0.1 ,0],
          [0  ,0.1 ,0],
          [0.0,0.1 ,0]],
#'Xi': [['Consumption','Capital','Consumption','Capital'],
#       ['Consumption','Capital','Capital','Consumption'],[0,.5,1,0]],
'Xi': [[0.0,0,1],
       [0.0,0,1],
       [0.0,0,1]],
'rho': np.eye(3),
}

Nsect=4
#A=np.diag([0.1 for i in range(Nsect-1)],1)
#A[Nsect-2,Nsect-1]=0

A=np.diag([0.1 for i in range(Nsect-1)],-1)
A[Nsect-1,Nsect-2]=0

preset_N = {
'Tmax':8,
'dt':0.1,
'Nprod': ['Consumption']+['Inter'+str(i) for i in range(Nsect-2)]+['Capital'],
'nx':1,

'alpha' : 0.02,
'n'     : 0.025,
'phinull':0.1,

'gammai':0,
'r':0.03,
'a':1,
'N':4,
'Dh':0,
'w':0.8,

'sigma':5,
'K': [4]+[0.4 for i in range(Nsect-2)]+[5],
'D':0,
'u':.95,
'p':1,
'V':1,
'z':1,
'k0': 1.,
'Cpond':[1]+[0 for i in range(Nsect-1)],
'mu0':1.3,
'delta':0.05,
'deltah':0.05,
'eta':0.3,
'chi':1,
'b':3,
'nu':3,

## MATRICES
'Gamma': A,
'Xi':    [[0 for j in range(Nsect-1)]+[1] for i in range(Nsect)],
'rho': np.eye(Nsect),
}

########################################################################################
_PRESETS = {
    'Goodwin': {
        'fields': dictMONOGOODWIN,
        'com': ('A monosectoral system that behaves just as a Goodwin'),
        'plots': {},
    },
    'Bisectoral': {
        'fields': preset_basis,
        'com': ('Two sectors : one producing consumption good, one for capital goods.'
                'Converging run starting for VERY far from equilibrium'),
        'plots': {},
    },
    'SimpleBi': {
        'fields': preset_basis2, 
        'com': ('Two sectors : one producing consumption good, one for capital goods.'
                'Converging run starting close to equilibrium'),
        'plots': {},
    },
    'SimpleTri': {
        'fields': preset_TRI,
        'com': 'Trisectoral',
        'plots': {},
    },
    'WithRegions': {
        'fields': withregion,
        'com': 'more dimensions',
        'plots': {},
    },
    'SimpleN': {
        'fields': preset_N,
        'com': ('Two sectors : one producing consumption good, one for capital goods.'
                'Converging run starting close to equilibrium'),
        'plots': {},
    },
}
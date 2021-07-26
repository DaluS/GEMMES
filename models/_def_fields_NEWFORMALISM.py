# -*- coding: utf-8 -*-
"""
This file contains the default fields (units, dimension, symbol...) for all
common parameters / variables that can be used by any model.

It can be used a common database where all default fields attached to each
parameter / variable are stored

Users can decide to replace some fields when they define their model, but all
fields which are not explicitly described by the user / modeller in the model
will be taken from this default database

"""

import numpy as np  
import itertools 

_LIBRARY = { 
    
    'Numerical' : {
        'Tmax' : {
            'value' : 100,
            'units' : 'y',
            'com' : 'Total simulated time',
            },
        'dt' : {
            'value' : 0.01,
            'units' : 'y',
            'com' : 'time between two steps',
            },
        'nt' : {
            'func': lambda Tmax=0, dt=1: int(Tmax / dt),
            'units' : None,
            'com' : 'Total simulated time',
            },
        'nx' : {
            'value' : 100,
            'units' : 'y',
            'com' : 'Total simulated time',
            },
        'time': {
            'value' : 0,
            'ode' : lambda dt=0: 1.,
            'com': 'Time vector',
            'units': 'y',
            },
        },
    
    'CORE' : {
        # Population    
        'N': {
            'value': 1.,
            'com': 'Exogenous population as an exponential',
            'units': 'humans'
            },
        'beta': {
            'value': 0.025,
            'com': 'Rate of population growth',
            'units': 'y^{-1}',   
            },
        
        # Productivity
        'a': {
            'value': 1,
            'units': 'Units.Humans^{-1}.years^{-1}',
            'com': 'Exogenous technical progress as an exponential',
        },        
        'alpha': {
            'value': 0.02,
            'com': 'Rate of productivity increase',
            'units': 'y^{-1}',
            },    
        'W': {
            'value': 0.85,
            'com': 'Wage value',
            'units': 'Dollars'
        },

        
        # Capital
        'delta': {
            'value': 0.005,
            'com': 'Rate of capital depletion',
            'units': 'y^{-1}',
            },
        'nu': {
            'value': 3,
            'com': 'Kapital to output ratio',   
            'units': None,
            },
        'K': {
            'value': 2.7,
            'units':'Units',
            'com': 'Capital evolution from investment and depreciation',
        },        
        
        
       'pi': {
            'value': None,
            'com': 'relative profit',
            'units': '',
            'symbol': r'$\pi$',
            },
        'g': {
            'value': None,
            'com': 'Relative growth',
            'units': 'y^{-1}',
            },       
        'Y': {
            'value': None,
            'com': 'GDP in output quantity',
            'units': 'Units.years^{-1}',
            },
        'L': {
            'value': None,
            'com': 'Workers',
            'units': 'Humans',
            },
        'I': {
            'value': None,
            'com': 'Investment',
            'units': 'Dollars',
            },    
        'Pi': {
            'value': None,
            'com': 'Absolute profit',
            'units': 'Dollars',
            },
        },

    'Salary Negociation':{
        'phillips': {
            'value': None,
            'com': 'Wage inflation rate',
            'units': 'y^{-1}',
            'symbol': r'$\phi$',
            },
        'phinull': {
            'value' : 0.04,
            'com': 'Unemployment rate with no salary increase',
            'units': None,
            },
        'phi0': {
            'func': lambda phinull=0: phinull / (1 - phinull**2),
            'com': '',
            'units': None,
            },
        'phi1': {
            'func': lambda phinull=0: phinull**3 / (1 - phinull**2),
            'com': '',
            'units': None,
            },
        },
                
   'Investment': {
        'kappa': {
            'value': None,
            'com': 'Part of GDP in investment',
            'units': '',
            'symbol': r'$\kappa$',
        },    
       'k0': {
           'value': -0.0065,
           'com': 'Percent of GDP invested when profit is zero',
           'units': None,
        },
        'k1': {
            'value': np.exp(-5),
            'com': 'Investment slope',
            'units': None,
        },
        'k2': {
            'value': 20,
            'com': 'Investment power in kappa',
            'units': None,
        },
    },
   
    'Debt' : { 
        'r': {
            'value': .03,
            'com': 'Interest at the bank',
            'units': 'y^{-1}',
        },
        'D': {
            'value': 0.1,
            'com': 'Debt as Investment-Profit difference',
            'units': 'Dollars',
        },
        'd': {
            #'func': lambda GDP=0, D=0: D/GDP,
            'value': 0.1,
            'com': 'relative debt',
            'units':''
        },
    },
    
    'Prices' : {
        'mu' : {
            'value' : 2 ,
            'com' : 'Markup on prices', 
            'units' : None,
            },
        'eta' : {
            'value' : 1 ,
            'com' : 'timerate of price adjustment',
            'units' : 'y^{-1}'},
        'GDP': {          
            'value': None,
            'com': 'GDP in nominal term',
            'units': 'Dollars',
            },
        },
               
    'MISC' : {
        'Coucou' : {
            'value': 0,
            'com' : 'I am just a test',
            'units' :None,
            },
        },
    
}

_DEFAULTFIELDS = {'com':'',
                  'units':''}

def CHECK_FIELDS(dic):
    ''' 
    This function check the consistency for each definition 
    * Unity of value declaration
    * Consistency of the field declared 
    '''
    
    Errormessage = ''
    Warningmessage = ''
    
    # 1) ### CHECK THAT NO FIELD DEFINITION ARE AT TWO PLACES 
    listoflistofkeys = [[ keys2 for keys2 in dic[keys1].keys()] 
                                for keys1 in dic.keys()        ]
    listofkeys =  list(itertools.chain(*listoflistofkeys))
    duplicates = set([x for x in listofkeys if listofkeys.count(x) > 1])
    
    if len(duplicates) > 0 : 
        msg= "keys defined in multiple groups !"+str(duplicates)
        Errormessage+=msg+'\n'
        
    # 2) ### CHECK THAT THE BEHAVIOR FIELDS ARE CONSISTENT
    for group in dic.keys() : 
        for field in dic[group].keys() :
            subject = dic[group][field]
            
            # We want that either : 
                # there is function and no value 
                # there is an ode and and a value 
                # there is a value and nothing else 
            if ( 'func' in subject.keys() and 'value' in subject.keys() ):  
                msg = str(field)+' in '+str(group)+' have both function and value'
                Errormessage+=msg+'\n'
            elif ( 'ode' in subject.keys() and not 'value' in subject.keys() ):
                msg = str(field)+' in '+str(group)+' is an ODE with no initial condition'
                Errormessage+=msg+'\n'
            elif ( 'func' not in subject.keys() and 'value' not in subject.keys() ): 
                msg = str(field)+' in '+str(group)+' is a parameter with no value'
                Errormessage+=msg+'\n'
                
            # We can also check if there are comments and units fields
            if 'com' not in subject.keys(): 
                msg = str(field)+' in '+str(group)+' has no comment'
                Warningmessage+=msg+'\n'
            if 'units' not in subject.keys():    
                msg = str(field)+' in '+str(group)+' has no unit'
                Warningmessage+=msg+'\n'
        # Check that all fields are well located 
        #print(group, len(dic[group].keys()))
        if (group=='MISC' and len(dic[group].keys())>0):
            msg ='MISC group contains field that should be classified'          
                    
                
    if len(Warningmessage) :
        raise Warning(Warningmessage)
    if len(Errormessage):
        raise ValueError(Errormessage)                

def from_Library_to_DFIELDS(lib,_DEFAULTFIELDS,_DFIELDS={}):
    print(_DFIELDS)
    
    '''
    allow the _Library to be compatible with _DFIELDS
    (with minimal work needed on ode etc)
    '''
    for group in lib.keys() : 
        for field in lib[group].keys() :
               subject = lib[group][field] 
               if ( 'func' in subject.keys()):  
                   _DFIELDS[field]= { 
                       'value' : subject['func'],
                       'com'   : subject.get('com',_DEFAULTFIELDS['com']),
                       'units' : subject.get('units',_DEFAULTFIELDS['units']),
                       'type'  : detectype(subject),
                       'dimension' : detectdimension(subject),
                       'symbol': subject.get('symbol',field), 
                       'group' : group,
                                   }                  
               elif ( 'ode' in subject.keys()):
                   _DFIELDS[field]= { 
                       'ode' : subject['ode'],
                       'initial': subject['value'],
                       'com'   : subject.get('com',_DEFAULTFIELDS['com']),
                       'units' : subject.get('units',_DEFAULTFIELDS['units']),
                       'type'  : detectype(subject),
                       'dimension' : detectdimension(subject),
                       'symbol': subject.get('symbol',field), 
                       'group' : group,
                                   }   
               else : 
                   _DFIELDS[field]= { 
                       'value' : subject['value'],
                       'com'   : subject.get('com',_DEFAULTFIELDS['com']),
                       'units' : subject.get('units',_DEFAULTFIELDS['units']),
                       'symbol': subject.get('symbol',field), 
                       'type'  : detectype(subject),
                       'dimension' : detectdimension(subject),
                       'group' : group,
                                   }                         
    return _DFIELDS

def detectype(subject):
    dims = detectdimension(subject)
    
    dimlist =[ keys for keys in dims.keys() if keys!='Muliplier']
    
    if len(dimlist)==0 : 
        return 'dimensionless'
    elif len(dimlist)==1 :
        if (dimlist[0] in ['y','humans','Units','Dollars'] and dims[dimlist]==1):
            return 'Extensive'
    else:
        return 'Intensive'
def detectdimension(subject):
    ''' This function takes the units and transform it into a dictionnary 
    of units '''
    dimensions={}
    infos = subject['units']
    
    # CUT THE STRING INTO SEPARATE ELEMENTS 
    if infos == None :
        dimensions['Multiplier']=1
    else :
        infos = infos.split(' ')
        
        # Identify if there is a multiplier
        if len(infos)==2:
            dimensions['Multiplier']=infos[0] 
            unitblock = infos[1]
        elif len(infos)==1:
            dimensions['Multiplier']=1
            unitblock = infos[0]
        elif len(infos)>2:
            raise ValueError('bad unit formalism, two spaces, in',subject)
            
        # Identify all the units 
        unitblock = unitblock.split('.')
        for units in unitblock :    
            # Identify their exponent 
            if units.endswith('}'):
                charplace = units.find('{')
                exponent= units[charplace+1:-1]
                charplace2 = units.find('^')
                dim = units[:charplace2].lower()
                dimensions[dim]=exponent 
            else :
                dimensions[units]=1  
                
    return dimensions

def print_fields(value=False,com=False,unit=False,group=False):
    print(60*'#')
    print('List of fields in the library')
    for key in _DFIELDS.keys(): 
        msg = key+(10-len(key))*' '
        if com : 
            msg +=' : '+_DFIELDS[key]['com']+(30-len(str(_DFIELDS[key]['com'])))*' '
        if unit :
            msg +=', unit :'+str(_DFIELDS[key]['units'])+(10-len(str(_DFIELDS[key]['units'])))*' '
        if group :
            msg +=', key :'+str(_DFIELDS[key]['group'])+(10-len(str(_DFIELDS[key]['group'])))*' '
        if (value and 'value' in _DFIELDS[key].keys() ): 
            msg +=', value :'+str(_DFIELDS[key]['value'])
        print(msg)
    print(60*'#')    
    
    
CHECK_FIELDS(_LIBRARY)
    
_DFIELDS=from_Library_to_DFIELDS(_LIBRARY,_DEFAULTFIELDS)
    


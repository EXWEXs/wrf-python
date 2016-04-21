from __future__ import (absolute_import, division, print_function, 
                        unicode_literals)

from .constants import Constants
from .extension import computetk, computeeth, computetv, computewetbulb
from .decorators import convert_units
from .metadecorators import copy_and_set_metadata
from .util import extract_vars

__all__ = ["get_theta", "get_temp", "get_eth", "get_tv", "get_tw",
           "get_tk", "get_tc"]

@copy_and_set_metadata(copy_varname="T", name="theta", 
                       description="potential temperature")
@convert_units("temp", "k")
def get_theta(wrfnc, timeidx=0, method="cat", squeeze=True, 
              cache=None, meta=True,
              units="k"):
    varnames = ("T",)
    
    ncvars = extract_vars(wrfnc, timeidx, varnames, method, squeeze, cache,
                          meta=False)
    t = ncvars["T"]
    full_t = t + Constants.T_BASE

    return full_t

@copy_and_set_metadata(copy_varname="T", name="temp", 
                       description="temperature")
@convert_units("temp", "k")
def get_temp(wrfnc, timeidx=0, method="cat", squeeze=True, 
             cache=None, meta=True,
             units="k"):
    """Return the temperature in Kelvin or Celsius"""
    
    varnames=("T", "P", "PB")
    ncvars = extract_vars(wrfnc, timeidx, varnames, method, squeeze, cache,
                          meta=False)
    t = ncvars["T"]
    p = ncvars["P"]
    pb = ncvars["PB"]
    
    full_t = t + Constants.T_BASE
    full_p = p + pb
    tk = computetk(full_p, full_t)
    
    return tk

@copy_and_set_metadata(copy_varname="T", name="theta_e", 
                       description="equivalent potential temperature")
@convert_units("temp", "k")
def get_eth(wrfnc, timeidx=0, method="cat", squeeze=True, 
            cache=None, meta=True,
            units="k"):
    "Return equivalent potential temperature (Theta-e) in Kelvin"
    
    varnames=("T", "P", "PB", "QVAPOR")
    ncvars = extract_vars(wrfnc, timeidx, varnames, method, squeeze, cache,
                          meta=False)
    t = ncvars["T"]
    p = ncvars["P"]
    pb = ncvars["PB"]
    qv = ncvars["QVAPOR"]
    
    full_t = t + Constants.T_BASE
    full_p = p + pb
    tk = computetk(full_p, full_t)
    
    eth = computeeth(qv, tk, full_p)
    
    return eth

@copy_and_set_metadata(copy_varname="T", name="tv", 
                       description="virtual temperature")
@convert_units("temp", "k")
def get_tv(wrfnc, timeidx=0, method="cat", squeeze=True, 
           cache=None, meta=True,
           units="k"):
    "Return the virtual temperature (tv) in Kelvin or Celsius"
    
    varnames=("T", "P", "PB", "QVAPOR")
    ncvars = extract_vars(wrfnc, timeidx, varnames, method, squeeze, cache,
                          meta=False)
    
    t = ncvars["T"]
    p = ncvars["P"]
    pb = ncvars["PB"]
    qv = ncvars["QVAPOR"]
    
    full_t = t + Constants.T_BASE
    full_p = p + pb
    tk = computetk(full_p, full_t)
    
    tv = computetv(tk,qv)
    
    return tv
    
@copy_and_set_metadata(copy_varname="T", name="twb", 
                       description="wetbulb temperature")
@convert_units("temp", "k")
def get_tw(wrfnc, timeidx=0, method="cat", squeeze=True, 
           cache=None, meta=True,
           units="k"):
    "Return the wetbulb temperature (tw)"
    
    varnames=("T", "P", "PB", "QVAPOR")
    ncvars = extract_vars(wrfnc, timeidx, varnames, method, squeeze, cache,
                          meta=False)
    t = ncvars["T"]
    p = ncvars["P"]
    pb = ncvars["PB"]
    qv = ncvars["QVAPOR"]
    
    full_t = t + Constants.T_BASE
    full_p = p + pb
    
    tk = computetk(full_p, full_t)
    tw = computewetbulb(full_p,tk,qv)
    
    return tw

def get_tk(wrfnc, timeidx=0, method="cat", squeeze=True, cache=None, 
           meta=True):
    return get_temp(wrfnc, timeidx, method, squeeze, cache, meta, units="k")

def get_tc(wrfnc, timeidx=0, method="cat", squeeze=True, cache=None,
           meta=True):
    return get_temp(wrfnc, timeidx, method, squeeze, cache, meta, units="c")
    
    


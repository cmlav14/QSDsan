#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 10:56:00 2021

@author: torimorgan
"""

import numpy as np
from warnings import warn
from qsdsan import SanUnit, Construction
from ._decay import Decay
from ..utils import load_data, data_path

__all__ = ('HousingReclaimer',)

data_path += 'sanunit_data/_housing_reclaimer.csv'



class HousingReclaimer(SanUnit, Decay):
    '''
    Cost and life cycle impacts of the housing for the Reclaimer 2.0
    
    '''
    
    #Assume no replacement as of now and no life cycle impacts for powder coating

    def __init__(self, ID='', ins=None, outs=(), thermo=None, init_with='WasteStream', 
                 **kwargs):
        SanUnit.__init__(self, ID, ins, outs, F_BM_default=1)


# load data from csv each name will be self.name    
        data = load_data(path=data_path)
        for para in data.index:
            value = float(data.loc[para]['expected'])
            setattr(self, para, value)
        del data
        
        for attr, value in kwargs.items():
            setattr(self, attr, value)
    def _run(self):
        waste = self.ins[0]
        treated = self.outs[0]
        treated.copy_like(self.ins[0])

    def _design(self):
        #find rough value for FRP for tank 
        design = self.design_results
        #!!! Add later design['Aluminum'] = aluminum_quant = self.aluminum_weight
        design['Steel'] = steel_quant = self.steel_weight
        self.construction = (
                            (Construction(item='Steel', quantity = steel_quant, quantity_unit = 'kg')))
        self.add_construction()
        
 
    def _cost(self):
        
        #purchase_costs is used for capital costs
        #can use quantities from above (e.g., self.design_results['StainlessSteel'])
        #can be broken down as specific items within purchase_costs or grouped (e.g., 'Misc. parts')
        self.baseline_purchase_costs['Housing'] = (self.frame + self.extrusion + self.angle_frame + 
                self.angle + self.door_sheet + self.plate_valve + self.powder)
        self._BM = dict.fromkeys(self.baseline_purchase_costs.keys(), 1)
        
        #certain parts need to be replaced based on an expected lifefime
        #the cost of these parts is considered along with the cost of the labor to replace them
        #rc_replacement_parts_annual_cost = (self.filter_replacement * self.filter_cost) # USD/yr only accounts for time running
        #self.add_OPEX =  (rc_replacement_parts_annual_cost) / (365 * 24) # USD/hr (all items are per hour)
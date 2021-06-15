#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Smiti Mittal <smitimittal@gmail.com>
    Yalin Li <zoe.yalin.li@gmail.com>
    Anna Kogler

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/master/LICENSE.txt
for license details.
'''

# %%
import math
#!!! Change this to relative importing when compiled into qsdsan
from qsdsan import Equipment, SanUnit, Component, WasteStream
# from .. import SanUnit, Equipment # relative importing

isinstance = isinstance

# __all__ = ('Electrode', 'ElectroChemCell')

# %%

# =============================================================================
# Then we can construct the unit with the different equipment
# =============================================================================

#!!! Note `Electrode` and `ElectroChemCell` has not been include in `qsdsan` now,
# so to actual run the example below, first run this script, then change
# `qs.sanunits.Electrode` to `Electrode` and `qs.sanunits.ElectroChemCell` to `ElectroChemCell`

class ElectroChemCell(SanUnit):

    '''
    
    Electrochemical cell for nutrient recovery.

    This unit has the following equipment:
        - :class:`Electrode`
        - :class: `Membrane`
        - :class: `Column`
        - :class: `Machine`

    Parameters
    ----------
    recovery : dict
        Keys refer to chemical component IDs. Values refer to recovery fractions (with 1 being 100%) for the respective chemicals.
    removal : dict
        Keys refer to chemical component IDs. Values refer to removal fractions (with 1 being 100%) for the respective chemicals.
    equipments : list
        List of Equipment objects part of the Electrochemical Cell.
    OPEX_over_CAPEX : float
        Ratio with which operating costs are calculated as a fraction of capital costs

    '''

    def __init__(self, ID='', ins=None, outs=(), recovery={'NH3':0.6}, removal={'NH3':0.2},
                 equipments=(), OPEX_over_CAPEX=0):
        if isinstance(equipments, Equipment):
            equipments = (equipments,)
        SanUnit.__init__(self=self, ID=ID, ins=ins, outs=outs, equipments=equipments)
        self.recovery = recovery
        self.removal = removal
        self.OPEX_over_CAPEX = OPEX_over_CAPEX

    _N_ins = 2
    _N_outs = 3

    def _run(self):
        influent, cleaner = self.ins
        recovered, removed, left = self.outs[0], self.outs[1], self.outs[2]

        mixture = WasteStream()
        mixture.mix_from(self.ins)
        left.copy_like(mixture)

        for chemical, ratio in self.recovery.items():
            recovered.imass[chemical] = mixture.imass[chemical]*ratio
            left.imass[chemical] = left.imass[chemical]-mixture.imass[chemical]*ratio

        for chemical, ratio in self.removal.items():
            removed.imass[chemical] = mixture.imass[chemical]*ratio
            left.imass[chemical] = left.imass[chemical]-mixture.imass[chemical]*ratio

    def _design(self):
        self.add_equipment_design()

    def _cost(self):
        self.add_equipment_cost()
        self.equip_costs = self.baseline_purchase_costs.values()
        add_OPEX = sum(self.equip_costs)*self.OPEX_over_CAPEX
        self._add_OPEX = {'Additional OPEX': add_OPEX}

print('classes compiled')

#sample code
# Set components
import qsdsan as qs
kwargs = dict(particle_size='Soluble',
              degradability='Undegradable',
              organic=False)
H2O = qs.Component.from_chemical('H2O', phase='l', **kwargs)
NH3 = qs.Component.from_chemical('NH3', phase='g', **kwargs)
NH3.particle_size = 'Dissolved gas'
NH4OH = qs.Component.from_chemical('NH4OH', phase='l', **kwargs)
H2SO4 = qs.Component.from_chemical('H2SO4', phase='l', **kwargs)
AmmoniumSulfate = qs.Component.from_chemical('AmmoniumSulfate', phase='l',
                                             **kwargs)
CleaningAgent = qs.Component('CleaningAgent', MW=1, phase='l', **kwargs)
cmps = qs.Components((H2O, NH3, NH4OH, H2SO4, AmmoniumSulfate, CleaningAgent))
# Assuming all has the same molar volume as water for demonstration purpose
for cmp in cmps:
    cmp.copy_models_from(H2O, names=['V'])
    cmp.default()
qs.set_thermo(cmps)
# Set waste streams
influent = qs.WasteStream('influent', H2O=1000, NH4OH=50)
cleaning_agent = qs.WasteStream('cleaning_agent', price=5)
# Set anode and cathode
anode = Electrode(name='anode', electrode_type='anode',
                              material='graphite', surface_area=10)
cathode = Electrode(name='cathode', electrode_type='cathode',
                                material='carbon', surface_area=10, unit_cost=1)
membrane = Membrane(name='membrane', N=2,
            material='polyethylene', unit_cost=0.2, surface_area=1)
column = Column(name='column1', N=3,
            material='resin', unit_cost=2, surface_area=20)
machine = Machine(name='fan', N=1, unit_cost=3)
# Set the unit
U1 = ElectroChemCell('U1', ins=(influent, cleaning_agent),
                                outs=('rec', 'rem', 'leftover'),
                                recovery={'NH4OH':0.6}, removal={'NH4OH':0.2},
                                equipments=(anode, cathode, membrane, column, machine), OPEX_over_CAPEX = 0.2)
# Simulate and look at the results
U1.simulate()
U1.diagram()
U1.show()
U1.results()

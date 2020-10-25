#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 16:52:05 2020

@author: yalinli_cabbi, joy_c
"""

import os
os.chdir("C:/Users/joy_c/Dropbox/PhD/Research/QSD/codes_developing/QSD-for-WaSH/sanitation")

import biosteam as bst
from sanitation import Components, WasteStream, units

components = Components.load_default()
components.compile()
bst.settings.set_thermo(components)

ws1 = WasteStream.from_composite_measures('ws1', components, 10)

ins1 = WasteStream('ins1', SAc=5, H2O=1000, units='kg/hr')
ins2 = WasteStream('ins2', SF=10, H2O=1000, units='kg/hr')

M1 = units.Mixer('M1', ins=(ins1, ins2, ''), outs='mixture')
M1.simulate()
M1.show()
M1.diagram()

S1 = units.Splitter('S1', ins=M1-0, outs=('', ''), split=0.2)

ins3 = WasteStream('ins3', SNO3=7, H2O=1000, units='kg/hr')
P1 = units.Pump('P1', ins=ins3)

M2 = units.MixTank('M2', ins=(S1-0, P1-0), tau=2)
M2-0-2-M1

System = bst.System('System', path=(M1, S1, P1, M2), recycle=M2-0)
System.show()
System.simulate()
System.show()
System.diagram()

M2.show()
M2.results()




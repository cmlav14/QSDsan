#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Sanitation Explorer: Sustainable design of non-sewered sanitation technologies
Copyright (C) 2020, Sanitation Explorer Development Group

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>

This module is under the UIUC open-source license. See 
https://github.com/QSD-for-WaSH/sanitation/blob/master/LICENSE.txt
for license details.
'''

import biosteam as bst
from biosteam import utils
from .utils.piping import WSIns, WSOuts


__all__ = ('SanUnit',)

@utils.registered(ticket_name='SU')
class SanUnit(bst.Unit, isabstract=True):
    '''Subclass of Unit in biosteam, is initialized with WasteStream rather than Stream.'''

    def __init__(self, ID='', ins=None, outs=(), thermo=None):
        self._specification = None
        self._load_thermo(thermo)
        self._init_ins(ins)
        self._init_outs(outs)
        self._init_utils()
        self._init_results()
        self._assert_compatible_property_package()
        self._register(ID)
    
    def _init_ins(self, ins):
        self._ins = WSIns(self, self._N_ins, ins, self._thermo,
                          self._ins_size_is_fixed, self._stacklevel)
        
    def _init_outs(self, outs):
        self._outs = WSOuts(self, self._N_outs, outs, self._thermo,
                            self._outs_size_is_fixed, self._stacklevel)

    def _info(self, T, P, flow, composition, N, _stream_info):
        """Information of the unit."""
        if self.ID:
            info = f'{type(self).__name__}: {self.ID}\n'
        else:
            info = f'{type(self).__name__}\n'
        info += 'ins...\n'
        i = 0
        for stream in self.ins:
            if not stream:
                info += f'[{i}] {stream}\n'
                i += 1
                continue
            if _stream_info:
                stream_info = stream._info(T, P, flow, composition, N) + \
                    '\n' + stream._wastestream_info()
            else:
                stream_info = stream._wastestream_info()
            unit = stream._source
            index = stream_info.index('\n')
            source_info = f'  from  {type(unit).__name__}-{unit}\n' if unit else '\n'
            info += f'[{i}] {stream.ID}' + source_info + stream_info[index+1:] + '\n'
            i += 1
        info += 'outs...\n'
        i = 0
        for stream in self.outs:
            if not stream:
                info += f'[{i}] {stream}\n'
                i += 1
                continue
            if _stream_info:
                stream_info = stream._info(T, P, flow, composition, N) + \
                    '\n' + stream._wastestream_info()
            else:
                stream_info = stream._wastestream_info()
            unit = stream._sink
            index = stream_info.index('\n')
            sink_info = f'  to  {type(unit).__name__}-{unit}\n' if unit else '\n'
            info += f'[{i}] {stream.ID}' + sink_info + stream_info[index+1:] + '\n'
            i += 1
        info = info.replace('\n ', '\n    ')
        return info[:-1]
        
    def show(self, T=None, P=None, flow='kg/hr', composition=None, N=None, stream_info=True):
        """Print information of the unit, including WasteStream-specific information"""
        print(self._info(T, P, flow, composition, N, stream_info))
        



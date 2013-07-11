#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# generate_cpp.py
#
# Copyright (C) 2013 Alexey Naydenov <alexey.naydenovREMOVETHIS@linux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""C++ code generation functions."""

import registergen.tree as rgt

class DescriptionError(Exception):
    pass

def section_pre(section, state):
    state['namespace'].append(section['name'])
    state['header'].append('namespace {ns} {{'.format(ns=section['name']))
    state['src'].append('namespace {ns} {{'.format(ns=section['name']))
    state['addr'] = section.get('addr', None)
    return state

def section_post(section, state):
    state['namespace'].pop()
    state['header'].append('}} // namespace {ns}'.format(ns=section['name']))
    state['src'].append('}} // namespace {ns}'.format(ns=section['name']))
    state['addr'] = None
    return state

REGISTER_PRE_HEADER = [
    '//! Register {name}, {desc}',
    'struct {name} {{',
    'static const std::size_t address = 0x{addr:X};',
    '',
    'static inline uint32_t read() {{',
    '    return *(reinterpret_cast<volatile uint32_t *>(address));',
    '}}',
    'static inline uint32_t write(uint32_t new_value) {{',
    '    *(reinterpret_cast<volatile uint32_t *>(address)) = new_value;',
    '    return *(reinterpret_cast<volatile uint32_t *>(address));',
    '}}',
    '',
    '{name}() {{}}',
    'explicit {name}(uint32_t value) {{',
    '    write(value);',
    '}}',
    '',
    'operator uint32_t() const {{',
    '    return read();',
    '}}'
    ]
REGISTER_POST_HEADER = [
    '',
    '}}; // struct {name}'
    ]

def register_format_dict(register, state):
    format_dict = {'name': register['name'], 'desc': register.get('desc', '')}
    if 'addr' in register:
        format_dict['addr'] = register['addr']
    else:
        if 'off' in register and state['addr'] is not None:
            format_dict['addr'] = state['addr'] + register['off']
        else:
            raise DescriptionError('Cannot calculate address of {name}'.format(
                    **format_dict))
    return format_dict
            

def register_pre(register, state):
    format_dict = register_format_dict(register, state)
    header = [hl.format(**format_dict) for hl in REGISTER_PRE_HEADER]
    state['header'].extend(header)
    return state

def register_post(register, state):
    format_dict = register_format_dict(register, state)
    header = [hl.format(**format_dict) for hl in REGISTER_POST_HEADER]
    state['header'].extend(header)
    return state

CPP_GENERATOR_DICT = {'sections': {'pre': section_pre, 
                                   'post': section_post}, 
                      'registers': {'pre': register_pre, 
                                    'post': register_post},
                      'fields': {'pre': rgt.accumulate_nothing, 
                                 'post': rgt.accumulate_nothing},
                      'values': {'pre': rgt.accumulate_nothing, 
                                 'post': rgt.accumulate_nothing}}

def generate_cpp(regtree):
    regtree = rgt.transform_tree(rgt.convert_to_numbers, regtree, 
                                 rgt.numeric_filter)
    cpp_generator_state = {'namespace': [],
                           'addr': None,
                           'header': [],
                           'src': []}
    return rgt.process_tree(CPP_GENERATOR_DICT, regtree, cpp_generator_state)

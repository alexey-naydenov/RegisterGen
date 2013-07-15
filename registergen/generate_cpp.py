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
import registergen.utils as rgu

class DescriptionError(Exception):
    pass

CPP_HEADER_PREAMBLE = [
    '#ifndef {guard}',
    '#define {guard}',
    '',
    '#include <stdint.h>',
    '#include <string>',
    '#include <sstream>',
    '',
    'namespace {{',
    'uint32_t ReadField(uint32_t address, uint32_t first_bit, uint32_t last_bit) {{',
    '    return (*(reinterpret_cast<volatile uint32_t *>(address)) & ( ((~0u)<<(last_bit+1))^((~0u)<<first_bit) ))>>first_bit;',
    '',
    'void WriteField(uint32_t address, uint32_t first_bit, uint32_t last_bit, uint32_t value) {{',
    '    uint32_t mask = ((~0u)<<(last_bit+1))^((~0u)<<first_bit);',
    '    *(reinterpret_cast<volatile uint32_t *>(address)) =',
    '        (*(reinterpret_cast<volatile uint32_t *>(address)) & ~mask) | ((value<<first_bit) & mask);',
    '}}',
    ''
]

CPP_HEADER_EPILOG = [
    '#endif // {guard}',
    ]

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
    'typedef {name} ObjectType;',
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

REGISTER_DESC_BEG = [
    '//! Convert register value into a string.',
    'std::string {name}_desc(bool verbose=false) {{',
    '    uint32_t value = {name}();',
    '    std::ostringstream ss;',
    '    ss << "{name}: 0x" << std::hex << value "(" << std::dec << value << ")\\n";',
    '    if (verbose) {{',
    '        ss << "\\t{desc}\\n";',
    ]
REGISTER_DESC_VAL = [
    '        {field_name}_desc(verbose);'
    ]
REGISTER_DESC_END = [
    '    }}',
    '    return ss.str();',
    '}}'
    ]

def register_post(register, state):
    format_dict = register_format_dict(register, state)
    state['header'].extend([hl.format(**format_dict) 
                            for hl in REGISTER_DESC_BEG])
    for field in state['fields']:
        state['header'].extend([hl.format(field_name=field) 
                                for hl in REGISTER_DESC_VAL])
    state['header'].extend([hl.format(**format_dict) 
                            for hl in REGISTER_DESC_END])
    state['fields'] = []
    header = [hl.format(**format_dict) for hl in REGISTER_POST_HEADER]
    state['header'].extend(header)
    return state

FIELD_READ_HEADER = [
    '//! Read field {name}, {desc}',
    'inline uint32_t {name}() const {{',
    '    return ReadField(address, {bits[0]}, {bits[1]});',
    '}}',
]
FIELD_WRITE_HEADER = [
    '//! Write field {name}, {desc}',
    'ObjectType &{name}(uint32_t value) {{',
    '    WriteField(address, {bits[0]}, {bits[1]}, value);',
    '    return *this;',
    '}}',
]

def field_format_dict(field, state):
    format_dict = {'name': field['name'], 'desc': field.get('desc', ''),
                   'writable': field.get('writable', True)}
    if 'bits' in field:
        format_dict['bits'] = rgu.parse_bits(field['bits'])
    else:
        raise DescriptionError('Description of field {name} does '
                               'not have bits'.format(**format_dict))

    return format_dict

def field_pre(field, state):
    format_dict = field_format_dict(field, state)
    state['header'].extend([hl.format(**format_dict) 
                            for hl in FIELD_READ_HEADER])
    if format_dict['writable']:
        state['header'].extend([hl.format(**format_dict) 
                                for hl in FIELD_WRITE_HEADER])
    return state

FIELD_DESC_BEG = [
    '//! Convert field value into a string.',
    'std::string {name}_desc(bool verbose=false) {{',
    '    uint32_t value = {name}();',
    '    std::ostringstream ss;',
    '    ss << "{name} [{bits[1]}:{bits[0]}]: 0x" << std::hex << value "(" << std::dec << value << ")\\n";',
    '    if (verbose) {{',
    '        ss << "\\t{desc}\\n";',
    ]
FIELD_DESC_VAL = [
    '        if (value == k{name})',
    '            ss << "\\t0x" << std::hex << value << " - {name} \\n"'
    ]
FIELD_DESC_END = [
    '    }}',
    '    return ss.str();',
    '}}'
    ]

FIELD_VAL_CONST = [
    'const uint32_t k{name} = 0x{val:X};'
]

def field_post(field, state):
    format_dict = field_format_dict(field, state)
    for val_dict in state['values']:
        state['header'].extend([hl.format(**val_dict) 
                                for hl in FIELD_VAL_CONST])
    state['header'].extend([hl.format(**format_dict) 
                            for hl in FIELD_DESC_BEG])
    for val_dict in state['values']:
        state['header'].extend([hl.format(**val_dict) 
                                for hl in FIELD_DESC_VAL])
    state['header'].extend([hl.format(**format_dict) 
                            for hl in FIELD_DESC_END])
    state['values'] = []
    state['fields'].append(format_dict['name'])
    return state

def value_pre(value, state):
    state['values'].append(value)
    return state

CPP_GENERATOR_DICT = {'sections': {'pre': section_pre, 
                                   'post': section_post}, 
                      'registers': {'pre': register_pre, 
                                    'post': register_post},
                      'fields': {'pre': field_pre, 
                                 'post': field_post},
                      'values': {'pre': value_pre, 
                                 'post': rgt.accumulate_nothing}}

def generate_cpp(regtree):
    regtree = rgt.transform_tree(rgt.convert_to_numbers, regtree, 
                                 rgt.numeric_filter)
    cpp_generator_state = {'namespace': [],
                           'addr': None,
                           'header': [],
                           'src': [],
                           'fields': [],
                           'values': []}
    header_dict = {'guard': regtree.get('guard', 'GENERATED_HEADER').upper()}
    cpp_generator_state['header'].extend([hl.format(**header_dict) 
                                          for hl in CPP_HEADER_PREAMBLE])
    cpp_generator_state =rgt.process_tree(CPP_GENERATOR_DICT, regtree, 
                                          cpp_generator_state)
    cpp_generator_state['header'].extend([hl.format(**header_dict) 
                                          for hl in CPP_HEADER_EPILOG])
    return cpp_generator_state

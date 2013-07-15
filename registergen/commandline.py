#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# commandline.py
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

"""Command line utility for generating register access code."""

import sys
import argparse

import registergen.generate_cpp as rgc
import registergen.utils as rgu

def generate_cpp_code():
    options = argparse.ArgumentParser(
        description='Convert json description of some registers into cpp '
        'header that provides read/write/print functionality.')
    options.add_argument('-o', '--output', required=True, help='output file name')
    options.add_argument('-i', '--input', required=True, help='input file name')
    args = options.parse_args()
    # create cpp code
    try:
        parsed_json = rgu.read_json(args.input)
    except FileNotFoundError as e:
        sys.exit('can not read file: ' + e.filename)
    parsed_json['guard'] = args.output.replace('.', '_')
    cpp_state = rgc.generate_cpp(parsed_json)
    # write cpp header into a file
    with open(args.output, 'w') as output_file:
        output_file.write('\n'.join(cpp_state['header']))


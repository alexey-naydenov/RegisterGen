#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# utils.py
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

"""Utilities used in other functions."""

import re
import json

def read_json(filename):
    """Read json file from disk and return a dictionary."""
    with open(filename, 'r') as f:
        return json.load(f)

def string_to_int(int_string):
    """Convert a bin, hex or dec string into an integer."""
    if isinstance(int_string, str):
        return int(int_string, 0)
    else:
        return int_string
    
def parse_bits(bits):
    """Parse bit range string into list of length 2."""
    bits_match = re.match(r"(\d{1,2})(-(\d{1,2}))?", bits)
    if bits_match is None:
        raise Exception('Failed to parse bits in {0}'.format(bits))
    if bits_match.groups()[2] is None:
        parsed_bits = [int(bits_match.groups()[0]), 
                       int(bits_match.groups()[0])]
    else:
        parsed_bits = [int(bits_match.groups()[0]), 
                       int(bits_match.groups()[2])]
    return sorted(parsed_bits)

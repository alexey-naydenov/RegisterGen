#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# tree.py
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

"""Different utilities for walking register description tree."""

_SECTIONS = 'sections'
_REGISTERS = 'registers'
_FIELDS = 'fields'
_VALUES = 'values'
_CHILDREN_KEY_NAMES = [_SECTIONS, _REGISTERS, _FIELDS, _VALUES]
_NUMERIC_KEY_NAMES = ['addr', 'off', 'val']

def always_apply_condition(path, key):
    """Helper function that applies to all nodes."""
    return True

def apply_to_leaves(function, condition=None):
    """Apply a function to values of nodes that satisfy some condition. """
    pass

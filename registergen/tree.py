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

from collections import abc

import registergen.utils as rgu

_SECTIONS = 'sections'
_REGISTERS = 'registers'
_FIELDS = 'fields'
_VALUES = 'values'
_CHILDREN_KEY_NAMES = set([_SECTIONS, _REGISTERS, _FIELDS, _VALUES])
_NUMERIC_KEY_NAMES = set(['addr', 'off', 'val'])

def apply_to_all(path):
    """Helper function that applies to all nodes."""
    return True

def identity_transform(path, value):
    """Does not do anything with the tree, test function."""
    return value

def identity_transform_debug(path, value):
    print(path)
    return value

def numeric_filter(path):
    return path[-1] in _NUMERIC_KEY_NAMES

def convert_to_numbers(path, value):
    return rgu.string_to_int(value)

def transform_tree(function, tree, condition=None, path=None):
    """Apply a function to values of nodes that satisfy some condition.

    function must take a path value pair and return a new value;
    condition takes a path and returns a bool that indicates whether 
    the function must be applied to the given node.
    """
    if condition is None:
        condition = apply_to_all
    if path is None:
        path = []
    # transform breath first way, so that functions can remove subtrees
    for k, v in tree.items():
        if condition(path + [k]):
            tree[k] = function(path + [k], v)
    # iterate over children
    for k, v in tree.items():
        if k in _CHILDREN_KEY_NAMES and isinstance(v, abc.Iterable):
            tree[k] = [transform_tree(function, c, condition, path + [k]) 
                       for c in v]
    return tree

def accumulate_paths(path, value, accumulator):
    """Accumulate paths of visited nodes."""
    if accumulator is None:
        accumulator = []
    accumulator.append(".".join(path))
    return value, accumulator        

def reduce_tree(function, tree, accumulator=None):
    """Walk the tree and accumulate some data from it.

    function takes path, value and current value of the accumulator,
    it must return new value and new accumulator.
    """
    def transform_function(path, value):
        nonlocal accumulator
        new_value, accumulator = function(path, value, accumulator)
        return new_value
    tree = transform_tree(transform_function, tree)
    return accumulator, tree

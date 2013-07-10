from pprint import pprint

import registergen.tree as rgt

TEST_REGISTER_TREE = {'sections': [{'addr': '0x02530000',
                                    'desc': 'I2C configuration registers',
                                    'name': 'i2c',
                                    'registers': [{'desc': 'I2C Mode Register',
                                                   'name': 'ICMDR',
                                                   'off': '0x24'}]}]}

def test_transform_tree_identity():
    assert rgt.transform_tree(rgt.identity_transform, 
                              TEST_REGISTER_TREE) == TEST_REGISTER_TREE

# def test_accumulate_paths():
#     print(rgt.reduce_tree(rgt.accumulate_paths, TEST_REGISTER_TREE)[0])

def test_convert_numeric_values():
    pprint(TEST_REGISTER_TREE)
    pprint(rgt.transform_tree(rgt.convert_to_numbers, TEST_REGISTER_TREE, 
                             rgt.numeric_filter))

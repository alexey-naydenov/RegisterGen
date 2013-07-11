from pprint import pprint

import registergen.tree as rgt
import registergen.generate_cpp as rgc
import registergen.utils as rgu

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
#     pprint(rgt.reduce_tree(rgt.accumulate_paths, TEST_REGISTER_TREE,
#                            condition=rgt.internal_node_filter)[0])

# def test_convert_numeric_values():
#     pprint(TEST_REGISTER_TREE)
#     pprint(rgt.transform_tree(rgt.convert_to_numbers, TEST_REGISTER_TREE, 
#                              rgt.numeric_filter))

def test_generate_cpp():
    gen_state = rgc.generate_cpp(rgu.read_json('registergen/test/i2c.json'))
    print()
    print('\n'.join(gen_state['header']))
    print()
    


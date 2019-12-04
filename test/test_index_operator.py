"""
Name: Functional testing for index operator

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of index operator
"""
import copy
import random
import unittest

from methods.components.index_operator import connect_all, divide_all, sort_order


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.test_o_matrix = []
        self.test_i_matrix = []
        for index in range(100):
            data = list(map(int, list(str(bin(index))[2:].zfill(7))))
            self.test_o_matrix.append(data)
            self.test_i_matrix.append(data + data)

    def test_add_indices(self):
        i_matrix = connect_all(copy.deepcopy(self.test_o_matrix))
        self.assertEqual(i_matrix, self.test_i_matrix)

    def test_sort_indices(self):
        shuffle_i_matrix = copy.deepcopy(self.test_i_matrix)
        random.shuffle(shuffle_i_matrix)
        indices, temp_matrix = divide_all(shuffle_i_matrix)
        restore_matrix = sort_order(indices, temp_matrix)
        self.assertEqual(restore_matrix, self.test_o_matrix)

import copy
import random
import unittest

from methods.verifies import hm


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.test_binaries = [[random.randint(0, 1) for _ in range(12)] for _ in range(2)]
        self.test_real_verify_matrix = [
                [1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0]
            ]
        self.tool = hm.Hm()

    def test_add_verify_in_matrix(self):
        output_matrix = self.tool.add_for_matrix(self.test_binaries)
        self.assertEqual(output_matrix, self.test_real_verify_matrix)

    def test_verify_the_matrix(self):
        change_matrix = copy.deepcopy(self.test_real_verify_matrix)

        change_1_index = random.randint(0, len(self.test_real_verify_matrix[0]) - 1)
        if change_matrix[0][change_1_index] == 0:
            change_matrix[0][change_1_index] = 1
        else:
            change_matrix[0][change_1_index] = 0

        for change_index in random.sample([index for index in range(len(self.test_real_verify_matrix[0]))], 2):
            if change_matrix[1][change_index] == 0:
                change_matrix[1][change_index] = 1
            else:
                change_matrix[1][change_index] = 0

        output_matrix = self.tool.verify_for_matrix(copy.deepcopy(change_matrix))

        results = []
        for output_list, real_list in zip(output_matrix, self.test_real_verify_matrix):
            results.append(output_list == real_list)
        self.assertEqual(results, [True, False])

    def test_remove_verify_from_matrix(self):
        output_matrix = self.tool.remove_for_matrix(copy.deepcopy(self.test_real_verify_matrix))
        self.assertEqual(output_matrix, self.test_binaries)

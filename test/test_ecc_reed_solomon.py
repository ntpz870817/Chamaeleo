import copy
import random
import unittest

from Chamaeleo.methods.ecc import ReedSolomon


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.test_binaries = [[random.randint(0, 1) for _ in range(120)] for _ in range(3)]
        self.test_real_verify_matrix = [
            [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1,
             0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1,
             1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1,
             0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0,
             0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0,
             1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0,
             0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1,
             0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1,
             1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        ]

        self.tool = ReedSolomon(check_size=2)
        self.tool.segment_lengths = [120, 120, 120]

    def test_add_verify_in_matrix(self):
        output_matrix, _ = self.tool.insert(self.test_binaries)
        self.assertEqual(output_matrix, self.test_real_verify_matrix)

    def test_verify_the_matrix(self):
        change_matrix = copy.deepcopy(self.test_real_verify_matrix)

        change_1_index = random.randint(0, len(self.test_real_verify_matrix[0]) - 1)
        if change_matrix[1][change_1_index] == 0:
            change_matrix[1][change_1_index] = 1
        else:
            change_matrix[1][change_1_index] = 0

        for change_index in random.sample([index for index in range(len(self.test_real_verify_matrix[0]))], 4):
            if change_matrix[2][change_index] == 0:
                change_matrix[2][change_index] = 1
            else:
                change_matrix[2][change_index] = 0

        output_matrix = self.tool.remove(copy.deepcopy(change_matrix))
        results = []
        for output_list, real_list in zip(output_matrix["bit"], self.test_binaries):
            results.append(output_list == real_list)

        self.assertEqual(results, [True, True])

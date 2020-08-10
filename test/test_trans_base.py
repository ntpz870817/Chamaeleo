import random
import unittest

from Chamaeleo.methods.default import BaseCodingAlgorithm


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = BaseCodingAlgorithm(need_tips=False)
        self.test_list = [[random.randint(0, 1) for _ in range(160)] for _ in range(4)]

    def test_list_to_sequence(self):
        dna_sequences = self.tool.silicon_to_carbon(self.test_list, 160 * 4).get("dna")

        self.assertEqual(dna_sequences, [
                ['G', 'C', 'C', 'G', 'C', 'A', 'A', 'C', 'G', 'G', 'C', 'G', 'G', 'T', 'C', 'T', 'A', 'C', 'A', 'T',
                 'A', 'T', 'T', 'G', 'A', 'T', 'T', 'T', 'A', 'C', 'G', 'C', 'T', 'T', 'T', 'T', 'G', 'C', 'G', 'A',
                 'G', 'T', 'C', 'A', 'T', 'T', 'A', 'G', 'G', 'C', 'G', 'C', 'C', 'C', 'G', 'T', 'C', 'G', 'T', 'G',
                 'A', 'T', 'G', 'A', 'G', 'C', 'A', 'C', 'A', 'T', 'C', 'A', 'A', 'C', 'A', 'G', 'A', 'T', 'C', 'C'],
                ['G', 'T', 'C', 'G', 'T', 'C', 'A', 'C', 'A', 'A', 'T', 'A', 'G', 'T', 'T', 'G', 'A', 'A', 'A', 'C',
                 'C', 'C', 'T', 'A', 'A', 'T', 'G', 'G', 'G', 'C', 'G', 'T', 'G', 'A', 'G', 'G', 'T', 'G', 'C', 'C',
                 'G', 'A', 'A', 'T', 'A', 'A', 'A', 'C', 'A', 'A', 'T', 'A', 'G', 'G', 'G', 'A', 'T', 'A', 'A', 'A',
                 'G', 'G', 'C', 'C', 'T', 'G', 'C', 'A', 'T', 'G', 'G', 'T', 'A', 'A', 'C', 'T', 'A', 'A', 'A', 'G'],
                ['G', 'C', 'T', 'C', 'A', 'T', 'T', 'T', 'T', 'A', 'T', 'A', 'A', 'T', 'T', 'C', 'G', 'T', 'G', 'T',
                 'T', 'T', 'G', 'T', 'A', 'T', 'A', 'G', 'G', 'C', 'A', 'C', 'C', 'T', 'G', 'T', 'T', 'G', 'A', 'A',
                 'A', 'A', 'C', 'T', 'A', 'G', 'T', 'C', 'A', 'C', 'T', 'G', 'A', 'G', 'C', 'G', 'G', 'G', 'C', 'T',
                 'C', 'A', 'G', 'C', 'G', 'A', 'A', 'T', 'T', 'G', 'T', 'G', 'T', 'G', 'C', 'T', 'G', 'T', 'A', 'G'],
                ['C', 'G', 'T', 'C', 'G', 'G', 'A', 'T', 'T', 'G', 'A', 'G', 'G', 'T', 'T', 'A', 'C', 'G', 'A', 'C',
                 'C', 'G', 'G', 'G', 'G', 'C', 'C', 'C', 'G', 'T', 'C', 'A', 'A', 'A', 'A', 'G', 'A', 'A', 'G', 'T',
                 'T', 'G', 'G', 'G', 'T', 'G', 'C', 'A', 'A', 'C', 'A', 'T', 'G', 'G', 'G', 'G', 'G', 'C', 'G', 'G',
                 'A', 'A', 'T', 'A', 'G', 'C', 'A', 'G', 'G', 'G', 'T', 'T', 'A', 'T', 'C', 'G', 'A', 'G', 'T', 'T'],
            ])

    def test_sequence_to_list(self):
        bit_segments = self.tool.carbon_to_silicon([
                ['G', 'C', 'C', 'G', 'C', 'A', 'A', 'C', 'G', 'G', 'C', 'G', 'G', 'T', 'C', 'T', 'A', 'C', 'A', 'T',
                 'A', 'T', 'T', 'G', 'A', 'T', 'T', 'T', 'A', 'C', 'G', 'C', 'T', 'T', 'T', 'T', 'G', 'C', 'G', 'A',
                 'G', 'T', 'C', 'A', 'T', 'T', 'A', 'G', 'G', 'C', 'G', 'C', 'C', 'C', 'G', 'T', 'C', 'G', 'T', 'G',
                 'A', 'T', 'G', 'A', 'G', 'C', 'A', 'C', 'A', 'T', 'C', 'A', 'A', 'C', 'A', 'G', 'A', 'T', 'C', 'C'],
                ['G', 'T', 'C', 'G', 'T', 'C', 'A', 'C', 'A', 'A', 'T', 'A', 'G', 'T', 'T', 'G', 'A', 'A', 'A', 'C',
                 'C', 'C', 'T', 'A', 'A', 'T', 'G', 'G', 'G', 'C', 'G', 'T', 'G', 'A', 'G', 'G', 'T', 'G', 'C', 'C',
                 'G', 'A', 'A', 'T', 'A', 'A', 'A', 'C', 'A', 'A', 'T', 'A', 'G', 'G', 'G', 'A', 'T', 'A', 'A', 'A',
                 'G', 'G', 'C', 'C', 'T', 'G', 'C', 'A', 'T', 'G', 'G', 'T', 'A', 'A', 'C', 'T', 'A', 'A', 'A', 'G'],
                ['G', 'C', 'T', 'C', 'A', 'T', 'T', 'T', 'T', 'A', 'T', 'A', 'A', 'T', 'T', 'C', 'G', 'T', 'G', 'T',
                 'T', 'T', 'G', 'T', 'A', 'T', 'A', 'G', 'G', 'C', 'A', 'C', 'C', 'T', 'G', 'T', 'T', 'G', 'A', 'A',
                 'A', 'A', 'C', 'T', 'A', 'G', 'T', 'C', 'A', 'C', 'T', 'G', 'A', 'G', 'C', 'G', 'G', 'G', 'C', 'T',
                 'C', 'A', 'G', 'C', 'G', 'A', 'A', 'T', 'T', 'G', 'T', 'G', 'T', 'G', 'C', 'T', 'G', 'T', 'A', 'G'],
                ['C', 'G', 'T', 'C', 'G', 'G', 'A', 'T', 'T', 'G', 'A', 'G', 'G', 'T', 'T', 'A', 'C', 'G', 'A', 'C',
                 'C', 'G', 'G', 'G', 'G', 'C', 'C', 'C', 'G', 'T', 'C', 'A', 'A', 'A', 'A', 'G', 'A', 'A', 'G', 'T',
                 'T', 'G', 'G', 'G', 'T', 'G', 'C', 'A', 'A', 'C', 'A', 'T', 'G', 'G', 'G', 'G', 'G', 'C', 'G', 'G',
                 'A', 'A', 'T', 'A', 'G', 'C', 'A', 'G', 'G', 'G', 'T', 'T', 'A', 'T', 'C', 'G', 'A', 'G', 'T', 'T'],
            ]).get("bit")

        self.assertEqual(bit_segments, self.test_list)
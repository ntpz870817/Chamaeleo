import random
import unittest

from Chamaeleo.methods.fixed import Grass


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = Grass(need_tips=False)
        self.tool.segment_length = 160
        self.test_list = [[random.randint(0, 1) for _ in range(160)] for _ in range(4)]

    def test_list_to_sequence(self):
        dna_sequences = self.tool.silicon_to_carbon(self.test_list, 160 * 4).get("dna")
        self.assertEqual(dna_sequences, [
            ['C', 'C', 'T', 'C', 'G', 'C', 'C', 'G', 'C', 'C', 'G', 'C', 'C', 'C', 'A', 'A', 'C', 'A', 'A', 'A', 'T',
             'A', 'T', 'C', 'T', 'A', 'T', 'A', 'G', 'C', 'C', 'A', 'T', 'G', 'G', 'T', 'G', 'C', 'T', 'G', 'C', 'T',
             'A', 'G', 'T', 'C', 'G', 'T', 'T', 'T', 'A', 'G', 'C', 'A', 'C', 'C', 'T', 'T', 'A', 'C', 'C', 'A', 'T',
             'C', 'A', 'C', 'T', 'A', 'C', 'C', 'C', 'G', 'C', 'C', 'G', 'T', 'A', 'T', 'T', 'G', 'A', 'A', 'A', 'T',
             'A', 'C', 'T', 'A', 'G', 'T'],
            ['C', 'T', 'A', 'A', 'G', 'T', 'T', 'A', 'C', 'A', 'A', 'G', 'C', 'T', 'C', 'C', 'G', 'C', 'A', 'A', 'C',
             'A', 'G', 'C', 'C', 'G', 'C', 'A', 'G', 'A', 'T', 'A', 'G', 'A', 'T', 'C', 'C', 'C', 'G', 'A', 'C', 'G',
             'G', 'A', 'G', 'C', 'C', 'A', 'A', 'G', 'T', 'G', 'A', 'T', 'A', 'A', 'G', 'C', 'T', 'A', 'T', 'G', 'T',
             'C', 'T', 'C', 'C', 'C', 'A', 'C', 'A', 'T', 'G', 'A', 'T', 'G', 'A', 'C', 'T', 'C', 'T', 'A', 'A', 'C',
             'T', 'A', 'T', 'A', 'G', 'T'],
            ['C', 'G', 'A', 'A', 'T', 'C', 'C', 'T', 'G', 'C', 'T', 'G', 'G', 'G', 'C', 'C', 'T', 'A', 'C', 'T', 'A',
             'T', 'A', 'C', 'T', 'G', 'A', 'A', 'C', 'T', 'T', 'C', 'G', 'C', 'G', 'T', 'C', 'A', 'T', 'C', 'C', 'G',
             'G', 'T', 'C', 'A', 'A', 'C', 'T', 'C', 'A', 'A', 'C', 'G', 'A', 'C', 'A', 'C', 'T', 'G', 'A', 'T', 'C',
             'C', 'G', 'C', 'C', 'G', 'A', 'A', 'G', 'T', 'C', 'C', 'A', 'C', 'A', 'G', 'G', 'C', 'G', 'G', 'A', 'T',
             'T', 'C', 'G', 'A', 'A', 'C'],
            ['C', 'A', 'C', 'G', 'T', 'A', 'A', 'G', 'T', 'G', 'A', 'T', 'C', 'A', 'C', 'T', 'T', 'C', 'A', 'T', 'G',
             'C', 'A', 'G', 'G', 'C', 'G', 'C', 'C', 'T', 'C', 'C', 'G', 'C', 'G', 'C', 'A', 'A', 'C', 'A', 'T', 'G',
             'A', 'G', 'A', 'G', 'C', 'A', 'A', 'T', 'C', 'C', 'G', 'C', 'A', 'A', 'T', 'C', 'A', 'G', 'A', 'C', 'T',
             'C', 'C', 'T', 'T', 'C', 'G', 'A', 'C', 'A', 'C', 'C', 'G', 'T', 'T', 'C', 'T', 'T', 'A', 'A', 'G', 'A',
             'C', 'A', 'G', 'A', 'G', 'A']
        ])

    def test_sequence_to_list(self):
        bit_segments = self.tool.carbon_to_silicon([
            ['C', 'C', 'T', 'C', 'G', 'C', 'C', 'G', 'C', 'C', 'G', 'C', 'C', 'C', 'A', 'A', 'C', 'A', 'A', 'A', 'T',
             'A', 'T', 'C', 'T', 'A', 'T', 'A', 'G', 'C', 'C', 'A', 'T', 'G', 'G', 'T', 'G', 'C', 'T', 'G', 'C', 'T',
             'A', 'G', 'T', 'C', 'G', 'T', 'T', 'T', 'A', 'G', 'C', 'A', 'C', 'C', 'T', 'T', 'A', 'C', 'C', 'A', 'T',
             'C', 'A', 'C', 'T', 'A', 'C', 'C', 'C', 'G', 'C', 'C', 'G', 'T', 'A', 'T', 'T', 'G', 'A', 'A', 'A', 'T',
             'A', 'C', 'T', 'A', 'G', 'T'],
            ['C', 'T', 'A', 'A', 'G', 'T', 'T', 'A', 'C', 'A', 'A', 'G', 'C', 'T', 'C', 'C', 'G', 'C', 'A', 'A', 'C',
             'A', 'G', 'C', 'C', 'G', 'C', 'A', 'G', 'A', 'T', 'A', 'G', 'A', 'T', 'C', 'C', 'C', 'G', 'A', 'C', 'G',
             'G', 'A', 'G', 'C', 'C', 'A', 'A', 'G', 'T', 'G', 'A', 'T', 'A', 'A', 'G', 'C', 'T', 'A', 'T', 'G', 'T',
             'C', 'T', 'C', 'C', 'C', 'A', 'C', 'A', 'T', 'G', 'A', 'T', 'G', 'A', 'C', 'T', 'C', 'T', 'A', 'A', 'C',
             'T', 'A', 'T', 'A', 'G', 'T'],
            ['C', 'G', 'A', 'A', 'T', 'C', 'C', 'T', 'G', 'C', 'T', 'G', 'G', 'G', 'C', 'C', 'T', 'A', 'C', 'T', 'A',
             'T', 'A', 'C', 'T', 'G', 'A', 'A', 'C', 'T', 'T', 'C', 'G', 'C', 'G', 'T', 'C', 'A', 'T', 'C', 'C', 'G',
             'G', 'T', 'C', 'A', 'A', 'C', 'T', 'C', 'A', 'A', 'C', 'G', 'A', 'C', 'A', 'C', 'T', 'G', 'A', 'T', 'C',
             'C', 'G', 'C', 'C', 'G', 'A', 'A', 'G', 'T', 'C', 'C', 'A', 'C', 'A', 'G', 'G', 'C', 'G', 'G', 'A', 'T',
             'T', 'C', 'G', 'A', 'A', 'C'],
            ['C', 'A', 'C', 'G', 'T', 'A', 'A', 'G', 'T', 'G', 'A', 'T', 'C', 'A', 'C', 'T', 'T', 'C', 'A', 'T', 'G',
             'C', 'A', 'G', 'G', 'C', 'G', 'C', 'C', 'T', 'C', 'C', 'G', 'C', 'G', 'C', 'A', 'A', 'C', 'A', 'T', 'G',
             'A', 'G', 'A', 'G', 'C', 'A', 'A', 'T', 'C', 'C', 'G', 'C', 'A', 'A', 'T', 'C', 'A', 'G', 'A', 'C', 'T',
             'C', 'C', 'T', 'T', 'C', 'G', 'A', 'C', 'A', 'C', 'C', 'G', 'T', 'T', 'C', 'T', 'T', 'A', 'A', 'G', 'A',
             'C', 'A', 'G', 'A', 'G', 'A']
        ]).get("bit")

        self.assertEqual(bit_segments, self.test_list)
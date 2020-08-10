import random
import unittest

from Chamaeleo.methods.fixed import Blawat


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = Blawat(need_tips=False)
        self.test_list = [[random.randint(0, 1) for _ in range(160)] for _ in range(4)]

    def test_list_to_sequence(self):
        dna_sequences = self.tool.silicon_to_carbon(self.test_list, 160 * 4).get("dna")
        self.assertEqual(dna_sequences, [
            ['G', 'C', 'A', 'C', 'G', 'C', 'A', 'A', 'A', 'C', 'G', 'G', 'A', 'C', 'G', 'G', 'T', 'A', 'C', 'T', 'A',
             'C', 'A', 'A', 'T', 'A', 'T', 'A', 'T', 'G', 'A', 'T', 'C', 'T', 'A', 'A', 'C', 'A', 'G', 'C', 'T', 'T',
             'C', 'T', 'A', 'G', 'C', 'A', 'G', 'A', 'G', 'T', 'A', 'C', 'A', 'T', 'T', 'A', 'A', 'G', 'G', 'C', 'A',
             'G', 'C', 'C', 'C', 'A', 'G', 'T', 'C', 'G', 'A', 'T', 'G', 'A', 'T', 'A', 'G', 'A', 'G', 'C', 'A', 'A',
             'C', 'A', 'T', 'A', 'C', 'A', 'A', 'C', 'A', 'A', 'G', 'A', 'T', 'C', 'C', 'G'],
            ['G', 'T', 'A', 'C', 'G', 'T', 'C', 'A', 'A', 'C', 'A', 'A', 'C', 'T', 'C', 'G', 'T', 'A', 'T', 'G', 'A',
             'A', 'C', 'A', 'G', 'C', 'C', 'A', 'T', 'A', 'A', 'T', 'C', 'G', 'T', 'G', 'C', 'A', 'G', 'T', 'G', 'A',
             'C', 'G', 'T', 'T', 'G', 'C', 'C', 'G', 'G', 'A', 'A', 'A', 'T', 'A', 'A', 'C', 'A', 'G', 'A', 'A', 'C',
             'T', 'C', 'G', 'G', 'A', 'G', 'A', 'T', 'A', 'C', 'A', 'C', 'G', 'G', 'C', 'C', 'G', 'T', 'G', 'A', 'C',
             'A', 'T', 'G', 'A', 'G', 'T', 'A', 'A', 'C', 'C', 'A', 'A', 'A', 'C', 'A', 'T'],
            ['G', 'C', 'A', 'T', 'C', 'A', 'T', 'C', 'T', 'A', 'T', 'A', 'A', 'T', 'A', 'A', 'T', 'A', 'T', 'C', 'G',
             'T', 'A', 'G', 'T', 'T', 'T', 'A', 'G', 'T', 'A', 'T', 'A', 'A', 'G', 'G', 'C', 'A', 'A', 'C', 'C', 'T',
             'A', 'G', 'T', 'T', 'G', 'C', 'A', 'C', 'A', 'A', 'C', 'C', 'A', 'A', 'G', 'A', 'T', 'C', 'A', 'C', 'A',
             'T', 'G', 'A', 'G', 'A', 'C', 'G', 'G', 'G', 'A', 'C', 'T', 'C', 'A', 'A', 'G', 'C', 'G', 'A', 'A', 'A',
             'T', 'T', 'G', 'A', 'T', 'G', 'T', 'G', 'A', 'C', 'T', 'G', 'T', 'A', 'A', 'G'],
            ['C', 'G', 'A', 'T', 'C', 'G', 'G', 'A', 'A', 'T', 'T', 'G', 'A', 'A', 'G', 'G', 'T', 'A', 'T', 'A', 'C',
             'G', 'A', 'A', 'C', 'C', 'G', 'C', 'G', 'T', 'G', 'C', 'C', 'C', 'G', 'G', 'T', 'A', 'C', 'A', 'A', 'A',
             'C', 'A', 'T', 'A', 'A', 'C', 'G', 'A', 'T', 'G', 'C', 'G', 'T', 'T', 'G', 'A', 'C', 'A', 'A', 'C', 'A',
             'A', 'T', 'G', 'G', 'C', 'G', 'T', 'G', 'C', 'C', 'G', 'T', 'A', 'A', 'C', 'T', 'C', 'G', 'C', 'A', 'A',
             'G', 'G', 'G', 'C', 'T', 'A', 'A', 'T', 'A', 'C', 'G', 'A', 'G', 'C', 'T', 'A']
        ])

    def test_sequence_to_list(self):
        bit_segments = self.tool.carbon_to_silicon([
            ['G', 'C', 'A', 'C', 'G', 'C', 'A', 'A', 'A', 'C', 'G', 'G', 'A', 'C', 'G', 'G', 'T', 'A', 'C', 'T', 'A',
             'C', 'A', 'A', 'T', 'A', 'T', 'A', 'T', 'G', 'A', 'T', 'C', 'T', 'A', 'A', 'C', 'A', 'G', 'C', 'T', 'T',
             'C', 'T', 'A', 'G', 'C', 'A', 'G', 'A', 'G', 'T', 'A', 'C', 'A', 'T', 'T', 'A', 'A', 'G', 'G', 'C', 'A',
             'G', 'C', 'C', 'C', 'A', 'G', 'T', 'C', 'G', 'A', 'T', 'G', 'A', 'T', 'A', 'G', 'A', 'G', 'C', 'A', 'A',
             'C', 'A', 'T', 'A', 'C', 'A', 'A', 'C', 'A', 'A', 'G', 'A', 'T', 'C', 'C', 'G'],
            ['G', 'T', 'A', 'C', 'G', 'T', 'C', 'A', 'A', 'C', 'A', 'A', 'C', 'T', 'C', 'G', 'T', 'A', 'T', 'G', 'A',
             'A', 'C', 'A', 'G', 'C', 'C', 'A', 'T', 'A', 'A', 'T', 'C', 'G', 'T', 'G', 'C', 'A', 'G', 'T', 'G', 'A',
             'C', 'G', 'T', 'T', 'G', 'C', 'C', 'G', 'G', 'A', 'A', 'A', 'T', 'A', 'A', 'C', 'A', 'G', 'A', 'A', 'C',
             'T', 'C', 'G', 'G', 'A', 'G', 'A', 'T', 'A', 'C', 'A', 'C', 'G', 'G', 'C', 'C', 'G', 'T', 'G', 'A', 'C',
             'A', 'T', 'G', 'A', 'G', 'T', 'A', 'A', 'C', 'C', 'A', 'A', 'A', 'C', 'A', 'T'],
            ['G', 'C', 'A', 'T', 'C', 'A', 'T', 'C', 'T', 'A', 'T', 'A', 'A', 'T', 'A', 'A', 'T', 'A', 'T', 'C', 'G',
             'T', 'A', 'G', 'T', 'T', 'T', 'A', 'G', 'T', 'A', 'T', 'A', 'A', 'G', 'G', 'C', 'A', 'A', 'C', 'C', 'T',
             'A', 'G', 'T', 'T', 'G', 'C', 'A', 'C', 'A', 'A', 'C', 'C', 'A', 'A', 'G', 'A', 'T', 'C', 'A', 'C', 'A',
             'T', 'G', 'A', 'G', 'A', 'C', 'G', 'G', 'G', 'A', 'C', 'T', 'C', 'A', 'A', 'G', 'C', 'G', 'A', 'A', 'A',
             'T', 'T', 'G', 'A', 'T', 'G', 'T', 'G', 'A', 'C', 'T', 'G', 'T', 'A', 'A', 'G'],
            ['C', 'G', 'A', 'T', 'C', 'G', 'G', 'A', 'A', 'T', 'T', 'G', 'A', 'A', 'G', 'G', 'T', 'A', 'T', 'A', 'C',
             'G', 'A', 'A', 'C', 'C', 'G', 'C', 'G', 'T', 'G', 'C', 'C', 'C', 'G', 'G', 'T', 'A', 'C', 'A', 'A', 'A',
             'C', 'A', 'T', 'A', 'A', 'C', 'G', 'A', 'T', 'G', 'C', 'G', 'T', 'T', 'G', 'A', 'C', 'A', 'A', 'C', 'A',
             'A', 'T', 'G', 'G', 'C', 'G', 'T', 'G', 'C', 'C', 'G', 'T', 'A', 'A', 'C', 'T', 'C', 'G', 'C', 'A', 'A',
             'G', 'G', 'G', 'C', 'T', 'A', 'A', 'T', 'A', 'C', 'G', 'A', 'G', 'C', 'T', 'A']
        ]).get("bit")

        self.assertEqual(bit_segments, self.test_list)
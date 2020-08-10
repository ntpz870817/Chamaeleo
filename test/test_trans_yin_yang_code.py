import random
import unittest

from Chamaeleo.methods.flowed import YinYangCode


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = YinYangCode(need_tips=False)
        self.test_list = [[random.randint(0, 1) for _ in range(100)] for _ in range(8)]

    def test_list_to_sequence(self):
        dna_sequences = self.tool.silicon_to_carbon(self.test_list, 100 * 8).get("dna")
        self.assertEqual(dna_sequences, [
            ['G', 'T', 'C', 'G', 'A', 'G', 'C', 'T', 'C', 'A', 'T', 'G', 'G', 'A', 'A', 'T', 'T', 'T', 'G', 'C', 'C',
             'A', 'A', 'G', 'C', 'C', 'T', 'T', 'A', 'G', 'G', 'C', 'G', 'A', 'G', 'A', 'A', 'G', 'A', 'C', 'C', 'T',
             'G', 'T', 'T', 'T', 'G', 'T', 'T', 'T', 'C', 'G', 'T', 'G', 'G', 'T', 'A', 'T', 'A', 'A', 'A', 'C', 'T',
             'G', 'C', 'G', 'C', 'C', 'T', 'A', 'A', 'T', 'T', 'C', 'G', 'G', 'T', 'G', 'G', 'A', 'G', 'G', 'A', 'C',
             'A', 'T', 'C', 'G', 'C', 'G', 'A', 'T', 'C', 'G', 'G', 'C', 'T', 'G', 'C', 'G'],
            ['G', 'T', 'G', 'T', 'C', 'T', 'G', 'G', 'A', 'G', 'T', 'C', 'C', 'G', 'C', 'G', 'C', 'G', 'A', 'T', 'C',
             'A', 'C', 'T', 'T', 'G', 'A', 'A', 'T', 'A', 'C', 'G', 'T', 'T', 'C', 'G', 'A', 'C', 'A', 'C', 'T', 'A',
             'A', 'A', 'A', 'G', 'T', 'T', 'G', 'A', 'G', 'G', 'G', 'A', 'A', 'T', 'A', 'A', 'G', 'A', 'T', 'C', 'G',
             'A', 'C', 'G', 'C', 'A', 'C', 'G', 'G', 'A', 'C', 'T', 'A', 'A', 'G', 'A', 'A', 'G', 'T', 'A', 'T', 'G',
             'A', 'C', 'A', 'C', 'C', 'T', 'T', 'A', 'G', 'T', 'G', 'A', 'T', 'T', 'T', 'A'],
            ['A', 'G', 'G', 'A', 'G', 'C', 'T', 'T', 'G', 'A', 'T', 'G', 'T', 'T', 'G', 'C', 'A', 'G', 'A', 'T', 'T',
             'C', 'T', 'G', 'A', 'G', 'C', 'A', 'G', 'C', 'T', 'A', 'T', 'G', 'T', 'A', 'G', 'T', 'C', 'T', 'G', 'T',
             'A', 'A', 'C', 'A', 'A', 'T', 'T', 'G', 'A', 'A', 'A', 'A', 'C', 'T', 'T', 'T', 'T', 'A', 'C', 'C', 'C',
             'A', 'C', 'T', 'C', 'A', 'A', 'C', 'T', 'C', 'T', 'G', 'T', 'C', 'A', 'G', 'T', 'G', 'A', 'T', 'C', 'A',
             'T', 'C', 'G', 'T', 'C', 'A', 'C', 'A', 'G', 'G', 'C', 'C', 'T', 'T', 'T', 'A'],
            ['C', 'G', 'A', 'C', 'G', 'T', 'G', 'T', 'T', 'A', 'C', 'T', 'G', 'T', 'T', 'G', 'T', 'T', 'C', 'G', 'A',
             'G', 'T', 'C', 'T', 'A', 'G', 'A', 'T', 'G', 'A', 'C', 'A', 'A', 'A', 'C', 'A', 'A', 'T', 'T', 'A', 'C',
             'G', 'G', 'G', 'G', 'A', 'C', 'A', 'A', 'T', 'A', 'A', 'G', 'C', 'T', 'A', 'T', 'A', 'C', 'T', 'A', 'C',
             'T', 'A', 'T', 'C', 'A', 'T', 'T', 'A', 'C', 'G', 'G', 'A', 'T', 'A', 'G', 'G', 'A', 'T', 'T', 'G', 'A',
             'T', 'A', 'C', 'T', 'C', 'C', 'T', 'A', 'A', 'A', 'A', 'G', 'G', 'G', 'G', 'T']
        ])

    def test_sequence_to_list(self):
        bit_segments = self.tool.carbon_to_silicon([
            ['G', 'T', 'C', 'G', 'A', 'G', 'C', 'T', 'C', 'A', 'T', 'G', 'G', 'A', 'A', 'T', 'T', 'T', 'G', 'C', 'C',
             'A', 'A', 'G', 'C', 'C', 'T', 'T', 'A', 'G', 'G', 'C', 'G', 'A', 'G', 'A', 'A', 'G', 'A', 'C', 'C', 'T',
             'G', 'T', 'T', 'T', 'G', 'T', 'T', 'T', 'C', 'G', 'T', 'G', 'G', 'T', 'A', 'T', 'A', 'A', 'A', 'C', 'T',
             'G', 'C', 'G', 'C', 'C', 'T', 'A', 'A', 'T', 'T', 'C', 'G', 'G', 'T', 'G', 'G', 'A', 'G', 'G', 'A', 'C',
             'A', 'T', 'C', 'G', 'C', 'G', 'A', 'T', 'C', 'G', 'G', 'C', 'T', 'G', 'C', 'G'],
            ['G', 'T', 'G', 'T', 'C', 'T', 'G', 'G', 'A', 'G', 'T', 'C', 'C', 'G', 'C', 'G', 'C', 'G', 'A', 'T', 'C',
             'A', 'C', 'T', 'T', 'G', 'A', 'A', 'T', 'A', 'C', 'G', 'T', 'T', 'C', 'G', 'A', 'C', 'A', 'C', 'T', 'A',
             'A', 'A', 'A', 'G', 'T', 'T', 'G', 'A', 'G', 'G', 'G', 'A', 'A', 'T', 'A', 'A', 'G', 'A', 'T', 'C', 'G',
             'A', 'C', 'G', 'C', 'A', 'C', 'G', 'G', 'A', 'C', 'T', 'A', 'A', 'G', 'A', 'A', 'G', 'T', 'A', 'T', 'G',
             'A', 'C', 'A', 'C', 'C', 'T', 'T', 'A', 'G', 'T', 'G', 'A', 'T', 'T', 'T', 'A'],
            ['A', 'G', 'G', 'A', 'G', 'C', 'T', 'T', 'G', 'A', 'T', 'G', 'T', 'T', 'G', 'C', 'A', 'G', 'A', 'T', 'T',
             'C', 'T', 'G', 'A', 'G', 'C', 'A', 'G', 'C', 'T', 'A', 'T', 'G', 'T', 'A', 'G', 'T', 'C', 'T', 'G', 'T',
             'A', 'A', 'C', 'A', 'A', 'T', 'T', 'G', 'A', 'A', 'A', 'A', 'C', 'T', 'T', 'T', 'T', 'A', 'C', 'C', 'C',
             'A', 'C', 'T', 'C', 'A', 'A', 'C', 'T', 'C', 'T', 'G', 'T', 'C', 'A', 'G', 'T', 'G', 'A', 'T', 'C', 'A',
             'T', 'C', 'G', 'T', 'C', 'A', 'C', 'A', 'G', 'G', 'C', 'C', 'T', 'T', 'T', 'A'],
            ['C', 'G', 'A', 'C', 'G', 'T', 'G', 'T', 'T', 'A', 'C', 'T', 'G', 'T', 'T', 'G', 'T', 'T', 'C', 'G', 'A',
             'G', 'T', 'C', 'T', 'A', 'G', 'A', 'T', 'G', 'A', 'C', 'A', 'A', 'A', 'C', 'A', 'A', 'T', 'T', 'A', 'C',
             'G', 'G', 'G', 'G', 'A', 'C', 'A', 'A', 'T', 'A', 'A', 'G', 'C', 'T', 'A', 'T', 'A', 'C', 'T', 'A', 'C',
             'T', 'A', 'T', 'C', 'A', 'T', 'T', 'A', 'C', 'G', 'G', 'A', 'T', 'A', 'G', 'G', 'A', 'T', 'T', 'G', 'A',
             'T', 'A', 'C', 'T', 'C', 'C', 'T', 'A', 'A', 'A', 'A', 'G', 'G', 'G', 'G', 'T']
        ]).get("bit")

        for bit_segment in bit_segments:
            self.assertIn(bit_segment, self.test_list)
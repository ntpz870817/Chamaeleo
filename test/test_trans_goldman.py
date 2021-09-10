import random
import unittest
from Chamaeleo.methods.fixed import Goldman


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = Goldman(need_logs=False)
        self.tool.segment_length = 160
        self.test_list = [[random.randint(0, 1) for _ in range(160)] for _ in range(4)]

    def test_list_to_sequence(self):
        dna_sequences = self.tool.silicon_to_carbon(self.test_list, 160 * 4).get("dna")
        self.assertEqual(dna_sequences, [
            ['T', 'C', 'G', 'T', 'G', 'T', 'G', 'T', 'G', 'C', 'A', 'G', 'T', 'C', 'T', 'A', 'T', 'G', 'C', 'A', 'G',
             'A', 'G', 'A', 'G', 'C', 'A', 'T', 'C', 'A', 'C', 'A', 'G', 'T', 'C', 'G', 'A', 'T', 'C', 'A', 'G', 'C',
             'T', 'C', 'A', 'T', 'G', 'C', 'A', 'T', 'G', 'A', 'C', 'A', 'C', 'T', 'G', 'T', 'G', 'A', 'G', 'C', 'T',
             'C', 'G', 'C', 'G', 'T', 'C', 'A', 'C', 'A', 'C', 'G', 'T', 'G', 'A', 'C', 'A', 'T', 'A', 'G', 'A', 'G',
             'A', 'T', 'A', 'T', 'G', 'A', 'G', 'C', 'T', 'G', 'A', 'T', 'A', 'G', 'C', 'T', 'G', 'C'],
            ['G', 'C', 'G', 'C', 'A', 'G', 'C', 'G', 'T', 'A', 'G', 'C', 'G', 'T', 'C', 'G', 'A', 'T', 'G', 'C', 'G',
             'T', 'C', 'G', 'T', 'C', 'G', 'C', 'G', 'T', 'G', 'T', 'A', 'T', 'C', 'G', 'A', 'C', 'G', 'C', 'A', 'T',
             'C', 'T', 'C', 'A', 'G', 'A', 'T', 'C', 'G', 'T', 'G', 'A', 'T', 'A', 'C', 'T', 'A', 'C', 'T', 'G', 'T',
             'A', 'G', 'C', 'G', 'T', 'A', 'T', 'A', 'G', 'C', 'G', 'A', 'G', 'A', 'T', 'G', 'C', 'A', 'T', 'G', 'A',
             'T', 'C', 'G', 'T', 'C', 'G', 'A', 'T', 'G', 'C', 'T', 'C', 'G', 'A', 'G', 'C', 'A', 'C'],
            ['C', 'G', 'A', 'T', 'A', 'T', 'C', 'G', 'A', 'C', 'G', 'C', 'T', 'G', 'T', 'G', 'C', 'A', 'T', 'A', 'C',
             'G', 'T', 'C', 'T', 'G', 'C', 'G', 'T', 'A', 'C', 'T', 'C', 'T', 'A', 'G', 'A', 'G', 'A', 'T', 'A', 'C',
             'A', 'G', 'A', 'G', 'A', 'G', 'A', 'T', 'C', 'A', 'T', 'G', 'A', 'G', 'T', 'A', 'G', 'C', 'T', 'A', 'T',
             'G', 'C', 'T', 'A', 'T', 'C', 'T', 'G', 'A', 'G', 'A', 'C', 'T', 'C', 'G', 'C', 'G', 'T', 'C', 'G', 'T',
             'A', 'T', 'C', 'A', 'C', 'G', 'A', 'G', 'A', 'C', 'T', 'A', 'C', 'T', 'C', 'G', 'C', 'T', 'A'],
            ['G', 'A', 'C', 'A', 'G', 'C', 'T', 'G', 'T', 'C', 'G', 'C', 'G', 'T', 'C', 'G', 'A', 'C', 'A', 'C', 'G',
             'A', 'G', 'A', 'T', 'G', 'T', 'A', 'G', 'C', 'A', 'T', 'A', 'C', 'G', 'T', 'G', 'T', 'C', 'A', 'G', 'A',
             'T', 'G', 'T', 'G', 'C', 'A', 'G', 'C', 'A', 'T', 'A', 'T', 'C', 'A', 'T', 'G', 'C', 'T', 'G', 'A', 'G',
             'A', 'G', 'A', 'G', 'C', 'A', 'G', 'C', 'A', 'T', 'A', 'T', 'G', 'A', 'G', 'C', 'G', 'T', 'C', 'A', 'C',
             'T', 'A', 'T', 'C', 'A', 'T', 'G', 'C', 'T', 'C', 'G', 'A', 'T', 'A', 'T', 'C', 'A', 'T']
        ])

    def test_sequence_to_list(self):
        self.tool.bit_size = 640
        bit_segments = self.tool.carbon_to_silicon([
            ['T', 'C', 'G', 'T', 'G', 'T', 'G', 'T', 'G', 'C', 'A', 'G', 'T', 'C', 'T', 'A', 'T', 'G', 'C', 'A', 'G',
             'A', 'G', 'A', 'G', 'C', 'A', 'T', 'C', 'A', 'C', 'A', 'G', 'T', 'C', 'G', 'A', 'T', 'C', 'A', 'G', 'C',
             'T', 'C', 'A', 'T', 'G', 'C', 'A', 'T', 'G', 'A', 'C', 'A', 'C', 'T', 'G', 'T', 'G', 'A', 'G', 'C', 'T',
             'C', 'G', 'C', 'G', 'T', 'C', 'A', 'C', 'A', 'C', 'G', 'T', 'G', 'A', 'C', 'A', 'T', 'A', 'G', 'A', 'G',
             'A', 'T', 'A', 'T', 'G', 'A', 'G', 'C', 'T', 'G', 'A', 'T', 'A', 'G', 'C', 'T', 'G', 'C'],
            ['G', 'C', 'G', 'C', 'A', 'G', 'C', 'G', 'T', 'A', 'G', 'C', 'G', 'T', 'C', 'G', 'A', 'T', 'G', 'C', 'G',
             'T', 'C', 'G', 'T', 'C', 'G', 'C', 'G', 'T', 'G', 'T', 'A', 'T', 'C', 'G', 'A', 'C', 'G', 'C', 'A', 'T',
             'C', 'T', 'C', 'A', 'G', 'A', 'T', 'C', 'G', 'T', 'G', 'A', 'T', 'A', 'C', 'T', 'A', 'C', 'T', 'G', 'T',
             'A', 'G', 'C', 'G', 'T', 'A', 'T', 'A', 'G', 'C', 'G', 'A', 'G', 'A', 'T', 'G', 'C', 'A', 'T', 'G', 'A',
             'T', 'C', 'G', 'T', 'C', 'G', 'A', 'T', 'G', 'C', 'T', 'C', 'G', 'A', 'G', 'C', 'A', 'C'],
            ['C', 'G', 'A', 'T', 'A', 'T', 'C', 'G', 'A', 'C', 'G', 'C', 'T', 'G', 'T', 'G', 'C', 'A', 'T', 'A', 'C',
             'G', 'T', 'C', 'T', 'G', 'C', 'G', 'T', 'A', 'C', 'T', 'C', 'T', 'A', 'G', 'A', 'G', 'A', 'T', 'A', 'C',
             'A', 'G', 'A', 'G', 'A', 'G', 'A', 'T', 'C', 'A', 'T', 'G', 'A', 'G', 'T', 'A', 'G', 'C', 'T', 'A', 'T',
             'G', 'C', 'T', 'A', 'T', 'C', 'T', 'G', 'A', 'G', 'A', 'C', 'T', 'C', 'G', 'C', 'G', 'T', 'C', 'G', 'T',
             'A', 'T', 'C', 'A', 'C', 'G', 'A', 'G', 'A', 'C', 'T', 'A', 'C', 'T', 'C', 'G', 'C', 'T', 'A'],
            ['G', 'A', 'C', 'A', 'G', 'C', 'T', 'G', 'T', 'C', 'G', 'C', 'G', 'T', 'C', 'G', 'A', 'C', 'A', 'C', 'G',
             'A', 'G', 'A', 'T', 'G', 'T', 'A', 'G', 'C', 'A', 'T', 'A', 'C', 'G', 'T', 'G', 'T', 'C', 'A', 'G', 'A',
             'T', 'G', 'T', 'G', 'C', 'A', 'G', 'C', 'A', 'T', 'A', 'T', 'C', 'A', 'T', 'G', 'C', 'T', 'G', 'A', 'G',
             'A', 'G', 'A', 'G', 'C', 'A', 'G', 'C', 'A', 'T', 'A', 'T', 'G', 'A', 'G', 'C', 'G', 'T', 'C', 'A', 'C',
             'T', 'A', 'T', 'C', 'A', 'T', 'G', 'C', 'T', 'C', 'G', 'A', 'T', 'A', 'T', 'C', 'A', 'T']
        ]).get("bit")

        self.assertEqual(bit_segments, self.test_list)
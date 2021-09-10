import random
import unittest

from Chamaeleo.methods.fixed import Church


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = Church(need_logs=False)
        self.tool.segment_length = 160
        self.test_list = [[random.randint(0, 1) for _ in range(160)] for _ in range(4)]

    def test_list_to_sequence(self):
        dna_sequences = self.tool.silicon_to_carbon(self.test_list, 160 * 4).get("dna")
        self.assertEqual(dna_sequences, [
            ['T', 'C', 'C', 'T', 'C', 'G', 'G', 'A', 'A', 'T', 'A', 'A', 'A', 'C', 'C', 'T', 'G', 'C', 'T', 'A', 'C',
             'G', 'T', 'A', 'T', 'C', 'G', 'T', 'C', 'T', 'G', 'G', 'C', 'C', 'C', 'G', 'C', 'C', 'G', 'T', 'C', 'A',
             'G', 'T', 'G', 'G', 'T', 'C', 'C', 'C', 'G', 'G', 'T', 'G', 'T', 'G', 'A', 'A', 'C', 'G', 'G', 'A', 'C',
             'G', 'T', 'T', 'G', 'G', 'G', 'T', 'T', 'T', 'G', 'C', 'A', 'T', 'G', 'A', 'A', 'A', 'G', 'C', 'T', 'T',
             'A', 'T', 'C', 'A', 'G', 'G', 'T', 'T', 'C', 'C', 'G', 'A', 'G', 'C', 'A', 'G', 'G', 'A', 'A', 'G', 'A',
             'T', 'C', 'T', 'G', 'C', 'T', 'T', 'A', 'T', 'T', 'C', 'T', 'G', 'T', 'A', 'A', 'C', 'G', 'T', 'G', 'A',
             'A', 'C', 'T', 'A', 'C', 'G', 'C', 'C', 'C', 'G', 'A', 'A', 'T', 'T', 'C', 'G', 'A', 'C', 'A', 'A', 'A',
             'G', 'A', 'A', 'G', 'C', 'A', 'C', 'T', 'G', 'C', 'G', 'A', 'T'],
            ['T', 'A', 'G', 'T', 'C', 'G', 'T', 'A', 'T', 'T', 'C', 'G', 'A', 'C', 'A', 'T', 'C', 'C', 'A', 'C', 'T',
             'T', 'C', 'A', 'G', 'C', 'T', 'T', 'G', 'G', 'G', 'A', 'C', 'C', 'C', 'A', 'C', 'A', 'A', 'T', 'C', 'G',
             'A', 'G', 'G', 'T', 'C', 'C', 'C', 'A', 'G', 'G', 'T', 'A', 'G', 'A', 'T', 'A', 'C', 'G', 'G', 'A', 'G',
             'G', 'T', 'C', 'A', 'A', 'G', 'A', 'G', 'A', 'T', 'G', 'G', 'A', 'C', 'G', 'C', 'T', 'T', 'C', 'C', 'A',
             'C', 'C', 'G', 'T', 'C', 'A', 'A', 'A', 'C', 'A', 'A', 'G', 'C', 'A', 'C', 'C', 'G', 'G', 'A', 'A', 'T',
             'A', 'T', 'C', 'T', 'A', 'A', 'C', 'T', 'T', 'A', 'C', 'C', 'A', 'A', 'A', 'G', 'A', 'G', 'A', 'C', 'T',
             'C', 'G', 'G', 'T', 'T', 'C', 'C', 'G', 'A', 'C', 'G', 'G', 'T', 'C', 'G', 'C', 'G', 'G', 'A', 'A', 'A',
             'C', 'A', 'G', 'G', 'T', 'C', 'C', 'A', 'C', 'C', 'C', 'G', 'C'],
            ['T', 'A', 'A', 'T', 'G', 'T', 'C', 'T', 'C', 'A', 'T', 'T', 'G', 'G', 'T', 'G', 'G', 'G', 'A', 'A', 'T',
             'G', 'C', 'A', 'A', 'A', 'G', 'G', 'G', 'T', 'A', 'G', 'T', 'A', 'G', 'G', 'T', 'A', 'T', 'T', 'T', 'G',
             'T', 'G', 'G', 'C', 'T', 'T', 'C', 'C', 'G', 'G', 'A', 'C', 'G', 'C', 'T', 'C', 'A', 'T', 'A', 'A', 'C',
             'T', 'A', 'G', 'G', 'T', 'T', 'A', 'T', 'G', 'G', 'G', 'T', 'C', 'A', 'C', 'A', 'C', 'C', 'A', 'C', 'C',
             'A', 'T', 'G', 'T', 'C', 'C', 'G', 'A', 'G', 'T', 'C', 'T', 'A', 'A', 'A', 'G', 'G', 'G', 'T', 'A', 'C',
             'C', 'G', 'C', 'A', 'T', 'T', 'A', 'T', 'C', 'T', 'A', 'A', 'T', 'T', 'T', 'A', 'T', 'A', 'C', 'T', 'C',
             'C', 'G', 'G', 'C', 'C', 'C', 'A', 'A', 'T', 'T', 'G', 'G', 'G', 'A', 'T', 'G', 'G', 'C', 'G', 'G', 'G',
             'A', 'C', 'G', 'T', 'T', 'G', 'C', 'T', 'T', 'C', 'A', 'T', 'C'],
            ['C', 'T', 'T', 'A', 'G', 'G', 'A', 'G', 'T', 'A', 'G', 'C', 'C', 'C', 'G', 'T', 'T', 'G', 'T', 'C', 'C',
             'C', 'G', 'A', 'T', 'C', 'T', 'G', 'T', 'G', 'C', 'C', 'C', 'G', 'T', 'C', 'C', 'C', 'A', 'G', 'C', 'T',
             'T', 'A', 'G', 'A', 'G', 'C', 'T', 'C', 'C', 'T', 'C', 'T', 'A', 'G', 'G', 'C', 'T', 'G', 'C', 'T', 'C',
             'A', 'C', 'C', 'C', 'A', 'A', 'C', 'T', 'A', 'C', 'C', 'A', 'C', 'T', 'C', 'T', 'G', 'T', 'G', 'G', 'A',
             'T', 'C', 'T', 'A', 'G', 'T', 'T', 'C', 'A', 'T', 'A', 'A', 'C', 'A', 'A', 'T', 'C', 'C', 'G', 'G', 'T',
             'C', 'G', 'C', 'T', 'C', 'T', 'A', 'G', 'C', 'A', 'T', 'G', 'C', 'T', 'C', 'A', 'C', 'A', 'A', 'T', 'G',
             'A', 'A', 'T', 'C', 'C', 'G', 'A', 'A', 'T', 'C', 'G', 'A', 'T', 'A', 'T', 'G', 'G', 'T', 'A', 'A', 'T',
             'G', 'A', 'G', 'G', 'C', 'A', 'A', 'T', 'C', 'G', 'G', 'T', 'G']
        ])

    def test_sequence_to_list(self):
        self.tool.bit_size = 640
        bit_segments = self.tool.carbon_to_silicon([
            ['T', 'C', 'C', 'T', 'C', 'G', 'G', 'A', 'A', 'T', 'A', 'A', 'A', 'C', 'C', 'T', 'G', 'C', 'T', 'A', 'C',
             'G', 'T', 'A', 'T', 'C', 'G', 'T', 'C', 'T', 'G', 'G', 'C', 'C', 'C', 'G', 'C', 'C', 'G', 'T', 'C', 'A',
             'G', 'T', 'G', 'G', 'T', 'C', 'C', 'C', 'G', 'G', 'T', 'G', 'T', 'G', 'A', 'A', 'C', 'G', 'G', 'A', 'C',
             'G', 'T', 'T', 'G', 'G', 'G', 'T', 'T', 'T', 'G', 'C', 'A', 'T', 'G', 'A', 'A', 'A', 'G', 'C', 'T', 'T',
             'A', 'T', 'C', 'A', 'G', 'G', 'T', 'T', 'C', 'C', 'G', 'A', 'G', 'C', 'A', 'G', 'G', 'A', 'A', 'G', 'A',
             'T', 'C', 'T', 'G', 'C', 'T', 'T', 'A', 'T', 'T', 'C', 'T', 'G', 'T', 'A', 'A', 'C', 'G', 'T', 'G', 'A',
             'A', 'C', 'T', 'A', 'C', 'G', 'C', 'C', 'C', 'G', 'A', 'A', 'T', 'T', 'C', 'G', 'A', 'C', 'A', 'A', 'A',
             'G', 'A', 'A', 'G', 'C', 'A', 'C', 'T', 'G', 'C', 'G', 'A', 'T'],
            ['T', 'A', 'G', 'T', 'C', 'G', 'T', 'A', 'T', 'T', 'C', 'G', 'A', 'C', 'A', 'T', 'C', 'C', 'A', 'C', 'T',
             'T', 'C', 'A', 'G', 'C', 'T', 'T', 'G', 'G', 'G', 'A', 'C', 'C', 'C', 'A', 'C', 'A', 'A', 'T', 'C', 'G',
             'A', 'G', 'G', 'T', 'C', 'C', 'C', 'A', 'G', 'G', 'T', 'A', 'G', 'A', 'T', 'A', 'C', 'G', 'G', 'A', 'G',
             'G', 'T', 'C', 'A', 'A', 'G', 'A', 'G', 'A', 'T', 'G', 'G', 'A', 'C', 'G', 'C', 'T', 'T', 'C', 'C', 'A',
             'C', 'C', 'G', 'T', 'C', 'A', 'A', 'A', 'C', 'A', 'A', 'G', 'C', 'A', 'C', 'C', 'G', 'G', 'A', 'A', 'T',
             'A', 'T', 'C', 'T', 'A', 'A', 'C', 'T', 'T', 'A', 'C', 'C', 'A', 'A', 'A', 'G', 'A', 'G', 'A', 'C', 'T',
             'C', 'G', 'G', 'T', 'T', 'C', 'C', 'G', 'A', 'C', 'G', 'G', 'T', 'C', 'G', 'C', 'G', 'G', 'A', 'A', 'A',
             'C', 'A', 'G', 'G', 'T', 'C', 'C', 'A', 'C', 'C', 'C', 'G', 'C'],
            ['T', 'A', 'A', 'T', 'G', 'T', 'C', 'T', 'C', 'A', 'T', 'T', 'G', 'G', 'T', 'G', 'G', 'G', 'A', 'A', 'T',
             'G', 'C', 'A', 'A', 'A', 'G', 'G', 'G', 'T', 'A', 'G', 'T', 'A', 'G', 'G', 'T', 'A', 'T', 'T', 'T', 'G',
             'T', 'G', 'G', 'C', 'T', 'T', 'C', 'C', 'G', 'G', 'A', 'C', 'G', 'C', 'T', 'C', 'A', 'T', 'A', 'A', 'C',
             'T', 'A', 'G', 'G', 'T', 'T', 'A', 'T', 'G', 'G', 'G', 'T', 'C', 'A', 'C', 'A', 'C', 'C', 'A', 'C', 'C',
             'A', 'T', 'G', 'T', 'C', 'C', 'G', 'A', 'G', 'T', 'C', 'T', 'A', 'A', 'A', 'G', 'G', 'G', 'T', 'A', 'C',
             'C', 'G', 'C', 'A', 'T', 'T', 'A', 'T', 'C', 'T', 'A', 'A', 'T', 'T', 'T', 'A', 'T', 'A', 'C', 'T', 'C',
             'C', 'G', 'G', 'C', 'C', 'C', 'A', 'A', 'T', 'T', 'G', 'G', 'G', 'A', 'T', 'G', 'G', 'C', 'G', 'G', 'G',
             'A', 'C', 'G', 'T', 'T', 'G', 'C', 'T', 'T', 'C', 'A', 'T', 'C'],
            ['C', 'T', 'T', 'A', 'G', 'G', 'A', 'G', 'T', 'A', 'G', 'C', 'C', 'C', 'G', 'T', 'T', 'G', 'T', 'C', 'C',
             'C', 'G', 'A', 'T', 'C', 'T', 'G', 'T', 'G', 'C', 'C', 'C', 'G', 'T', 'C', 'C', 'C', 'A', 'G', 'C', 'T',
             'T', 'A', 'G', 'A', 'G', 'C', 'T', 'C', 'C', 'T', 'C', 'T', 'A', 'G', 'G', 'C', 'T', 'G', 'C', 'T', 'C',
             'A', 'C', 'C', 'C', 'A', 'A', 'C', 'T', 'A', 'C', 'C', 'A', 'C', 'T', 'C', 'T', 'G', 'T', 'G', 'G', 'A',
             'T', 'C', 'T', 'A', 'G', 'T', 'T', 'C', 'A', 'T', 'A', 'A', 'C', 'A', 'A', 'T', 'C', 'C', 'G', 'G', 'T',
             'C', 'G', 'C', 'T', 'C', 'T', 'A', 'G', 'C', 'A', 'T', 'G', 'C', 'T', 'C', 'A', 'C', 'A', 'A', 'T', 'G',
             'A', 'A', 'T', 'C', 'C', 'G', 'A', 'A', 'T', 'C', 'G', 'A', 'T', 'A', 'T', 'G', 'G', 'T', 'A', 'A', 'T',
             'G', 'A', 'G', 'G', 'C', 'A', 'A', 'T', 'C', 'G', 'G', 'T', 'G']
        ]).get("bit")

        self.assertEqual(bit_segments, self.test_list)
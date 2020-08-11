import random
import unittest

from Chamaeleo.methods.flowed import YinYangCode


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = YinYangCode(need_logs=False)
        self.tool.index_length = 3
        self.tool.total_count = 4
        self.tool.segment_length = 100
        self.test_list = [list(map(int, list(str(bin(index))[2:].zfill(3))))
                          + [random.randint(0, 1) for _ in range(97)] for index in range(4)]

    def test_list_to_sequence(self):
        dna_sequences = self.tool.silicon_to_carbon(self.test_list, 100 * 4).get("dna")
        self.assertEqual(dna_sequences, [
            ['G', 'T', 'C', 'G', 'G', 'C', 'A', 'G', 'T', 'C', 'C', 'A', 'T', 'A', 'C', 'C', 'A', 'A', 'G', 'A', 'A',
             'T', 'C', 'T', 'A', 'G', 'G', 'G', 'A', 'A', 'C', 'G', 'T', 'G', 'A', 'T', 'T', 'C', 'G', 'T', 'G', 'A',
             'T', 'T', 'C', 'T', 'T', 'C', 'C', 'C', 'G', 'G', 'T', 'C', 'G', 'G', 'A', 'G', 'T', 'T', 'C', 'T', 'G',
             'C', 'C', 'A', 'C', 'C', 'T', 'A', 'T', 'C', 'T', 'T', 'C', 'T', 'T', 'A', 'T', 'T', 'G', 'A', 'T', 'T',
             'G', 'G', 'C', 'A', 'T', 'G', 'A', 'T', 'A', 'A', 'A', 'C', 'A', 'T', 'T', 'T'],
            ['G', 'T', 'G', 'A', 'G', 'G', 'A', 'G', 'C', 'A', 'T', 'G', 'C', 'C', 'C', 'G', 'G', 'G', 'A', 'C', 'C',
             'T', 'G', 'T', 'A', 'C', 'G', 'A', 'T', 'C', 'A', 'T', 'C', 'T', 'A', 'G', 'G', 'T', 'A', 'T', 'G', 'C',
             'T', 'T', 'G', 'A', 'C', 'A', 'C', 'T', 'G', 'G', 'G', 'A', 'A', 'C', 'T', 'A', 'A', 'G', 'G', 'G', 'A',
             'A', 'T', 'G', 'A', 'A', 'A', 'C', 'T', 'A', 'A', 'C', 'A', 'C', 'G', 'T', 'A', 'A', 'G', 'T', 'T', 'A',
             'G', 'A', 'A', 'G', 'A', 'T', 'G', 'C', 'A', 'A', 'C', 'G', 'T', 'C', 'C', 'T']
        ])

    def test_sequence_to_list(self):
        bit_segments = self.tool.carbon_to_silicon([
            ['G', 'T', 'C', 'G', 'G', 'C', 'A', 'G', 'T', 'C', 'C', 'A', 'T', 'A', 'C', 'C', 'A', 'A', 'G', 'A', 'A',
             'T', 'C', 'T', 'A', 'G', 'G', 'G', 'A', 'A', 'C', 'G', 'T', 'G', 'A', 'T', 'T', 'C', 'G', 'T', 'G', 'A',
             'T', 'T', 'C', 'T', 'T', 'C', 'C', 'C', 'G', 'G', 'T', 'C', 'G', 'G', 'A', 'G', 'T', 'T', 'C', 'T', 'G',
             'C', 'C', 'A', 'C', 'C', 'T', 'A', 'T', 'C', 'T', 'T', 'C', 'T', 'T', 'A', 'T', 'T', 'G', 'A', 'T', 'T',
             'G', 'G', 'C', 'A', 'T', 'G', 'A', 'T', 'A', 'A', 'A', 'C', 'A', 'T', 'T', 'T'],
            ['G', 'T', 'G', 'A', 'G', 'G', 'A', 'G', 'C', 'A', 'T', 'G', 'C', 'C', 'C', 'G', 'G', 'G', 'A', 'C', 'C',
             'T', 'G', 'T', 'A', 'C', 'G', 'A', 'T', 'C', 'A', 'T', 'C', 'T', 'A', 'G', 'G', 'T', 'A', 'T', 'G', 'C',
             'T', 'T', 'G', 'A', 'C', 'A', 'C', 'T', 'G', 'G', 'G', 'A', 'A', 'C', 'T', 'A', 'A', 'G', 'G', 'G', 'A',
             'A', 'T', 'G', 'A', 'A', 'A', 'C', 'T', 'A', 'A', 'C', 'A', 'C', 'G', 'T', 'A', 'A', 'G', 'T', 'T', 'A',
             'G', 'A', 'A', 'G', 'A', 'T', 'G', 'C', 'A', 'A', 'C', 'G', 'T', 'C', 'C', 'T']
        ]).get("bit")

        for bit_segment in bit_segments:
            self.assertIn(bit_segment, self.test_list)
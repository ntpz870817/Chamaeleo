"""
Name: Functional testing for HC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of Huffman code transformation
"""

import random
import unittest
import Chamaeleo.methods.hc as hc


class TestEncodeDecode(unittest.TestCase):
    def setUp(self):
        random.seed(30)
        self.tool = hc.HC()
        self.tool._huffman_dict()
        self.tool.segment_length = 120
        self.tool.index_binary_length = 0
        self.test_list = [random.randint(0, 1) for _ in range(120)]

    def test_list_to_sequence(self):
        dna_sequence = self.tool._list_to_sequence(
            self.tool._huffman_compressed(self.test_list)
        )
        self.assertEqual(
            dna_sequence,
            [
                "T", "C", "G", "T", "G", "T", "G", "T", "G", "C",
                "A", "G", "T", "C", "T", "A", "T", "G", "C", "A",
                "G", "A", "G", "A", "G", "C", "A", "T", "C", "A",
                "C", "A", "G", "T", "C", "G", "A", "T", "C", "A",
                "G", "C", "T", "C", "A", "T", "G", "C", "A", "T",
                "G", "A", "C", "A", "C", "T", "G", "T", "G", "A",
                "G", "C", "T", "C", "G", "C", "G", "T", "C", "A",
                "C", "A", "C", "G", "T", "G", "A",
            ],
        )

    def test_sequence_to_list(self):
        binary_list = self.tool._huffman_decompressed(
            self.tool._sequence_to_list(
                [
                    "T", "C", "G", "T", "G", "T", "G", "T", "G", "C",
                    "A", "G", "T", "C", "T", "A", "T", "G", "C", "A",
                    "G", "A", "G", "A", "G", "C", "A", "T", "C", "A",
                    "C", "A", "G", "T", "C", "G", "A", "T", "C", "A",
                    "G", "C", "T", "C", "A", "T", "G", "C", "A", "T",
                    "G", "A", "C", "A", "C", "T", "G", "T", "G", "A",
                    "G", "C", "T", "C", "G", "C", "G", "T", "C", "A",
                    "C", "A", "C", "G", "T", "G", "A",
                ]
            ),
            2,
        )
        self.assertEqual(binary_list, self.test_list)

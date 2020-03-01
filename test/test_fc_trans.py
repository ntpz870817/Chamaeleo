"""
Name: Functional testing for GC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of 256^2 and 47^3 transformation
"""
import random
import unittest
import Chamaeleo.methods.fc as fc


class TestEncodeDecode(unittest.TestCase):
    def setUp(self):
        random.seed(30)
        self.tool = fc.FC(redundancy=0.5)
        self.tool.segment_length = 160
        self.tool.index_binary_length = 0
        self.test_list = [[random.randint(0, 1) for _ in range(160)] for _ in range(4)]

    def test_list_to_sequence(self):
        dna_sequences = self.tool.encode(self.test_list, 320, False)
        self.assertEqual(
            dna_sequences,
            [
                [
                    "A", "G", "G", "A", "A", "G", "G", "G", "A", "A",
                    "A", "G", "A", "A", "A", "A", "C", "G", "C", "G",
                    "T", "C", "T", "C", "G", "A", "G", "A", "A", "T",
                    "C", "G", "T", "A", "G", "C", "G", "G", "T", "T",
                    "G", "C", "G", "A", "A", "T", "T", "A", "G", "A",
                    "C", "G", "C", "T", "A", "T", "C", "C", "G", "C",
                    "A", "T", "G", "T", "G", "C", "C", "A", "T", "C",
                    "C", "T", "C", "C", "A", "T", "C", "T", "T", "C",
                    "G", "A", "A", "A", "C", "T", "C", "C", "T", "A",
                    "A", "T", "G", "G", "G", "A",
                ], [
                    "A", "C", "C", "A", "A", "C", "C", "C", "A", "A",
                    "A", "C", "A", "A", "A", "A", "G", "C", "C", "G",
                    "C", "A", "A", "C", "G", "G", "C", "G", "G", "T",
                    "C", "T", "A", "C", "A", "T", "A", "T", "T", "G",
                    "A", "T", "T", "T", "A", "C", "G", "C", "T", "T",
                    "T", "T", "G", "C", "G", "A", "G", "T", "C", "A",
                    "T", "T", "A", "G", "G", "C", "G", "C", "C", "C",
                    "G", "T", "C", "G", "T", "G", "A", "T", "G", "A",
                    "G", "C", "A", "C", "A", "T", "C", "A", "A", "C",
                    "A", "G", "A", "T", "C", "C"
                ], [
                    "A", "A", "G", "G", "A", "A", "G", "G", "G", "A",
                    "A", "A", "G", "A", "A", "A", "A", "G", "G", "T",
                    "T", "G", "T", "G", "T", "A", "A", "A", "G", "A",
                    "A", "T", "G", "T", "G", "G", "G", "G", "C", "T",
                    "A", "A", "G", "A", "A", "A", "G", "G", "T", "T",
                    "A", "C", "A", "A", "C", "C", "G", "A", "C", "A",
                    "A", "G", "T", "A", "A", "C", "A", "G", "G", "A",
                    "T", "G", "C", "G", "C", "T", "T", "G", "T", "A",
                    "C", "G", "C", "T", "A", "A", "C", "C", "T", "G",
                    "A", "A", "G", "T", "A", "A"
                ], [
                    "A", "A", "C", "C", "A", "A", "C", "C", "C", "A",
                    "A", "A", "C", "A", "A", "A", "G", "T", "C", "G",
                    "T", "C", "A", "C", "A", "A", "T", "A", "G", "T",
                    "T", "G", "A", "A", "A", "C", "C", "C", "T", "A",
                    "A", "T", "G", "G", "G", "C", "G", "T", "G", "A",
                    "G", "G", "T", "G", "C", "C", "G", "A", "A", "T",
                    "A", "A", "A", "C", "A", "A", "T", "A", "G", "G",
                    "G", "A", "T", "A", "A", "A", "G", "G", "C", "C",
                    "T", "G", "C", "A", "T", "G", "G", "T", "A", "A",
                    "C", "T", "A", "A", "A", "G"
                ], [
                    "A", "A", "A", "G", "G", "A", "A", "G", "G", "G",
                    "A", "A", "A", "G", "A", "A", "G", "T", "C", "G",
                    "T", "C", "A", "C", "A", "A", "T", "A", "G", "T",
                    "T", "G", "A", "A", "A", "C", "C", "C", "T", "A",
                    "A", "T", "G", "G", "G", "C", "G", "T", "G", "A",
                    "G", "G", "T", "G", "C", "C", "G", "A", "A", "T",
                    "A", "A", "A", "C", "A", "A", "T", "A", "G", "G",
                    "G", "A", "T", "A", "A", "A", "G", "G", "C", "C",
                    "T", "G", "C", "A", "T", "G", "G", "T", "A", "A",
                    "C", "T", "A", "A", "A", "G"
                ], [
                    "A", "A", "A", "C", "C", "A", "A", "C", "C", "C",
                    "A", "A", "A", "C", "A", "A", "G", "C", "T", "C",
                    "A", "T", "T", "T", "T", "A", "T", "A", "A", "T",
                    "T", "C", "G", "T", "G", "T", "T", "T", "G", "T",
                    "A", "T", "A", "G", "G", "C", "A", "C", "C", "T",
                    "G", "T", "T", "G", "A", "A", "A", "A", "C", "T",
                    "A", "G", "T", "C", "A", "C", "T", "G", "A", "G",
                    "C", "G", "G", "G", "C", "T", "C", "A", "G", "C",
                    "G", "A", "A", "T", "T", "G", "T", "G", "T", "G",
                    "C", "T", "G", "T", "A", "G"
                ],
            ],
        )

    def test_sequence_to_sequence(self):
        self.tool.decode_packets = 4
        binary_lists, size = self.tool.decode(
            [
                [
                    "A", "G", "G", "A", "A", "G", "G", "G", "A", "A",
                    "A", "G", "A", "A", "A", "A", "C", "G", "C", "G",
                    "T", "C", "T", "C", "G", "A", "G", "A", "A", "T",
                    "C", "G", "T", "A", "G", "C", "G", "G", "T", "T",
                    "G", "C", "G", "A", "A", "T", "T", "A", "G", "A",
                    "C", "G", "C", "T", "A", "T", "C", "C", "G", "C",
                    "A", "T", "G", "T", "G", "C", "C", "A", "T", "C",
                    "C", "T", "C", "C", "A", "T", "C", "T", "T", "C",
                    "G", "A", "A", "A", "C", "T", "C", "C", "T", "A",
                    "A", "T", "G", "G", "G", "A",
                ], [
                    "A", "C", "C", "A", "A", "C", "C", "C", "A", "A",
                    "A", "C", "A", "A", "A", "A", "G", "C", "C", "G",
                    "C", "A", "A", "C", "G", "G", "C", "G", "G", "T",
                    "C", "T", "A", "C", "A", "T", "A", "T", "T", "G",
                    "A", "T", "T", "T", "A", "C", "G", "C", "T", "T",
                    "T", "T", "G", "C", "G", "A", "G", "T", "C", "A",
                    "T", "T", "A", "G", "G", "C", "G", "C", "C", "C",
                    "G", "T", "C", "G", "T", "G", "A", "T", "G", "A",
                    "G", "C", "A", "C", "A", "T", "C", "A", "A", "C",
                    "A", "G", "A", "T", "C", "C"
                ], [
                    "A", "A", "G", "G", "A", "A", "G", "G", "G", "A",
                    "A", "A", "G", "A", "A", "A", "A", "G", "G", "T",
                    "T", "G", "T", "G", "T", "A", "A", "A", "G", "A",
                    "A", "T", "G", "T", "G", "G", "G", "G", "C", "T",
                    "A", "A", "G", "A", "A", "A", "G", "G", "T", "T",
                    "A", "C", "A", "A", "C", "C", "G", "A", "C", "A",
                    "A", "G", "T", "A", "A", "C", "A", "G", "G", "A",
                    "T", "G", "C", "G", "C", "T", "T", "G", "T", "A",
                    "C", "G", "C", "T", "A", "A", "C", "C", "T", "G",
                    "A", "A", "G", "T", "A", "A"
                ], [
                    "A", "A", "C", "C", "A", "A", "C", "C", "C", "A",
                    "A", "A", "C", "A", "A", "A", "G", "T", "C", "G",
                    "T", "C", "A", "C", "A", "A", "T", "A", "G", "T",
                    "T", "G", "A", "A", "A", "C", "C", "C", "T", "A",
                    "A", "T", "G", "G", "G", "C", "G", "T", "G", "A",
                    "G", "G", "T", "G", "C", "C", "G", "A", "A", "T",
                    "A", "A", "A", "C", "A", "A", "T", "A", "G", "G",
                    "G", "A", "T", "A", "A", "A", "G", "G", "C", "C",
                    "T", "G", "C", "A", "T", "G", "G", "T", "A", "A",
                    "C", "T", "A", "A", "A", "G"
                ], [
                    "A", "A", "A", "G", "G", "A", "A", "G", "G", "G",
                    "A", "A", "A", "G", "A", "A", "G", "T", "C", "G",
                    "T", "C", "A", "C", "A", "A", "T", "A", "G", "T",
                    "T", "G", "A", "A", "A", "C", "C", "C", "T", "A",
                    "A", "T", "G", "G", "G", "C", "G", "T", "G", "A",
                    "G", "G", "T", "G", "C", "C", "G", "A", "A", "T",
                    "A", "A", "A", "C", "A", "A", "T", "A", "G", "G",
                    "G", "A", "T", "A", "A", "A", "G", "G", "C", "C",
                    "T", "G", "C", "A", "T", "G", "G", "T", "A", "A",
                    "C", "T", "A", "A", "A", "G"
                ], [
                    "A", "A", "A", "C", "C", "A", "A", "C", "C", "C",
                    "A", "A", "A", "C", "A", "A", "G", "C", "T", "C",
                    "A", "T", "T", "T", "T", "A", "T", "A", "A", "T",
                    "T", "C", "G", "T", "G", "T", "T", "T", "G", "T",
                    "A", "T", "A", "G", "G", "C", "A", "C", "C", "T",
                    "G", "T", "T", "G", "A", "A", "A", "A", "C", "T",
                    "A", "G", "T", "C", "A", "C", "T", "G", "A", "G",
                    "C", "G", "G", "G", "C", "T", "C", "A", "G", "C",
                    "G", "A", "A", "T", "T", "G", "T", "G", "T", "G",
                    "C", "T", "G", "T", "A", "G"
                ],
            ],
        )
        self.assertEqual(binary_lists, self.test_list)
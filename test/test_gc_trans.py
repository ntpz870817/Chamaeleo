"""
Name: Functional testing for GC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of 256^2 and 47^3 transformation
"""
import random
import unittest
import Chamaeleo.methods.gc as gc


class TestEncodeDecode(unittest.TestCase):
    def setUp(self):
        random.seed(30)
        self.tool = gc.GC([index for index in range(0, 48)])
        self.tool.segment_length = 160
        self.tool.index_binary_length = 0
        self.test_list = [random.randint(0, 1) for _ in range(160)]

    def test_list_to_motif(self):
        dna_sequence = self.tool._list_to_sequence(self.test_list)
        self.assertEqual(
            dna_sequence,
            [
                "C", "C", "T", "C", "G", "C", "C", "G", "C", "C",
                "G", "C", "C", "C", "A", "A", "C", "A", "A", "A",
                "T", "A", "T", "C", "T", "A", "T", "A", "G", "C",
                "C", "A", "T", "G", "G", "T", "G", "C", "T", "G",
                "C", "T", "A", "G", "T", "C", "G", "T", "T", "T",
                "A", "G", "C", "A", "C", "C", "T", "T", "A", "C",
                "C", "A", "T", "C", "A", "C", "T", "A", "C", "C",
                "C", "G", "C", "C", "G", "T", "A", "T", "T", "G",
                "A", "A", "A", "T", "A", "C", "T", "A", "G", "T",
            ],
        )

    def test_motif_to_list(self):
        binary_list = self.tool._sequence_to_list(
            [
                "C", "C", "T", "C", "G", "C", "C", "G", "C", "C",
                "G", "C", "C", "C", "A", "A", "C", "A", "A", "A",
                "T", "A", "T", "C", "T", "A", "T", "A", "G", "C",
                "C", "A", "T", "G", "G", "T", "G", "C", "T", "G",
                "C", "T", "A", "G", "T", "C", "G", "T", "T", "T",
                "A", "G", "C", "A", "C", "C", "T", "T", "A", "C",
                "C", "A", "T", "C", "A", "C", "T", "A", "C", "C",
                "C", "G", "C", "C", "G", "T", "A", "T", "T", "G",
                "A", "A", "A", "T", "A", "C", "T", "A", "G", "T",
            ]
        )
        self.assertEqual(binary_list, self.test_list)
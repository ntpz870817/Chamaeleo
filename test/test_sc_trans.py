"""
Name: Functional testing for SC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of Simple code transformation
"""
import random
import unittest
import Chamaeleo.methods.sc as sc


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.tool = sc.SC(mapping_rule=[0, 1, 1, 0])
        self.test_list = [random.randint(0, 1) for _ in range(120)]

    def test_list_to_sequence(self):
        dna_sequence = self.tool._list_to_sequence(self.test_list)
        self.assertEqual(
            dna_sequence,
            [
                "C", "A", "T", "G", "T", "C", "C", "A", "T", "C",
                "A", "T", "A", "A", "A", "C", "G", "A", "C", "T",
                "T", "C", "G", "A", "C", "A", "C", "C", "T", "C",
                "C", "G", "A", "A", "A", "C", "T", "T", "C", "G",
                "A", "T", "G", "C", "G", "G", "C", "T", "T", "A",
                "G", "G", "C", "G", "C", "C", "A", "T", "A", "C",
                "C", "A", "T", "G", "C", "C", "G", "C", "G", "G",
                "G", "C", "G", "T", "A", "C", "C", "A", "A", "A",
                "C", "A", "C", "G", "A", "G", "A", "T", "G", "G",
                "C", "C", "A", "A", "G", "T", "G", "A", "T", "C",
                "G", "A", "A", "G", "T", "C", "T", "G", "G", "A",
                "C", "C", "T", "C", "G", "A", "G", "G", "G", "A"
            ],
        )

    def test_sequence_to_list(self):
        binary_list = self.tool._sequence_to_list(
            [
                "C", "A", "T", "G", "T", "C", "C", "A", "T", "C",
                "A", "T", "A", "A", "A", "C", "G", "A", "C", "T",
                "T", "C", "G", "A", "C", "A", "C", "C", "T", "C",
                "C", "G", "A", "A", "A", "C", "T", "T", "C", "G",
                "A", "T", "G", "C", "G", "G", "C", "T", "T", "A",
                "G", "G", "C", "G", "C", "C", "A", "T", "A", "C",
                "C", "A", "T", "G", "C", "C", "G", "C", "G", "G",
                "G", "C", "G", "T", "A", "C", "C", "A", "A", "A",
                "C", "A", "C", "G", "A", "G", "A", "T", "G", "G",
                "C", "C", "A", "A", "G", "T", "G", "A", "T", "C",
                "G", "A", "A", "G", "T", "C", "T", "G", "G", "A",
                "C", "C", "T", "C", "G", "A", "G", "G", "G", "A"
            ],
        )
        self.assertEqual(binary_list, self.test_list)
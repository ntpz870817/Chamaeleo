import random
import unittest

from Chamaeleo.methods.components.inherent import index_base
from Chamaeleo.methods.components import validity


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.max_homopolymer = 3
        self.repeat_length = 4
        self.max_content = 0.6
        self.sequences = ["".join([index_base.get(random.randint(0, 3)) for _ in range(24)]) for _ in range(50)]

    def test_homopolymer(self):
        results = []
        for sequence in self.sequences:
            results.append(validity.homopolymer(sequence, self.max_homopolymer))
        self.assertEqual(
            results,
            [
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                True,
                False,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                True,
                True,
                True,
                True,
                False,
                False,
                False,
                True,
                True
            ]
        )

    def test_cg_content(self):
        results = []
        for sequence in self.sequences:
            results.append(validity.cg_content(sequence, self.max_content))

        self.assertEqual(
            results,
            [
                False,
                False,
                True,
                True,
                True,
                True,
                True,
                False,
                True,
                True,
                True,
                False,
                False,
                True,
                False,
                False,
                False,
                True,
                False,
                True,
                False,
                True,
                True,
                True,
                False,
                False,
                True,
                True,
                True,
                False,
                False,
                True,
                True,
                False,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                True,
                False,
                False,
                True,
                True,
                False
            ]
        )
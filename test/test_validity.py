import random
import unittest

from Chamaeleo.methods.components.inherent import index_base

from Chamaeleo.methods.components import validity


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.max_homopolymer = 2
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
                False,
                False,
                True,
                True,
                True,
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                True,
                False,
                False,
                True,
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
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
                False,
                False,
                False,
                False,
                False
            ]
        )

    def test_simple_repeat(self):
        results = []
        for sequence in self.sequences:
            results.append(validity.motif_repeat(sequence, self.repeat_length))

        self.assertEqual(
            results,
            [
                True,
                True,
                False,
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
                True,
                False,
                True,
                True,
                True,
                True,
                True,
                False,
                True,
                True,
                True
            ]
        )

    def test_inverse_repeat(self):
        results = []
        for sequence in self.sequences:
            results.append(validity.inverse_motif_repeat(sequence, self.repeat_length))

        self.assertEqual(
            results,
            [
                False,
                True,
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False
            ]
        )

    def test_dyad_repeat(self):
        results = []
        for sequence in self.sequences:
            results.append(validity.dyad_motif_repeat(sequence, self.repeat_length))

        self.assertEqual(
            results,
            [
                False,
                True,
                True,
                False,
                True,
                False,
                True,
                True,
                True,
                False,
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
                False,
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
                False,
                False,
                False
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


t = TestEncodeDecode()
t.setUp()
t.test_homopolymer()
t.test_simple_repeat()
t.test_inverse_repeat()
t.test_dyad_repeat()
t.test_cg_content()
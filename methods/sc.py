"""
Name: Simple Codec (Simple DNA Storage Code)

Reference:
Church G M, Gao Y, Kosuri S. Next-generation digital information storage in DNA[J]. Science, 2012, 337(6102): 1628-1628.

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s):
(1) DNA encoding by Simple.
(2) DNA decoding by Simple.
"""
import random
import sys

import Chamaeleo.utils.monitor as monitor
import Chamaeleo.utils.log as log
import Chamaeleo.methods.components.inherent as inherent


# noinspection PyMethodMayBeStatic,PyProtectedMember
class SC:
    def __init__(self, mapping_rule=None):
        """
        introduction: The initialization method of Simple Codec.

        :param mapping_rule: Mapping between bases and numbers.
                              There can be two settings:
                              (1) Two bases correspond to a number (0 or 1): i.e. AT-0, CG-1.
                              (2) Each base corresponds to a number: i.e. A-00, T-01, C-10, G-11.
        """

        if not mapping_rule:
            mapping_rule = [0, 1, 1, 0]

        self.mapping_rule = mapping_rule

        self._init_check()

        self.file_size = 0
        self.m = monitor.Monitor()

    def _init_check(self):
        """
        introduction: The verification of initialization parameters.
        """
        if 0 <= min(self.mapping_rule) and max(self.mapping_rule) <= 1:
            if self.mapping_rule.count(0) != 2 or self.mapping_rule.count(1) != 2:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Mapping rule is wrong!")
        else:
            if (0 not in self.mapping_rule) or (1 not in self.mapping_rule) \
                    or (2 not in self.mapping_rule) or (3 not in self.mapping_rule):
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Mapping rule is wrong!")

    # ================================================= encode part ====================================================

    def encode(self, matrix, size, need_log=False):
        """
        introduction: Encode DNA sequences from the data of binary file.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        Type: int or bit.

        :param size: This refers to file size, to reduce redundant bits when transferring DNA to binary files.
                      Type: int

        :param need_log: Show the log.

        :return dna_sequences: The DNA sequence of len(matrix) rows.
                               Type: list(string).
        """
        self.file_size = size

        self.m.restore()

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Encode the matrix by Simple Codec.")

        dna_sequences = []
        for row in range(len(matrix)):
            if need_log:
                self.m.output(row, len(matrix))
            dna_sequences.append(self._list_to_sequence(matrix[row]))

        return dna_sequences

    def _list_to_sequence(self, one_list):
        """
        introduction: from one binary list to DNA sequence.

        :param one_list: One binary list.
                          Type: int or bit.

        :return dna_sequence: One DNA sequence.
                              Type: List(char).
        """
        dna_sequence = []
        if 3 in self.mapping_rule:
            # unlimited mapping rule.
            if len(one_list) % 2 != 0:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Data length cannot be odd number!")
            for index in range(0, len(one_list), 2):
                dna_sequence.append(inherent.index_base.get(self.mapping_rule.index(one_list[index] * 2
                                                                                    + one_list[index + 1])))
        else:
            for index in range(len(one_list)):
                options = [position for position, value in enumerate(self.mapping_rule) if value == one_list[index]]
                sliding_window = dna_sequence[-3:]
                if len(sliding_window) == 3 and len(set(sliding_window)) == 1:
                    bases = list(map(inherent.index_base.get, options))
                    for base in bases:
                        if base != sliding_window[0]:
                            dna_sequence.append(base)
                            break
                else:
                    dna_sequence.append(inherent.index_base.get(random.choice(options)))
        return dna_sequence

    # ================================================= decode part ====================================================

    def decode(self, dna_sequences, need_log=False):
        """
        introduction: Decode DNA sequences to the data of binary file.

        :param dna_sequences: The DNA sequence of len(matrix) rows.
                              Type: One-dimensional list(string).

        :param need_log: Show the log.

        :return matrix: The binary matrix corresponding to the DNA sequences.
                         Type: Two-dimensional list(int).

        :return file_size: This refers to file size, to reduce redundant bits when transferring DNA to binary files.
                            Type: int
        """
        self.m.restore()

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Convert DNA sequences to binary matrix by Simple Codec.")

        matrix = []
        for index in range(len(dna_sequences)):
            if need_log:
                self.m.output(index, len(dna_sequences))
            matrix.append(self._sequence_to_list(dna_sequences[index]))

        self.m.restore()
        return matrix, self.file_size

    def _sequence_to_list(self, dna_sequence):
        """
        introduction: Convert one DNA sequence to one binary list.

        :param dna_sequence: One DNA sequence.
                           Type: String.

        :return one_list: The binary list corresponding to the DNA sequence.
                           Type: One-dimensional list(int).
        """
        one_list = []
        if max(self.mapping_rule) == 3:
            for index in range(len(dna_sequence)):
                number = self.mapping_rule[inherent.base_index.get(dna_sequence[index])]
                one_list.append(1 if number >= 2 else 0)
                one_list.append(1 if number % 2 == 1 else 0)
        else:
            for index in range(len(dna_sequence)):
                one_list.append(self.mapping_rule[inherent.base_index.get(dna_sequence[index])])

        return one_list

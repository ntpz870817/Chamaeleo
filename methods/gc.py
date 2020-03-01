"""
Name: Grass Codec (DNA Storage Code created by Grass)

Reference:
Grass R N, Heckel R, Puddu M, et al. Robust Chemical Preservation of Digital Information on DNA in Silica with Error‐Correcting Codes[J]. Angewandte Chemie International Edition, 2015, 54(8): 2552-2555.

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s):
(1) DNA encoding by Grass Codec.
(2) DNA decoding by Grass Codec.
"""

import sys

import Chamaeleo.methods.components.inherent as inherent
import Chamaeleo.utils.monitor as monitor
import Chamaeleo.utils.log as log


# noinspection PyMethodMayBeStatic,PyProtectedMember,PyTypeChecker,PyUnusedLocal
class GC:
    def __init__(self, base_values=None, need_log=False):
        """
        introduction: The initialization method of Grass Codec.

        :param base_values: Assignment of 48 base triplets (0-47).
                             Other values and their corresponding triplets will be discarded.
                             One-dimensional list containing all values of 0-46, 47 will be discarded.
        """

        if base_values is None:
            base_values = [index for index in range(48)]

        temp_keys = []
        temp_values = []
        for index in range(len(base_values)):
            if 0 <= base_values[index] < 47:
                temp_keys.append(inherent.gc_codes[index])
                temp_values.append(base_values[index])

        self.mapping_rule = [temp_keys, temp_values]
        self.segment_length = 0
        self.file_size = 0
        self.m = monitor.Monitor()

    # ================================================= encode part ====================================================

    def encode(self, matrix, size, need_log=False):
        """
        introduction: Encode DNA sequences from the data of binary file.

        :param matrix: Generated binary two-dimensional matrix.
                        The data of this matrix contains only 0 or 1 (non-char).
                        The length of col should be a multiple of 16.
                        Type: int or bit.

        :param size: This refers to file size, to reduce redundant bits when transferring DNA to binary files.
                      Type: int

        :param need_log: show the log.

        :return dna_sequences: The DNA sequence of len(matrix) rows.
                             Type: list(string).
        """

        self.file_size = size
        self.segment_length = len(matrix[0])
        self.m.restore()

        if self.segment_length % 16 != 0:
            temp_matrix = []
            for row in range(len(matrix)):
                temp_matrix.append([0 for col in range(16 - (self.segment_length % 16))] + matrix[row])
            matrix = temp_matrix

        dna_sequences = []

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Encode the matrix by Grass Codec.")

        for row in range(len(matrix)):
            if need_log:
                self.m.output(row, len(matrix))
            dna_sequences.append(self._list_to_sequence(matrix[row]))

        self.m.restore()
        return dna_sequences

    def _list_to_sequence(self, one_list):
        """
        introduction: from one binary list to DNA sequence.

        :param one_list: One binary list.
                          Type: int or bit.

        :return dna_sequence: One DNA sequence.
                            Type: list(char).
        """

        dna_sequence = []

        for col in range(0, len(one_list), 16):
            decimal_number = int("".join(list(map(str, one_list[col : col + 16]))), 2)
            third = decimal_number % 47

            decimal_number -= third
            decimal_number /= 47
            second = decimal_number % 47

            decimal_number -= second
            first = decimal_number / 47

            dna_sequence += self.mapping_rule[0][self.mapping_rule[1].index(int(first))]
            dna_sequence += self.mapping_rule[0][self.mapping_rule[1].index(int(second))]
            dna_sequence += self.mapping_rule[0][self.mapping_rule[1].index(int(third))]

        return dna_sequence

    # ================================================= decode part ====================================================

    def decode(self, dna_sequences, need_log=False):
        """
        introduction: Decode DNA sequences to the data of binary file.

        :param dna_sequences: The DNA sequence of len(matrix) rows.
                            The length of each DNA sequences should be a multiple of 9.
                            Type: One-dimensional list(string).

        :return matrix: The binary matrix corresponding to the dna sequences.
                         Type: Two-dimensional list(int).

        :param need_log: show the log.

        :return file_size: This refers to file size, to reduce redundant bits when transferring DNA to binary files.
                            Type: int
        """

        self.m.restore()

        matrix = []

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Convert DNA sequences to binary matrix by Grass Codec.")

        for index in range(len(dna_sequences)):
            if need_log:
                self.m.output(index, len(dna_sequences))
            matrix.append(self._sequence_to_list(dna_sequences[index]))

        self.m.restore()

        if len(matrix[0]) != self.segment_length:
            temp_matrix = []
            for row in range(len(matrix)):
                temp_matrix.append(matrix[row][16 - (self.segment_length % 16):])
            matrix = temp_matrix

        return matrix, self.file_size

    def _sequence_to_list(self, dna_sequence):
        """
        introduction: Convert one DNA sequence to one binary list.

        :param dna_sequence: One DNA sequence.
                           The length of DNA sequence should be a multiple of 9.
                           Type: String.

        :return one_list: The binary list corresponding to the DNA sequence.
                           Type: One-dimensional list(int).
        """

        if len(dna_sequence) % 3 != 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The length of dna sequence should be a multiple of 9!")

        one_list = []

        for index in range(0, len(dna_sequence), 9):
            first = self.mapping_rule[1][self.mapping_rule[0].index("".join(dna_sequence[index: index + 3]))]
            second = self.mapping_rule[1][self.mapping_rule[0].index("".join(dna_sequence[index + 3: index + 6]))]
            third = self.mapping_rule[1][self.mapping_rule[0].index("".join(dna_sequence[index + 6: index + 9]))]

            decimal_number = first
            decimal_number = decimal_number * 47 + second
            decimal_number = decimal_number * 47 + third

            one_list += list(map(int, list(str(bin(decimal_number))[2:].zfill(16))))

        return one_list

"""
Name: YYC (Yin-Yang DNA Storage Code)

Reference:
Ping, Z., Chen, S., Huang, X., Zhu, S., Chai, C., Zhang, H., ... & Yang, H. (2019). Towards Practical and Robust DNA-based Data Archiving by Codec System Named'Yin-Yang'. bioRxiv, 829721.

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s):
(1) DNA encoding by YYC.
(2) DNA decoding by YYC.

Advantages:
(1) High compressibility, maximum compressibility to 1/2 of the original data.
(2) Prevent repetitive motifs, like ATCGATCG...
(3) Increase the number of sequence changes (1,536 cases), increasing data security.
"""
import sys
import numpy

import Chamaeleo.methods.components.inherent as inherent
import Chamaeleo.methods.components.validity as validity
import Chamaeleo.utils.log as log
import Chamaeleo.utils.monitor as monitor


# noinspection PyProtectedMember
# noinspection PyBroadException,PyArgumentList,PyMethodMayBeStatic,PyTypeChecker
class YYC:
    def __init__(
        self,
        base_reference=None,
        current_code_matrix=None,
        support_bases=None,
        support_spacing=0,
        max_ratio=0.8,
        search_count=2
    ):
        """
        introduction: The initialization method of YYC.

        :param base_reference: Correspondence between base and binary data (RULE 1).
        Make sure that Two of the bases are 1 and the other two are 0, so there are only 6 case.

        :param current_code_matrix: Conversion rule between base and binary data based on support base and current base (RULE 2).
                                     Label row is the support base, label col is the current base.
                                         A   T   C   G
                                     A   X1  Y1  X2  Y2
                                     T   X3  Y3  X4  Y4
                                     C   X5  Y5  X6  Y6
                                     G   X7  Y7  X8  Y8
                                     Make sure that Xn + Yn = 1 and Xn * Yn = 0, n is in [1, 8].

        :param support_bases: Base replenishment before official data.
                               Make sure that the count of support base must more than support spacing.
                               Make sure that the number range of each position is {0, 1, 2, 3}, reference base index.

        :param support_spacing: Spacing between support base and current base.
                                 When the support base is the front of the current base, the spacing is 0.

        :param max_ratio: The max ratio of 0 or 1.
                           When the (count/length) >= this parameter, we decide that this binary sequence is not good.

        """

        # Set default values for Rules 1 and 2 (RULE 495)
        if not base_reference:
            base_reference = [0, 1, 0, 1]
        if not current_code_matrix:
            current_code_matrix = [
                [1, 1, 0, 0],
                [1, 0, 0, 1],
                [1, 1, 0, 0],
                [1, 1, 0, 0],
            ]
        if not support_bases:
            support_bases = [inherent.index_base.get(0)]

        # Assign input data to class variables
        self.base_reference = base_reference
        self.current_code_matrix = current_code_matrix
        self.support_bases = support_bases
        self.support_spacing = support_spacing
        self.max_ratio = max_ratio
        self.search_count = search_count

        # Detect parameters correctness
        self._init_check()

        self.file_size = 0
        self.monitor = monitor.Monitor()

    def _init_check(self):
        """
        introduction: The verification of initialization parameters.

        """
        # Check support bases
        for index in range(len(self.support_bases)):
            if (self.support_bases[index] != "A" and self.support_bases[index] != "T"
                    and self.support_bases[index] != "C" and self.support_bases[index] != "G"):
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Only A, T, C, and G can be included as support bases, "
                           "but the support bases[" + str(index) + "] has been detected as "
                           + str(self.support_bases[index] + "!"))

        if len(self.support_bases) < self.support_spacing + 1:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The count of support base needs to be more than support spacing!")

        # Check base reference (rule 1)
        for index in range(len(self.base_reference)):
            if self.base_reference[index] != 0 and self.base_reference[index] != 1:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Only 0 and 1 can be included for base reference, and base_reference[" + str(index)
                           + "] has been detected as " + str(self.base_reference[index] + "!"))
        if sum(self.base_reference) != 2:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "Wrong correspondence between base and binary data!")

        positions = []
        for i in range(len(self.base_reference)):
            if self.base_reference[i] == 1:
                positions.append(i)
        for i in range(len(self.base_reference)):
            if self.base_reference[i] != 1:
                positions.append(i)

        # Check current code matrix (rule 2)
        for row in range(len(self.current_code_matrix)):
            for col in range(len(self.current_code_matrix[row])):
                if self.current_code_matrix[row][col] != 0 and self.current_code_matrix[row][col] != 1:
                    log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                               "Only 0 and 1 can be included in the current code matrix, and the current code matrix ["
                               + str(row) + ", " + str(col) + "] has been detected as "
                               + str(self.current_code_matrix[row][col] + "!"))

        for row in range(len(self.current_code_matrix)):
            left = self.current_code_matrix[row][positions[0]]
            right = self.current_code_matrix[row][positions[1]]
            if left + right == 1 and left * right == 0:
                continue
            else:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Wrong current code matrix, the error locations are [" + str(row) + ", " + str(positions[0])
                           + "] and [" + str(row) + ", " + str(positions[1]) + "]! "
                           + "It is required by rule that these two values will have sum of 1 and product of 0.")

            left = self.current_code_matrix[row][positions[2]]
            right = self.current_code_matrix[row][positions[3]]
            if left + right == 1 and left * right == 0:
                continue
            else:
                log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                           "Wrong current code matrix, the error locations are [" + str(row) + ", " + str(positions[2])
                           + "] and [" + str(row) + ", " + str(positions[3]) + "]! "
                           + "It is required by rule that these two values will have sum of 1 and product of 0.")
        # Check max ratio
        if self.max_ratio <= 0.5 or self.max_ratio >= 1:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "Wrong max ratio (" + str(self.max_ratio) + ")!")

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
                             Type: list(list(char)).
        """
        self.file_size = size

        self.monitor.restore()

        good_data_set, bad_data_set = self._divide_library(matrix, need_log)

        self.monitor.restore()

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Random incorporation and validity testing.")

        data_set = self._pairing(good_data_set, bad_data_set, need_log)

        self.monitor.restore()

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Convert to DNA sequence string set.")

        dna_sequences = self._synthesis_sequences(data_set, need_log)

        self.monitor.restore()

        return dna_sequences

    def _divide_library(self, matrix, need_log):
        """
        introduction: Separate 'good' and 'bad' data from total data, and splice index and data as a list.

        :param matrix: Generated binary two-dimensional matrix
                       The data of this matrix contains only 0 or 1 (non-char).
                       Type: int or bit

        :param need_log: Show the log.

        :returns good_data_set, bad datas: 'good' and 'bad' data from total data
                                        Type: list(int)
        """
        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Separate 'good' data from 'bad' data.")

        bad_indexes = []
        for row in range(len(matrix)):
            if numpy.sum(matrix[row]) > len(matrix[row]) * self.max_ratio \
                    or numpy.sum(matrix[row]) < len(matrix[row]) * (1 - self.max_ratio):
                bad_indexes.append(row)

        if len(matrix) < len(bad_indexes) * 5:
            if need_log:
                log.output(log.WARN, str(__name__), str(sys._getframe().f_code.co_name),
                           "There may be a large number of sequences that are difficult for synthesis or sequencing. "
                           + "We recommend you to re-select the rule or take a new run.")

        if len(bad_indexes) == 0 and len(matrix) == 0:
            return [], []
        elif len(bad_indexes) == 0:
            good_data_set = []
            for row in range(len(matrix)):
                if need_log:
                    self.monitor.output(row, len(matrix))
                good_data_set.append(matrix[row])
            return good_data_set, []
        elif len(bad_indexes) == len(matrix):
            bad_data_set = []
            for row in range(len(matrix)):
                if need_log:
                    self.monitor.output(row, len(matrix))
                bad_data_set.append(matrix[row])
            return [], bad_data_set
        else:
            good_data_set = []
            bad_data_set = []
            for row in range(len(matrix)):
                if need_log:
                    self.monitor.output(row, len(matrix))
                if row in bad_indexes:
                    bad_data_set.append(matrix[row])
                else:
                    good_data_set.append(matrix[row])

            return good_data_set, bad_data_set

    def _pairing(self, good_data_set, bad_data_set, need_log):
        """
        introduction: Match 'good' data with 'bad' data, to ensure that the overall data is better.
                      If there are only 'good' or 'bad' data left, they will be selected to pair with each other.

        :param good_data_set: Generated binary two-dimensional matrix, the repetition rate of 0 or 1 is related low.
                            Type: Two-dimensional list(int)

        :param bad_data_set: Generated binary two-dimensional matrix, the repetition rate of 0 or 1 is related high.
                           Type: Two-dimensional list(int)

        :param need_log: Show the log.

        :returns data_set: Matched results
                         Type: Two-dimensional list(int)
        """

        data_set = []
        good_indexes = None
        bad_indexes = None
        if good_data_set is not None and bad_data_set is not None:
            good_indexes = set(str(i) for i in range(len(good_data_set)))
            bad_indexes = set(str(i) for i in range(len(bad_data_set)))
        elif good_data_set is None and bad_data_set is not None:
            good_indexes = set(str(i) for i in range(0))
            bad_indexes = set(str(i) for i in range(len(bad_data_set)))
        elif good_data_set is not None and bad_data_set is None:
            good_indexes = set(str(i) for i in range(len(good_data_set)))
            bad_indexes = set(str(i) for i in range(0))
        else:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "YYC did not receive matrix data!")

        for index in range(0, len(good_data_set) + len(bad_data_set), 2):
            if need_log:
                self.monitor.output(index, len(good_data_set) + len(bad_data_set))
            if index < len(good_data_set) + len(bad_data_set) - 1:
                if len(good_indexes) != 0 and len(bad_indexes) != 0:
                    for search_index in range(self.search_count):
                        good_index = int(good_indexes.pop())
                        bad_index = int(bad_indexes.pop())
                        if search_index >= self.search_count - 1 or validity.check(
                                "".join(self._list_to_sequence(good_data_set[good_index], bad_data_set[bad_index]))):
                            data_set.append(good_data_set[good_index])
                            data_set.append(bad_data_set[bad_index])
                            break
                        else:
                            good_indexes.add(str(good_index))
                            bad_indexes.add(str(bad_index))
                            index -= 1
                elif len(bad_indexes) == 0:
                    for search_index in range(self.search_count):
                        good_index1 = int(good_indexes.pop())
                        good_index2 = int(good_indexes.pop())
                        if search_index >= self.search_count - 1 or validity.check(
                                "".join(self._list_to_sequence(good_data_set[good_index1], good_data_set[good_index2]))):
                            data_set.append(good_data_set[good_index1])
                            data_set.append(good_data_set[good_index2])
                            break
                        else:
                            good_indexes.add(str(good_index1))
                            good_indexes.add(str(good_index2))
                            index -= 1
                elif len(good_indexes) == 0:
                    for search_index in range(self.search_count):
                        bad_index1 = int(bad_indexes.pop())
                        bad_index2 = int(bad_indexes.pop())
                        if search_index >= self.search_count - 1 or validity.check(
                                "".join(self._list_to_sequence(bad_data_set[bad_index1], bad_data_set[bad_index2]))):
                            data_set.append(bad_data_set[bad_index1])
                            data_set.append(bad_data_set[bad_index2])
                        else:
                            bad_indexes.add(str(bad_index1))
                            bad_indexes.add(str(bad_index2))
                            index -= 1
                else:
                    log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                               "Wrong pairing for YYC!")
            else:
                data_set.append(good_data_set[int(good_indexes.pop())]
                                if len(good_indexes) != 0 else bad_data_set[int(bad_indexes.pop())])

        del good_indexes, good_data_set, bad_indexes, bad_data_set

        return data_set

    def _synthesis_sequences(self, data_set, need_log):
        """
        introduction: Synthesis sequences by two-dimensional data set.

        :param data_set: Original data from file.
                       Type: Two-dimensional list(int).

        :param need_log: Show the log.

        :return dna_sequences: The DNA sequences from the original data set
                             Type: One-dimensional list(string).
        """

        dna_sequences = []
        for row in range(0, len(data_set), 2):
            if need_log:
                self.monitor.output(row, len(data_set))
            if row < len(data_set) - 1:
                dna_sequences.append(self._list_to_sequence(data_set[row], data_set[row + 1]))
            else:
                dna_sequences.append(self._list_to_sequence(data_set[row], None))

        del data_set

        return dna_sequences

    def _list_to_sequence(self, upper_list, lower_list):
        """
        introduction: from two binary list to one DNA sequence

        :param upper_list: The upper binary list
                            Type: List(byte)

        :param lower_list: The lower binary list
                            Type: List(byte)

        :return: one DNA sequence
                  Type: List(char)
        """

        dna_sequence = []

        for col in range(len(upper_list)):
            if lower_list is not None:
                if col > self.support_spacing:
                    dna_sequence.append(self._binary_to_base(upper_list[col], lower_list[col],
                                                             dna_sequence[col - (self.support_spacing + 1)]))
                else:
                    dna_sequence.append(self._binary_to_base(upper_list[col], lower_list[col], self.support_bases[col]))
            else:
                if col > self.support_spacing:
                    dna_sequence.append(self._binary_to_base(upper_list[col], upper_list[col],
                                                             dna_sequence[col - (self.support_spacing + 1)]))
                else:
                    dna_sequence.append(self._binary_to_base(upper_list[col], upper_list[col], self.support_bases[col]))
        return dna_sequence

    def _binary_to_base(self, upper_bit, lower_bit, support_base):
        """
        introduction: Get one base from two binary, based on the rules of YYC.

        :param upper_bit: The upper bit, used to identify two of the four bases by RULE 1.

        :param lower_bit: The lower bit, one of the parameters,
                           used to identify one of the two bases by RULE 2, after RULE 1.

        :param support_base: The base for support to get base in current position, one of the parameters,
                              used to identify one of the two bases by RULE 2, after RULE 1.

        :return one_base: The base in current position.
                           Type: int
        """

        current_options = []
        for index in range(len(self.base_reference)):
            if self.base_reference[index] == int(upper_bit):
                current_options.append(index)

        if self.current_code_matrix[inherent.base_index.get(support_base)][current_options[0]] == int(lower_bit):
            one_base = inherent.index_base[current_options[0]]
        else:
            one_base = inherent.index_base[current_options[1]]

        return one_base

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

        if not dna_sequences:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "DNA sequence string set is not existing")

        self.monitor.restore()

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Convert DNA sequences to binary matrix.")

        matrix = self._convert_binaries(dna_sequences, need_log)

        self.monitor.restore()

        return matrix, self.file_size

    def _convert_binaries(self, dna_sequences, need_log):
        """
        introduction: Convert DNA sequences to binary matrix.
                      One DNA sequence <-> two-line binaries.

        :param dna_sequences: The DNA sequence of len(matrix) rows.
                            Type: One-dimensional list(string).

        :param need_log: Show the log.

        :return matrix: The binary matrix corresponding to the DNA sequences.
                         Type: Two-dimensional list(int).
        """

        matrix = []

        for row in range(len(dna_sequences)):
            if need_log:
                self.monitor.output(row, len(dna_sequences))

            upper_row_datas, lower_row_datas = self._sequence_to_list(dna_sequences[row])
            matrix.append(upper_row_datas)

            if upper_row_datas != lower_row_datas:
                matrix.append(lower_row_datas)

        del dna_sequences

        return matrix

    def _sequence_to_list(self, dna_sequence):
        """
        introduction: Convert one DNA sequence to two-line binary list.

        :param dna_sequence: The DNA sequence of len(matrix) rows.
                            Type: One-dimensional list(string).

        :returns upper_row_list, lower_row_list: The binary list corresponding to the DNA sequence.
                                                Type: One-dimensional list(int).
        """

        upper_row_list = []
        lower_row_list = []

        for col in range(len(dna_sequence)):
            if col > self.support_spacing:
                upper_binary, lower_binary = self._base_to_binary(dna_sequence[col],
                                                                  dna_sequence[col - (self.support_spacing + 1)])
                upper_row_list.append(upper_binary)
                lower_row_list.append(lower_binary)
            else:
                upper_binary, lower_binary = self._base_to_binary(dna_sequence[col], self.support_bases[col])
                upper_row_list.append(upper_binary)
                lower_row_list.append(lower_binary)

        return upper_row_list, lower_row_list

    def _base_to_binary(self, current_base, support_base):
        """
        introduction: Get two bit from current base and support base, based on the rules of YYC.

        :param current_base: The upper bit, used to identify the upper bit by RULE 1.

        :param support_base: The base for support to get base in current position, one of the parameters (with current base),
                              used to identify the lower bit by RULE 2.

        :returns upper_bit lower_bit: The upper bit and lower bit.
                                       Type: int, int
        """
        upper_bit = self.base_reference[inherent.base_index[current_base]]
        lower_bit = self.current_code_matrix[inherent.base_index[support_base]][inherent.base_index[current_base]]

        return upper_bit, lower_bit

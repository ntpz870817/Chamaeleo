import random
import re
from Chamaeleo.methods.inherent import *
from Chamaeleo.methods.default import AbstractCodingAlgorithm


class Church(AbstractCodingAlgorithm):

    def __init__(self, need_logs=False):
        super().__init__(need_logs)
        self.carbon_options = [["A", "C"], ["G", "T"]]

        if self.need_logs:
            print("create Church et al. successfully")
            print("Church, G. M., Gao, Y., & Kosuri, S. (2012). "
                  "Next-generation digital information storage in DNA. "
                  "Science, 337(6102), 1628-1628.")

    def __init_check__(self):
        pass

    def encode(self, bit_segments):
        dna_sequences = []

        for segment_index, bit_segment in enumerate(bit_segments):
            dna_sequence = []
            for bit in bit_segment:
                options, window = self.carbon_options[bit], dna_sequence[-3:]
                if len(window) == 3 and len(set(window)) == 1:
                    for option in options:
                        if option != window[0]:
                            dna_sequence.append(option)
                            break
                else:
                    dna_sequence.append(random.choice(options))

            dna_sequences.append(dna_sequence)

            if self.need_logs:
                self.monitor.output(segment_index + 1, len(bit_segments))

        return dna_sequences

    def decode(self, dna_sequences):
        bit_segments = []

        for sequence_index, dna_sequence in enumerate(dna_sequences):
            bit_segment = []
            for nucleotide in dna_sequence:
                for option_index, carbon_option in enumerate(self.carbon_options):
                    if nucleotide in carbon_option:
                        bit_segment.append(option_index)

            bit_segments.append(bit_segment)

            if self.need_logs:
                self.monitor.output(sequence_index + 1, len(dna_sequences))

        return bit_segments


class Goldman(AbstractCodingAlgorithm):

    def __init__(self, fixed_huffman=True, support_nucleotide="A", need_logs=False):
        super().__init__(need_logs)
        self.fixed_huffman = fixed_huffman
        self.support_nucleotide = support_nucleotide
        if self.fixed_huffman:
            self.huffman_tree = goldman_dict
        else:
            self.huffman_tree = None

        self.__init_check__()

        if self.need_logs:
            print("create Goldman et al. successfully")
            print("Goldman, N., Bertone, P., Chen, S., Dessimoz, C., LeProust, E. M., Sipos, B., & Birney, E. (2013). "
                  "Towards practical, high-capacity, low-maintenance information storage in synthesized DNA. "
                  "Nature, 494(7435), 77-80.")

    def __init_check__(self):
        if self.support_nucleotide not in ["A", "C", "G", "T"]:
            raise ValueError("start nucleotide needs to be one of \"A\", \"C\", \"G\", or \"T\"!")

    def encode(self, bit_segments):
        if not self.fixed_huffman:
            print("In this encoding process, the ternary Huffman tree is "
                  + "generated according to the file. Please keep it properly.")
            self.huffman_tree = self.adaptive_huffman_tree(bit_segments, 3)

        dna_sequences = []
        for segment_index, bit_segment in enumerate(bit_segments):

            if not self.fixed_huffman and len(bit_segment) < 24:
                raise ValueError("length of bit segment must greater than or equal to 24!")

            dna_sequence = []

            if len(bit_segment) % 8 != 0:
                raise ValueError("The length of inputted binary segment must be divided by 8!")

            ternary_segment = []
            for position in range(0, len(bit_segment), 8):
                current_number = int("".join(list(map(str, bit_segment[position: position + 8]))), 2)
                huffman_code = self.huffman_tree[current_number]
                for code_index in range(len(huffman_code)):
                    ternary_segment.append(int(huffman_code[code_index]))

            last_nucleotide = self.support_nucleotide
            for value in ternary_segment:
                current_base = rotate_codes.get(last_nucleotide)[value]
                dna_sequence.append(current_base)
                last_nucleotide = current_base

            dna_sequences.append(dna_sequence)

            if self.need_logs:
                self.monitor.output(segment_index + 1, len(bit_segments))

        return dna_sequences

    def decode(self, dna_sequences):
        if self.huffman_tree is None:
            raise ValueError("The Ternary Huffman tree need to be pre-declared!")

        bit_segments = []

        for sequence_index, dna_sequence in enumerate(dna_sequences):
            try:
                last_nucleotide, ternary_segment = self.support_nucleotide, []
                for nucleotide in dna_sequence:
                    ternary_segment.append(rotate_codes.get(last_nucleotide).index(nucleotide))
                    last_nucleotide = nucleotide

                temp_ternary, bit_segment = "", []
                for value in ternary_segment:
                    temp_ternary += str(value)
                    if temp_ternary in self.huffman_tree:
                        tree_index = self.huffman_tree.index(temp_ternary)
                        bit_segment += list(map(int, list(str(bin(tree_index))[2:].zfill(8))))
                        temp_ternary = ""

                bit_segments.append(bit_segment)
            except ValueError:
                pass

            if self.need_logs:
                self.monitor.output(sequence_index + 1, len(dna_sequences))

        return bit_segments

    def adaptive_huffman_tree(self, bit_matrix, size=None, multiple=3):
        """
        introduction: Customize Huffman tree based on the bit matrix.

        :param bit_matrix: Bit matrix, containing only 0,1.
                            Type: Two-dimensional list(int)

        :param size: File size corresponding to the matrix.

        :param multiple: Number of branches constructed (decimal semi-octets).

        :return tree: Byte-based (256) Huffman tree.
        """
        if size is None:
            size = len(bit_matrix) * len(bit_matrix[0])

        # Replace the bit matrix with one-dimensional decimal byte list
        decimal_list = self._get_decimal_list(bit_matrix, size)

        # Store elements and their weights, their codes
        weight, code = {}, {}
        # Recorder, prepare for the following screening of valid keys
        _node = lambda i: "_" + str(i).zfill(3)
        for one_byte in decimal_list:
            # Create weight values for each element
            if _node(one_byte) in weight:
                weight[_node(one_byte)] += 1
            else:
                # Set the initial value of the code
                code[_node(one_byte)] = ""
                weight[_node(one_byte)] = 1

        for one_byte in range(1, multiple - 1):
            # Add impossible elements to ensure normal combination and close as one element
            if (len(weight) - 1) % (multiple - 1) == 0:
                break
            else:
                weight["_" * one_byte] = 0
        weight_list = list(weight.items())

        for index in range(0, (len(weight) - 1) // (multiple - 1)):
            weight_list = sorted(weight_list, key=lambda x: x[0])
            weight_list = sorted(weight_list, key=lambda x: x[1])
            # Combine the previous terms into one term
            item = str(index).zfill(3)
            weight = 0
            # Add Huffman coding and form new combinations
            for branch in range(0, multiple):
                item += weight_list[branch][0]
                weight += weight_list[branch][1]
                # Add headers to each item of the previous items.
                for index_item in re.findall(r"_\d{3}", weight_list[branch][0]):
                    code[index_item] = str(multiple - branch - 1) + code[index_item]
            new = [(item, weight)]
            weight_list = weight_list[multiple:] + new

        # noinspection PyTypeChecker
        dictionary = dict([int(key[1:]), value] for key, value in code.items())

        tree = []
        for index in range(256):
            tree.append(dictionary.get(index))
        return tree

    @staticmethod
    def _get_decimal_list(bit_matrix, size):
        """
        introduction: Decimal list generated by the bit matrix.

        :param bit_matrix: Bit matrix, containing only 0,1.
                            Type: Two-dimensional list(int)

        :param size: File size corresponding to the matrix.

        :return decimal_list: Decimal list.
                              Type: One-dimensional list(int)
        """
        bit_index, temp_byte, decimal_list = 0, 0, []
        for row in range(len(bit_matrix)):
            for col in range(len(bit_matrix[0])):
                bit_index += 1
                temp_byte *= 2
                temp_byte += bit_matrix[row][col]
                if bit_index == 8:
                    if size >= 0:
                        decimal_list.append(int(temp_byte))
                        size -= 1
                    bit_index, temp_byte = 0, 0

        return decimal_list


class Grass(AbstractCodingAlgorithm):

    def __init__(self, base_values=None, need_logs=False):
        super().__init__(need_logs)
        self.base_values = base_values
        self.mapping_rules = [[], []]

        self.__init_check__()

        if need_logs:
            print("create Grass et al. successfully")
            print("Grass, R. N., Heckel, R., Puddu, M., Paunescu, D., & Stark, W. J. (2015). "
                  "Robust chemical preservation of digital information on DNA in silica with error-correcting codes. "
                  "Angewandte Chemie International Edition, 54(8), 2552-2555.")

    def __init_check__(self):
        if self.base_values is None:
            self.base_values = [index for index in range(48)]
        else:
            counts = [0 for _ in range(48)]
            for index, value in enumerate(self.base_values):
                if type(value) is int and (0 <= value < 47):
                    counts[value] += 1
                else:
                    raise ValueError("type of value in \"base_values\" is wrong!")

            if max(counts) != 1 or min(counts) != 1:
                raise ValueError("type of value in \"base_values\" is wrong!")

        for index, value in enumerate(self.base_values):
            if 0 <= self.base_values[index] < 47:
                self.mapping_rules[0].append(gc_codes[index])
                self.mapping_rules[1].append(value)

    def encode(self, bit_segments):
        dna_sequences = []

        for segment_index, bit_segment in enumerate(bit_segments):
            dna_sequence = []

            if len(bit_segment) % 16 != 0:
                raise ValueError("The length of inputted binary segment must be divided by 16!")

            for position in range(0, len(bit_segment), 16):
                decimal_number = int("".join(list(map(str, bit_segment[position: position + 16]))), 2)

                rule_indices = []
                for index in range(3):
                    rule_indices.append(decimal_number % 47)
                    decimal_number -= rule_indices[-1]
                    decimal_number /= 47

                rule_indices = rule_indices[::-1]
                for rule_index in rule_indices:
                    dna_sequence += self.mapping_rules[0][self.mapping_rules[1].index(rule_index)]

            dna_sequences.append(dna_sequence)

            if self.need_logs:
                self.monitor.output(segment_index + 1, len(bit_segments))

        return dna_sequences

    def decode(self, dna_sequences):
        bit_segments = []

        for sequence_index, dna_sequence in enumerate(dna_sequences):
            try:
                bit_segment = []
                for position in range(0, len(dna_sequence), 9):
                    decimal_number, carbon_piece = 0, dna_sequence[position: position + 9]
                    for index in [0, 3, 6]:
                        position = self.mapping_rules[0].index("".join(carbon_piece[index: index + 3]))
                        value = self.mapping_rules[1][position]
                        decimal_number = decimal_number * 47 + value

                    bit_segment += list(map(int, list(str(bin(decimal_number))[2:].zfill(16))))

                bit_segments.append(bit_segment)
            except ValueError:
                pass
            except IndexError:
                pass

            if self.need_logs:
                self.monitor.output(sequence_index + 1, len(dna_sequences))

        return bit_segments


class Blawat(AbstractCodingAlgorithm):

    def __init__(self, need_logs=False):
        super().__init__(need_logs)
        self.first_3 = [[0, 0], [0, 1], [1, 0], [1, 1]]
        self.last_2 = {
            str([0, 0]): ["AA", "CC", "GG", "TT"],
            str([0, 1]): ["AC", "CG", "GT", "TA"],
            str([1, 0]): ["AG", "CT", "GA", "TC"],
            str([1, 1]): ["AT", "CA", "GC", "TG"],
        }
        self.__init_check__()

        if self.need_logs:
            print("create Blawat et al. successfully!")
            print("Blawat, M., Gaedke, K., Huetter, I., Chen, X. M., Turczyk, B., ... & Church, G. M. (2016). "
                  "Forward error correction for DNA data storage. "
                  "Procedia Computer Science, 80, 1011-1022.")

    def __init_check__(self):
        pass

    def encode(self, bit_segments):
        dna_sequences = []

        for segment_index, bit_segment in enumerate(bit_segments):
            dna_sequence = []

            if len(bit_segment) % 8 != 0:
                raise ValueError("The length of inputted binary segment must be divided by 8!")

            for position in range(0, len(bit_segment), 8):
                carbon_piece, silicon_piece = [None] * 5, bit_segment[position: position + 8]
                for index, carbon_position in zip([0, 2, 4], [0, 1, 3]):
                    carbon_piece[carbon_position] = index_base.get(self.first_3.index(silicon_piece[index: index + 2]))

                for last_2_option in self.last_2.get(str(silicon_piece[6: 8])):
                    carbon_piece[2], carbon_piece[4] = last_2_option[0], last_2_option[1]
                    if len(set(carbon_piece[:3])) > 1 and len(set(carbon_piece[3:])) > 1:
                        break

                dna_sequence += carbon_piece

            dna_sequences.append(dna_sequence)

            if self.need_logs:
                self.monitor.output(segment_index + 1, len(bit_segments))

        return dna_sequences

    def decode(self, dna_sequences):
        bit_segments = []

        for sequence_index, dna_sequence in enumerate(dna_sequences):
            bit_segment = []
            for position in range(0, len(dna_sequence), 5):
                carbon_piece, silicon_piece = dna_sequence[position: position + 5], []
                for index in [0, 1, 3]:
                    silicon_piece += self.first_3[base_index.get(carbon_piece[index])]

                combination = carbon_piece[2] + carbon_piece[4]
                for value, options in self.last_2.items():
                    if combination in options:
                        silicon_piece += [int(value[1]), int(value[4])]

                bit_segment += silicon_piece

            bit_segments.append(bit_segment)

            if self.need_logs:
                self.monitor.output(sequence_index + 1, len(dna_sequences))

        return bit_segments

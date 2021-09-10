import random
import sys

import math
import numpy
from collections import defaultdict
from Chamaeleo.methods.default import AbstractCodingAlgorithm
from Chamaeleo.methods.inherent import base_index, index_base
from Chamaeleo.utils import screen


class DNAFountain(AbstractCodingAlgorithm):

    def __init__(self, homopolymer=4, gc_bias=0.2, redundancy=0.07, header_size=4,
                 c_dist=0.1, delta=0.05, recursion_depth=10000000, decode_packets=None, need_pre_check=False,
                 need_logs=False):
        super().__init__(need_logs)
        self.homopolymer = homopolymer
        self.gc_bias = gc_bias
        self.redundancy = redundancy
        self.header_size = header_size
        self.c_dist = c_dist
        self.delta = delta
        self.recursion_depth = recursion_depth
        self.need_pre_check = need_pre_check
        self.prng = None
        self.decode_packets = decode_packets
        # adjust the maximum recursion depth to "self.recursion_depth" in Python.
        sys.setrecursionlimit(self.recursion_depth)

        self.__init_check__()

        if self.need_logs:
            print("Create DNA Fountain successfully")
            print("Erlich, Y., & Zielinski, D. (2017). "
                  "DNA Fountain enables a robust and efficient storage architecture. "
                  "Science, 355(6328), 950-954.")

    def __init_check__(self):
        if self.redundancy <= 0:
            raise ValueError("The parameter \"max_redundancy\" is wrong, it is greater than 0!")

        if self.header_size < 0:
            raise ValueError("The parameter \"header_size\" is wrong, it is greater than or equal to 0!")

        if self.gc_bias < 0 or self.gc_bias > 0.5:
            raise ValueError("The parameter \"gc_bias\" is wrong, it is in the range of [0, 0.5]!")

    def encode(self, bit_segments):
        for segment_index, bit_segment in enumerate(bit_segments):
            if len(bit_segment) % 2 != 0:
                bit_segments[segment_index] = [0] + bit_segment

        self.decode_packets = len(bit_segments)

        dna_sequences = []
        final_count = math.ceil(len(bit_segments) * (1 + self.redundancy))

        # things related to random number generator, starting an lfsr with a certain state and a polynomial for 32bits.
        lfsr = DNAFountain.LFSR().lfsr_s_p()
        # create the solition distribution object
        self.prng = DNAFountain.PRNG(number=self.decode_packets, delta=self.delta, c=self.c_dist)

        used_seeds = dict()
        chuck_recorder = []
        while len(dna_sequences) < final_count:
            seed = next(lfsr)
            if seed in used_seeds:
                continue

            # initialize droplet and trans-code to DNA.
            droplet = DNAFountain.Droplet()
            dna_sequence = droplet.get_dna(seed, self.prng, bit_segments, self.header_size)

            # check validity.
            if screen.check("".join(dna_sequence),
                            max_homopolymer=self.homopolymer, max_content=0.5 + self.gc_bias):
                dna_sequences.append(dna_sequence)
                chuck_recorder.append(droplet.chuck_indices)

            if self.need_logs:
                self.monitor.output(len(dna_sequences), final_count)

        # pre-check the decoding process in the encoding process
        if self.need_pre_check:
            try:
                visited_indices = [0] * self.decode_packets
                for chuck_indices in chuck_recorder:
                    for chuck_index in chuck_indices:
                        visited_indices[chuck_index] += 1
                if 0 in visited_indices:
                    no_visit_indices = []
                    for index, visited in enumerate(visited_indices):
                        if visited == 0:
                            no_visit_indices.append(index)
                    raise ValueError("bit segment " + str(no_visit_indices) + " are not been encoded!")
                if self.need_logs:
                    print("Pre-check the decoding process.")
                self.decode(dna_sequences)
            except ValueError:
                raise ValueError("Based on the pre decoding operation, "
                                 "it is found that the encoded data does not meet the full rank condition."
                                 "Please increase \"redundancy\" or use compression to "
                                 "change the original digital data.")
        else:
            if self.need_logs:
                print("We recommend that you test whether it can be decoded before starting the wet experiment.")

        return dna_sequences

    def decode(self, dna_sequences):
        if self.decode_packets is None:
            raise ValueError("We miss the parameter \"decode_packets\", "
                             + "please try again after inputting this parameter.")

        # creating the solition distribution object
        self.prng = DNAFountain.PRNG(number=self.decode_packets, delta=self.delta, c=self.c_dist)

        bit_segments = [None] * self.decode_packets
        done_segments = set()
        chunk_to_droplets = defaultdict(set)

        for dna_sequence in dna_sequences:
            droplet = DNAFountain.Droplet()
            droplet.init_binaries(self.prng, dna_sequence, self.header_size)

            for chunk_num in droplet.chuck_indices:
                chunk_to_droplets[chunk_num].add(droplet)

            self.update_droplets(droplet, bit_segments, done_segments, chunk_to_droplets)

            if self.need_logs:
                self.monitor.output(len(done_segments), self.decode_packets)

            if len(done_segments) == self.decode_packets:
                break

        if None in bit_segments or self.decode_packets - len(done_segments) > 0:
            raise ValueError("Couldn't decode the whole file, because some bit segments are not recovered!")

        return bit_segments

    def update_droplets(self, droplet, bit_segments, done_segments, chunk_to_droplets):
        for chunk_index in (set(droplet.chuck_indices) & done_segments):
            droplet.update_binaries(chunk_index, bit_segments)
            # cut the edge between droplet and input segment.
            chunk_to_droplets[chunk_index].discard(droplet)

        if len(droplet.chuck_indices) == 1:
            # the droplet has only one input segment
            lone_chunk = droplet.chuck_indices.pop()
            # assign the droplet value to the input segment (=entry[0][0])
            bit_segments[lone_chunk] = droplet.payload
            # add the lone_chunk to a data structure of done segments.
            done_segments.add(lone_chunk)
            # cut the edge between the input segment and the droplet
            chunk_to_droplets[lone_chunk].discard(droplet)
            # update other droplets
            for other_droplet in chunk_to_droplets[lone_chunk].copy():
                self.update_droplets(other_droplet, bit_segments, done_segments, chunk_to_droplets)

    class Droplet(object):

        def __init__(self):
            self.seed = None
            self.payload = None
            self.chuck_indices = None

        def get_dna(self, seed, prng, bit_segments, header_size):
            self.seed = seed
            self.payload = None
            self.chuck_indices = prng.get_src_blocks_wrap(seed)

            for chuck_index in self.chuck_indices:
                if self.payload is None:
                    self.payload = bit_segments[chuck_index]
                else:
                    self.payload = list(map(self.xor, self.payload, bit_segments[chuck_index]))

            bit_list = self._get_seed_list(header_size) + self.payload

            dna_sequence = []
            for index in range(0, len(bit_list), 2):
                dna_sequence.append(index_base.get(bit_list[index] * 2 + bit_list[index + 1]))

            return dna_sequence

        def init_binaries(self, prng, dna_sequence, header_size):
            # recover the bit segment
            bit_segment = []
            for base in dna_sequence:
                index = base_index.get(base)
                bit_segment.append(int(index / 2))
                bit_segment.append(index % 2)

            self.seed = self.get_seed(bit_segment[:header_size * 8])
            self.payload = bit_segment[header_size * 8:]
            self.chuck_indices = prng.get_src_blocks_wrap(self.seed)

        def update_binaries(self, chunk_index, bit_segments):
            self.payload = list(map(self.xor, self.payload, bit_segments[chunk_index]))
            # subtract (ie. xor) the value of the solved segment from the droplet.
            self.chuck_indices.remove(chunk_index)

        def _get_seed_list(self, header_size):
            seed_list = [0 for _ in range(header_size * 8)]
            temp_seed = self.seed
            for index in range(len(seed_list)):
                seed_list[index] = temp_seed % 2
                temp_seed = int((temp_seed - seed_list[index]) / 2)
            return seed_list

        @staticmethod
        def get_seed(seed_list):
            seed = 0
            for value in seed_list[::-1]:
                seed = seed * 2 + value

            return seed

        @staticmethod
        def xor(value_1, value_2):
            return value_1 ^ value_2

    class PRNG(object):

        def __init__(self, number, delta, c):
            self.number = number
            self.delta = delta
            self.c = c
            self.value = self.c * math.log(self.number / self.delta) * math.sqrt(self.number)
            self.cdf, self.degree = self.gen_rsd_cdf(number, self.value, self.delta)

        def get_src_blocks_wrap(self, seed):
            random.seed(seed)
            p = random.random()
            d = self._sample_degree(p)
            return random.sample(range(int(self.number)), d)

        @staticmethod
        def gen_rsd_cdf(number, value, delta):
            pivot = int(math.floor(number / value))
            value_1 = [value / number * 1 / d for d in range(1, pivot)]
            value_2 = [value / number * math.log(value / delta)]
            value_3 = [0 for _ in range(pivot, number)]
            tau = value_1 + value_2 + value_3
            rho = [1.0 / number] + [1.0 / (d * (d - 1)) for d in range(2, number + 1)]
            degree = sum(rho) + sum(tau)
            mu = [(rho[d] + tau[d]) / degree for d in range(number)]
            cdf = numpy.cumsum(mu)
            return cdf, degree

        def _sample_degree(self, p):
            index = None
            for index, value in enumerate(self.cdf):
                if value > p:
                    return index + 1
            return index + 1

    class LFSR(object):

        def __init__(self):
            pass

        @staticmethod
        def lfsr(state, mask):
            result = state
            nbits = mask.bit_length() - 1
            while True:
                result = result << 1
                xor = result >> nbits
                if xor != 0:
                    result ^= mask
                yield result

        @staticmethod
        def lfsr32p():
            return 0b100000000000000000000000011000101

        @staticmethod
        def lfsr32s():
            return 0b001010101

        def lfsr_s_p(self):
            return self.lfsr(self.lfsr32s(), self.lfsr32p())


class YinYangCode(AbstractCodingAlgorithm):

    def __init__(self, yang_rule=None, yin_rule=None, virtual_nucleotide="A", max_iterations=100,
                 max_ratio=0.8, faster=False, max_homopolymer=4, max_content=0.6, need_logs=False):
        super().__init__(need_logs)

        if not yang_rule:
            yang_rule = [0, 1, 0, 1]
        if not yin_rule:
            yin_rule = [[1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 0], [1, 1, 0, 0]]

        self.yang_rule = yang_rule
        self.yin_rule = yin_rule
        self.virtual_nucleotide = virtual_nucleotide
        self.max_iterations = max_iterations
        self.max_homopolymer = max_homopolymer
        self.max_content = max_content
        self.max_ratio = max_ratio
        self.faster = faster
        self.index_length = 0
        self.total_count = 0

        self.__init_check__()

        if self.need_logs:
            print("Create Yin-Yang Code successfully")

    def __init_check__(self):
        if self.virtual_nucleotide not in ["A", "C", "G", "T"]:
            raise ValueError("Virtual nucleotide needs to be one of \"A\", \"C\", \"G\", or \"T\"!")

        # Check Yang rule (rule 1)
        if sum(self.yang_rule) != 2:
            raise ValueError("Wrong correspondence between base and binary data!")
        for index, value in enumerate(self.yang_rule):
            if type(value) != int and (value != 0 and value != 1):
                raise ValueError("Only 0 and 1 can be included for base reference, and yang rule[" + str(index)
                                 + "] has been detected as " + str(value) + "!")

        # Check Yin rule (rule 2)
        if self.yang_rule[0] == self.yang_rule[1]:
            same = [0, 1, 2, 3]
        elif self.yang_rule[0] == self.yang_rule[2]:
            same = [0, 2, 1, 3]
        else:
            same = [0, 3, 1, 2]

        for index in range(len(self.yin_rule)):
            if self.yin_rule[index][same[0]] + self.yin_rule[index][same[1]] != 1 \
                    or self.yin_rule[index][same[0]] * self.yin_rule[index][same[1]] != 0:
                raise ValueError("Wrong yin rule, the error locations are ["
                                 + str(index) + ", " + str(same[0]) + "] and ["
                                 + str(index) + ", " + str(same[1]) + "]! "
                                 + "It is required by rule that these two values will have sum of 1 and product of 0.")
            if self.yin_rule[index][same[2]] + self.yin_rule[index][same[3]] != 1 \
                    or self.yin_rule[index][same[2]] * self.yin_rule[index][same[3]] != 0:
                raise ValueError("Wrong yin rule, the error locations are ["
                                 + str(index) + ", " + str(same[2]) + "] and ["
                                 + str(index) + ", " + str(same[3]) + "]! "
                                 + "It is required by rule that these two values will have sum of 1 and product of 0.")

    def encode(self, bit_segments):
        self.index_length = int(len(str(bin(len(bit_segments)))) - 2)
        self.total_count = len(bit_segments)

        if self.faster:
            dna_sequences = self.faster_encode(bit_segments)
        else:
            dna_sequences = self.normal_encode(bit_segments)

        if self.need_logs:
            print("There are " + str(len(dna_sequences) * 2 - self.total_count)
                  + " random bit segment(s) adding for logical reliability.")

        return dna_sequences

    def normal_encode(self, bit_segments):
        dna_sequences = []
        if self.need_logs:
            print("Separate \'good\' binary segments from \'bad\' binary segments.")

        bad_data = []
        for row in range(len(bit_segments)):
            if numpy.sum(bit_segments[row]) > len(bit_segments[row]) * self.max_ratio \
                    or numpy.sum(bit_segments[row]) < len(bit_segments[row]) * (1 - self.max_ratio):
                bad_data.append(row)

        if len(bit_segments) < len(bad_data) * 5:
            if self.need_logs:
                print("There may be a large number of sequences that are difficult for synthesis or sequencing. "
                      + "We recommend you to re-select the rule or take a new run.")

        if len(bad_data) == 0 and len(bit_segments) == 0:
            return [], []
        elif len(bad_data) == 0:
            good_data = []
            for row in range(len(bit_segments)):
                if self.need_logs:
                    self.monitor.output(row + 1, len(bit_segments))
                good_data.append(bit_segments[row])
            return good_data, []
        elif len(bad_data) == len(bit_segments):
            bad_data = []
            for row in range(len(bit_segments)):
                if self.need_logs:
                    self.monitor.output(row + 1, len(bit_segments))
                bad_data.append(bit_segments[row])
            return [], bad_data
        else:
            good_data = []
            bad_data = []
            for row in range(len(bit_segments)):
                if self.need_logs:
                    self.monitor.output(row + 1, len(bit_segments))
                if row in bad_data:
                    bad_data.append(bit_segments[row])
                else:
                    good_data.append(bit_segments[row])

        if self.need_logs:
            print("Encode based on random pair iteration.")

        while len(good_data) + len(bad_data) > 0:
            if len(good_data) > 0 and len(bad_data) > 0:
                fixed_bit_segment, is_finish, state = good_data.pop(), False, True
            elif len(good_data) > 0:
                fixed_bit_segment, is_finish, state = good_data.pop(), False, False
            elif len(bad_data) > 0:
                fixed_bit_segment, is_finish, state = bad_data.pop(), False, True
            else:
                raise ValueError("Wrong pairing for Yin-Yang Code!")

            for pair_time in range(self.max_iterations):
                if state:
                    if len(bad_data) > 0:
                        selected_index = random.randint(0, len(bad_data) - 1)
                        selected_bit_segment = bad_data[selected_index]
                    else:
                        break
                else:
                    if len(good_data) > 0:
                        selected_index = random.randint(0, len(good_data) - 1)
                        selected_bit_segment = good_data[selected_index]
                    else:
                        break

                dna_sequence = [[], []]
                support_nucleotide_1 = self.virtual_nucleotide
                support_nucleotide_2 = self.virtual_nucleotide
                for bit_1, bit_2 in zip(fixed_bit_segment, selected_bit_segment):
                    current_nucleotide_1 = self._bits_to_nucleotide(bit_1, bit_2, support_nucleotide_1)
                    current_nucleotide_2 = self._bits_to_nucleotide(bit_2, bit_1, support_nucleotide_2)
                    dna_sequence[0].append(current_nucleotide_1)
                    dna_sequence[1].append(current_nucleotide_2)
                    support_nucleotide_1 = current_nucleotide_1
                    support_nucleotide_2 = current_nucleotide_2

                if screen.check("".join(dna_sequence[0]),
                                max_homopolymer=self.max_homopolymer, max_content=self.max_content):
                    is_finish = True
                    dna_sequences.append(dna_sequence[0])
                    if state:
                        del bad_data[selected_index]
                    else:
                        del good_data[selected_index]
                    break
                elif screen.check("".join(dna_sequence[1]),
                                  max_homopolymer=self.max_homopolymer, max_content=self.max_content):
                    is_finish = True
                    dna_sequences.append(dna_sequence[1])
                    if state:
                        del bad_data[selected_index]
                    else:
                        del good_data[selected_index]
                    break

            # additional information
            if not is_finish:
                dna_sequences.append(self.addition(fixed_bit_segment, self.total_count))

            if self.need_logs:
                self.monitor.output(self.total_count - (len(good_data) + len(bad_data)), self.total_count)

        return dna_sequences

    def faster_encode(self, bit_segments):
        if self.need_logs:
            print("Faster setting may increases the number of additional binary segments "
                  + "(3 ~ 4 times than that of normal setting).")

        dna_sequences = []

        while len(bit_segments) > 0:
            fixed_bit_segment, is_finish = bit_segments.pop(), False
            for pair_time in range(self.max_iterations):
                if len(bit_segments) > 0:
                    selected_index = random.randint(0, len(bit_segments) - 1)
                    selected_bit_segment = bit_segments[selected_index]

                    dna_sequence = [[], []]
                    support_nucleotide_1 = self.virtual_nucleotide
                    support_nucleotide_2 = self.virtual_nucleotide
                    for bit_1, bit_2 in zip(fixed_bit_segment, selected_bit_segment):
                        current_nucleotide_1 = self._bits_to_nucleotide(bit_1, bit_2, support_nucleotide_1)
                        current_nucleotide_2 = self._bits_to_nucleotide(bit_2, bit_1, support_nucleotide_2)
                        dna_sequence[0].append(current_nucleotide_1)
                        dna_sequence[1].append(current_nucleotide_2)
                        support_nucleotide_1 = current_nucleotide_1
                        support_nucleotide_2 = current_nucleotide_2

                    if screen.check("".join(dna_sequence[0]),
                                    max_homopolymer=self.max_homopolymer, max_content=self.max_content):
                        is_finish = True
                        dna_sequences.append(dna_sequence[0])
                        del bit_segments[selected_index]
                        break
                    elif screen.check("".join(dna_sequence[1]),
                                      max_homopolymer=self.max_homopolymer, max_content=self.max_content):
                        is_finish = True
                        dna_sequences.append(dna_sequence[1])
                        del bit_segments[selected_index]
                        break

            # additional information
            if not is_finish:
                dna_sequences.append(self.addition(fixed_bit_segment, self.total_count))

            if self.need_logs:
                self.monitor.output(self.total_count - len(bit_segments), self.total_count)

        return dna_sequences

    def decode(self, dna_sequences):
        if self.index_length is None:
            raise ValueError("The parameter \"index_length\" is needed, "
                             + "which is used to eliminate additional random binary segments.")
        if self.total_count is None:
            raise ValueError("The parameter \"total_count\" is needed, "
                             + "which is used to eliminate additional random binary segments.")

        bit_segments = []

        for sequence_index, dna_sequence in enumerate(dna_sequences):
            upper_bit_segment, lower_bit_segment = [], []

            support_nucleotide = self.virtual_nucleotide
            for current_nucleotide in dna_sequence:
                upper_bit = self.yang_rule[base_index[current_nucleotide]]
                lower_bit = self.yin_rule[base_index[support_nucleotide]][base_index[current_nucleotide]]
                upper_bit_segment.append(upper_bit)
                lower_bit_segment.append(lower_bit)
                support_nucleotide = current_nucleotide

            bit_segments.append(upper_bit_segment)
            bit_segments.append(lower_bit_segment)

            if self.need_logs:
                self.monitor.output(sequence_index + 1, len(dna_sequences))

        remain_bit_segments = []
        for bit_segment in bit_segments:
            segment_index = int("".join(list(map(str, bit_segment[:self.index_length]))), 2)
            if segment_index < self.total_count:
                remain_bit_segments.append(bit_segment)

        return remain_bit_segments

    def addition(self, fixed_bit_segment, total_count):
        while True:
            # insert at least 2 interval.
            random_index = random.randint(total_count + 3, math.pow(2, self.index_length) - 1)
            random_segment = list(map(int, list(str(bin(random_index))[2:].zfill(self.index_length))))

            dna_sequence = [[], []]
            support_nucleotide_1 = self.virtual_nucleotide
            support_nucleotide_2 = self.virtual_nucleotide

            for bit_1, bit_2 in zip(fixed_bit_segment[: self.index_length], random_segment):
                current_nucleotide_1 = self._bits_to_nucleotide(bit_1, bit_2, support_nucleotide_1)
                current_nucleotide_2 = self._bits_to_nucleotide(bit_2, bit_1, support_nucleotide_2)
                dna_sequence[0].append(current_nucleotide_1)
                dna_sequence[1].append(current_nucleotide_2)
                support_nucleotide_1 = current_nucleotide_1
                support_nucleotide_2 = current_nucleotide_2

            work_flags = [True, True]
            for fixed_bit in fixed_bit_segment[self.index_length:]:
                current_nucleotide_1, current_nucleotide_2 = None, None
                for bit in [0, 1]:
                    if work_flags[0] and current_nucleotide_1 is None:
                        current_nucleotide_1 = self._bits_to_nucleotide(fixed_bit, bit, support_nucleotide_1)
                        if not screen.check("".join(dna_sequence[0]) + current_nucleotide_1,
                                            max_homopolymer=self.max_homopolymer,
                                            max_content=self.max_content):
                            current_nucleotide_1 = None
                    if work_flags[1] and current_nucleotide_2 is None:
                        current_nucleotide_2 = self._bits_to_nucleotide(bit, fixed_bit, support_nucleotide_2)
                        if not screen.check("".join(dna_sequence[1]) + current_nucleotide_2,
                                            max_homopolymer=self.max_homopolymer,
                                            max_content=self.max_content):
                            current_nucleotide_2 = None

                if current_nucleotide_1 is None:
                    work_flags[0] = False
                    dna_sequence[0] = None
                else:
                    dna_sequence[0].append(current_nucleotide_1)
                    support_nucleotide_1 = current_nucleotide_1

                if current_nucleotide_2 is None:
                    work_flags[1] = False
                    dna_sequence[1] = None
                else:
                    dna_sequence[1].append(current_nucleotide_2)
                    support_nucleotide_2 = current_nucleotide_2

            for potential_dna_sequence in dna_sequence:
                if potential_dna_sequence is not None and screen.check("".join(potential_dna_sequence),
                                                                       max_homopolymer=self.max_homopolymer,
                                                                       max_content=self.max_content):
                    return potential_dna_sequence

    def _bits_to_nucleotide(self, upper_bit, lower_bit, support_nucleotide):
        current_options = []
        for index in range(len(self.yang_rule)):
            if self.yang_rule[index] == upper_bit:
                current_options.append(index)

        if self.yin_rule[base_index.get(support_nucleotide)][current_options[0]] == lower_bit:
            return index_base[current_options[0]]
        else:
            return index_base[current_options[1]]

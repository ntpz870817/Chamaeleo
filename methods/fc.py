"""
Name: Fountain Codec (DNA Storage Code created by DNA Fountain)

Reference:
Erlich, Y., & Zielinski, D. (2017). DNA Fountain enables a robust and efficient storage architecture. Science, 355(6328), 950-954.

Coder: HaoLing ZHANG (BGI-Research)[V1], QianLong ZHUANG (BGI-Research)[V1]

Current Version: 1

Function(s):
(1) DNA encoding by Fountain Codec.
(2) DNA decoding by Fountain Codec.
"""

import random
import sys
import math
import numpy
from collections import defaultdict

from Chamaeleo.utils import monitor
from Chamaeleo.utils import log
from Chamaeleo.methods.components import inherent
from Chamaeleo.methods.components import validity


# noinspection PyMethodMayBeStatic, PyProtectedMember,PyBroadException
class FC:

    def __init__(
            self,
            homopolymer=4,
            gc_content=0.2,
            redundancy=0.5,
            c_dist=0.1,
            delta=0.5,
            header_size=4,
            recursion_depth=10000000,
            decode_packets=None):
        """
        introduction: The initialization method of FC.

        :param homopolymer: maximum length of homopolymer, type = int.
        :param gc_content: the fraction of gc content above/below 0.5 (0.1 means 0.4-0.6).
        :param redundancy: artificial redundancy for decode successfully (0.5 generate 50% more fragments),type = float.
        :param c_dist: Degree distribution tuning parameter,type = float.
        :param delta: Degree distribution tuning parameter,type = float.
        :param header_size: number of bytes for the header, type = int.
        :param decode_packets: bit segments in the encoding process, type = int.
        """
        self.homopolymer = homopolymer
        self.gc_content = gc_content
        self.redundancy = redundancy
        self.header_size = header_size
        self.recursion_depth = recursion_depth

        self.c_dist = c_dist
        self.delta = delta
        self.decode_packets = decode_packets

        self._init_check()

        self.prng = None
        self.file_size = 0
        self.monitor = monitor.Monitor()

    def _init_check(self):
        """
        introduction: The verification of initialization parameters.

        """
        if self.redundancy < 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The parameter \"redundancy\" is wrong, it is greater than or equal to 0!")

        if self.header_size < 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The parameter \"header_size\" is wrong, it is greater than or equal to 0!")

        if self.gc_content < 0 or self.gc_content > 0.5:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The parameter \"gc_content\" is wrong, it is in the [0, 0.5]!")

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

        :param need_log: Show the log.

        :return dna_sequences: The DNA sequence of len(matrix) rows.
                             Type: list(string).
        """
        self.file_size = size
        self.monitor.restore()

        if len(matrix[0]) % 2 == 1:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "Binary sequence length should be even.")

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Encode the matrix by Fountain Codec.")

        # calculate decode packets
        self.decode_packets = len(matrix)

        dna_sequences = []
        final_count = math.ceil(len(matrix) * (1 + self.redundancy))

        # things related to random number generator, starting an lfsr with a certain state and a polynomial for 32bits.
        lfsr = LFSR().lfsr_s_p()
        # creating the solition distribution object
        self.prng = PRNG(K=len(matrix), delta=self.delta, c=self.c_dist)

        used_bc = dict()
        while len(dna_sequences) < final_count:
            seed = next(lfsr)
            if seed in used_bc:
                continue

            # initialize droplet and trans-code to DNA.
            droplet = Droplet()
            dna_sequence = droplet.get_dna(seed, self.prng, matrix, self.header_size)

            # check validity.
            if validity.homopolymer("".join(dna_sequence), self.homopolymer) \
                    and validity.cg_content("".join(dna_sequence), 0.5 + self.gc_content):
                dna_sequences.append(dna_sequence)

            if need_log:
                self.monitor.output(len(dna_sequences), final_count)

        if need_log:
            log.output(log.WARN, str(__name__), str(sys._getframe().f_code.co_name),
                       "Fountain codes for which the inputted matrix is of full rank in the decoding process are "
                       "decodable, the full rank depends on the hyper-parameter \"redundancy\" in the Fountain Codec.\n"
                       "Therefore, we strongly recommend that we decode it directly to verify the decodable "
                       "of the DNA file before conducting DNA synthesis experiments.")

        self.monitor.restore()

        return dna_sequences

    # ================================================= decode part ====================================================

    def decode(self, dna_sequences, need_log=False):
        """
        introduction: Decode DNA sequences to the data of binary file.

        :param dna_sequences: The DNA sequence of len(matrix) rows.
                            The length of each DNA sequences should be a multiple of 9.
                            Type: One-dimensional list(string).

        :param need_log: Show the log.

        :return matrix: The binary matrix corresponding to the dna sequences.
                         Type: Two-dimensional list(int).

        :return file_size: This refers to file size, to reduce redundant bits when transferring DNA to binary files.
                            Type: int
        """
        self.monitor.restore()

        # adjust the maximum recursion depth to "self.recursion_depth" in Python.
        sys.setrecursionlimit(self.recursion_depth)

        if self.decode_packets is None:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "We miss the parameter \"decode_packets\", please try again after inputting this parameter.")

        if need_log:
            log.output(log.WARN, str(__name__), str(sys._getframe().f_code.co_name),
                       "If we get the system crash named -1073741571(0xC00000FD), "
                       "it is caused by the excessive function (_update_droplets) recursive calls.\n"
                       "Please reduce the hyper-parameter \"redundancy\" or split the original digital file"
                       " in the encoding process.")

        if need_log:
            log.output(log.NORMAL, str(__name__), str(sys._getframe().f_code.co_name),
                       "Decode the matrix by Fountain Codec.")

        # creating the solition distribution object
        self.prng = PRNG(K=self.decode_packets, delta=self.delta, c=self.c_dist)

        matrix = [None] * self.decode_packets
        done_segments = set()
        chunk_to_droplets = defaultdict(set)

        for dna_sequence in dna_sequences:
            droplet = Droplet()
            droplet.init_binaries(self.prng, dna_sequence, self.header_size)

            for chunk_num in droplet.chuck_indices:
                chunk_to_droplets[chunk_num].add(droplet)

            self._update_droplets(droplet, matrix, done_segments, chunk_to_droplets)

            if need_log:
                self.monitor.output(len(done_segments), self.decode_packets)

        if None in matrix or self.decode_packets - len(done_segments) > 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "Couldn't decode the whole file.")

        self.monitor.restore()

        return matrix, self.file_size

    def _update_droplets(self, droplet, matrix, done_segments, chunk_to_droplets):
        """
        introduction: Update droplets by removing solved segments from droplets.

        :param droplet: Current droplet.

        :param matrix: Current decoded matrix.

        :param done_segments: The done bit segments.

        :param chunk_to_droplets: Current chucked droplets.
        """
        for chunk_index in (set(droplet.chuck_indices) & done_segments):
            droplet.update_binaries(chunk_index, matrix)
            # cut the edge between droplet and input segment.
            chunk_to_droplets[chunk_index].discard(droplet)

        if len(droplet.chuck_indices) == 1:
            # the droplet has only one input segment
            lone_chunk = droplet.chuck_indices.pop()
            # assign the droplet value to the input segment (=entry[0][0])
            matrix[lone_chunk] = droplet.payload
            # add the lone_chunk to a data structure of done segments.
            done_segments.add(lone_chunk)
            # cut the edge between the input segment and the droplet
            chunk_to_droplets[lone_chunk].discard(droplet)
            # update other droplets
            for other_droplet in chunk_to_droplets[lone_chunk].copy():
                self._update_droplets(other_droplet, matrix, done_segments, chunk_to_droplets)

    # ================================================= other part =====================================================


# noinspection PyMethodMayBeStatic
class Droplet(object):

    def __init__(self):
        """
        introduction: The initialization method of FC.
        """
        self.seed = None
        self.payload = None
        self.chuck_indices = None

    def get_dna(self, seed, prng, matrix, header_size):
        """
        introduction: Obtain DNA sequence from the seed and matrix.

        :param seed: The random seed.

        :param prng: The pseudo-random number generator created in the Fountain Codec.

        :param matrix: Original bit matrix.

        :param header_size: Header size mentioned in the Fountain Codec.

        :return: The generated DNA sequence.
        """
        self.seed = seed
        self.payload = None
        self.chuck_indices = prng.get_src_blocks_wrap(seed)

        for chuck_index in self.chuck_indices:
            if self.payload is None:
                self.payload = matrix[chuck_index]
            else:
                self.payload = list(map(self._xor, self.payload, matrix[chuck_index]))

        bit_list = self._get_seed_list(header_size) + self.payload

        dna_sequence = []
        for index in range(0, len(bit_list), 2):
            dna_sequence.append(inherent.index_base.get(bit_list[index] * 2 + bit_list[index + 1]))

        return dna_sequence

    def init_binaries(self, prng, dna_sequence, header_size):
        """
        introduction: Initialize the bit segment by initial information.

        :param prng: The pseudo-random number generator created in the Fountain Codec.

        :param dna_sequence: The current obtained DNA sequence.

        :param header_size: Header size mentioned in the Fountain Codec.
        """
        # recover the bit segment
        bit_segment = []
        for base in dna_sequence:
            index = inherent.base_index.get(base)
            bit_segment.append(int(index / 2))
            bit_segment.append(index % 2)

        self.seed = self._get_seed(bit_segment[:header_size * 8])
        self.payload = bit_segment[header_size * 8:]
        self.chuck_indices = prng.get_src_blocks_wrap(self.seed)

    def update_binaries(self, chunk_index, matrix):
        """
        introduction: Remove solved segments from droplets

        :param chunk_index: The chuck index in the droplet.

        :param matrix: The current decoded matrix.
        """
        self.payload = list(map(self._xor, self.payload, matrix[chunk_index]))
        # subtract (ie. xor) the value of the solved segment from the droplet.
        self.chuck_indices.remove(chunk_index)

    def _get_seed_list(self, header_size):
        """
        introduction: Obtain seed bit list with the length "header_size"

        :param header_size: The header size mentioned in the Fountain Codec.

        :return: The generated seed list.
        """
        seed_list = [0 for _ in range(header_size * 8)]
        temp_seed = self.seed
        for index in range(len(seed_list)):
            seed_list[index] = temp_seed % 2
            temp_seed = int((temp_seed - seed_list[index]) / 2)
        return seed_list

    def _get_seed(self, seed_list):
        """
        introduction: Obtain the integer seed from the corresponding seed list.

        :param seed_list: The inputted seed list.

        :return: The integer seed.
        """
        seed = 0
        for value in seed_list[::-1]:
            seed = seed * 2 + value

        return seed

    def _xor(self, value_1, value_2):
        """
        introduction: The xor operation in Fountain Codec

        :param value_1: value 1.
        :param value_2: value 2.

        :return: value 1 xor value 2.
        """
        return value_1 ^ value_2


# noinspection PyMethodMayBeStatic,PyPep8Naming
class PRNG(object):

    def __init__(self, K, delta, c):
        """
        introduction: The initialization method of Pseudo-Random Number Generator.

        :param K: The number of segments.

        :param delta: The parameter that determine the distribution.

        :param c: The parameter that determine the distribution.
        """
        self.K = K
        self.delta = delta
        self.c = c
        self.S = self.c * math.log(self.K / self.delta) * math.sqrt(self.K)
        self.cdf, self.Z = self._gen_rsd_cdf(K, self.S, self.delta)

    def get_src_blocks_wrap(self, seed):
        """
        introduction: A wrapper function to get source blocks.

        :param seed: The current random seed.

        :return: the random number group from the random seed.
        """
        random.seed(seed)
        p = random.random()
        d = self._sample_degree(p)
        return random.sample(range(int(self.K)), d)

    def _gen_rsd_cdf(self, K, S, delta):
        """
        introduction: The CDF of the RSD on block degree, precomputed for sampling speed.

        :param K: The number of segments.

        :param S: A helper function to calculate S, the expected number of degree=1 nodes.

        :param delta: The parameter that determine the distribution.

        :return: The Robust part of the Robust Soliton Distribution on the degree of transmitted blocks and the Ideal Soliton Distribution.
        """
        pivot = int(math.floor(K / S))
        val1 = [S / K * 1 / d for d in range(1, pivot)]
        val2 = [S / K * math.log(S / delta)]
        val3 = [0 for _ in range(pivot, K)]
        tau = val1 + val2 + val3
        rho = [1.0 / K] + [1.0 / (d * (d - 1)) for d in range(2, K + 1)]
        Z = sum(rho) + sum(tau)
        mu = [(rho[d] + tau[d]) / Z for d in range(K)]
        cdf = numpy.cumsum(mu)
        return cdf, Z

    def _sample_degree(self, p):
        """
        introduction: Samples degree given the precomputed distributions.

        :param p: The precomputed distribution.

        :return: The sample degree.
        """
        index = None
        for index, value in enumerate(self.cdf):
            if value > p:
                return index + 1
        return index + 1


# noinspection PyMethodMayBeStatic
class LFSR(object):

    def __init__(self):
        pass

    def lfsr(self, state, mask):
        """
        introduction: Obtain the iterator of Galois lfsr.

        :param state: Current state.

        :param mask: Current mask.

        :return: the random seed.
        """
        result = state
        nbits = mask.bit_length() - 1
        while True:
            result = result << 1
            xor = result >> nbits
            if xor != 0:
                result ^= mask
            yield result

    def lfsr32p(self):
        """
        introduction: A hard coded polynomial (0b100000000000000000000000011000101).
                      The polynomial corresponds to 1 + x^25 + x^26 + x^30 + x^32, which is known
                      to repeat only after 32^2-1 tries. Don't change unless you know what you are doing.

        :return: 0b100000000000000000000000011000101.
        """
        return 0b100000000000000000000000011000101

    def lfsr32s(self):
        """
        introduction: A hard coded state for the lfsr (0b001010101).
                      This state is the initial position in the register. You can change it without a major implication.

        :return: 0b001010101.
        """
        return 0b001010101

    def lfsr_s_p(self):
        """
        introduction: Create the lfsr iterator based on 0b100000000000000000000000011000101 and 0b001010101.

        :return: The lfsr iterator.
        """
        return self.lfsr(self.lfsr32s(), self.lfsr32p())

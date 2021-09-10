from datetime import datetime
from Chamaeleo.methods.inherent import index_base, base_index
from Chamaeleo.utils.monitor import Monitor


class AbstractCodingAlgorithm(object):

    def __init__(self, need_logs):
        self.bit_size = None
        self.need_logs = need_logs
        self.monitor = Monitor()
        self.segment_length = None

    def __init_check__(self):
        raise NotImplementedError("\"init_check\" interface needs to be implemented!")

    def silicon_to_carbon(self, bit_segments, bit_size):
        for bit_segment in bit_segments:
            if type(bit_segment) != list or type(bit_segment[0]) != int:
                raise ValueError("The dimension of bit matrix can only be 2!")

        self.bit_size = bit_size
        self.segment_length = len(bit_segments[0])
        start_time = datetime.now()

        if self.need_logs:
            print("Encode bit segments to DNA sequences by coding scheme.")

        dna_sequences = self.encode(bit_segments)

        encoding_runtime = (datetime.now() - start_time).total_seconds()

        nucleotide_count = 0
        for dna_sequence in dna_sequences:
            nucleotide_count += len(dna_sequence)

        information_density = bit_size / nucleotide_count

        return {"dna": dna_sequences, "i": information_density, "t": encoding_runtime}

    def carbon_to_silicon(self, dna_sequences):
        for dna_sequence in dna_sequences:
            if type(dna_sequence) != list or type(dna_sequence[0]) != str:
                raise ValueError("The dimension of nucleotide matrix can only be 2!")

        start_time = datetime.now()

        if self.need_logs:
            print("Decode DNA sequences to bit segments by coding scheme.")
        bit_segments = self.decode(dna_sequences)

        for segment_index, bit_segment in enumerate(bit_segments):
            if len(bit_segment) != self.segment_length:
                bit_segments[segment_index] = bit_segment[: self.segment_length]

        decoding_runtime = (datetime.now() - start_time).total_seconds()

        return {"bit": bit_segments, "s": self.bit_size, "t": decoding_runtime}

    def encode(self, bit_segments):
        raise NotImplementedError("\"decode\" interface needs to be implemented!")

    def decode(self, dna_sequences):
        raise NotImplementedError("\"decode\" interface needs to be implemented!")


class BaseCodingAlgorithm(AbstractCodingAlgorithm):

    def __init__(self, need_logs=False):
        super().__init__(need_logs)
        self.mapping_rules = [[0, 0], [0, 1], [1, 0], [1, 1]]

    def __init_check__(self):
        pass

    def encode(self, bit_segments):
        dna_sequences = []

        for segment_index, bit_segment in enumerate(bit_segments):
            dna_sequence = []

            if len(bit_segment) % 2 != 0:
                bit_segment = bit_segment + [0]

            for position in range(0, len(bit_segment), 2):
                dna_sequence.append(index_base.get(self.mapping_rules.index(bit_segment[position: position + 2])))

            dna_sequences.append(dna_sequence)

            if self.need_logs:
                self.monitor.output(segment_index + 1, len(bit_segments))

        return dna_sequences

    def decode(self, dna_sequences):
        bit_segments = []

        for sequence_index, dna_sequence in enumerate(dna_sequences):
            bit_segment = []
            for nucleotide in dna_sequence:
                bit_segment += self.mapping_rules[base_index.get(nucleotide)]

            bit_segments.append(bit_segment)

            if self.need_logs:
                self.monitor.output(sequence_index + 1, len(dna_sequences))

        return bit_segments


class AbstractErrorCorrectionCode(object):

    def __init__(self, need_logs):
        self.need_logs = need_logs
        self.segment_lengths = []
        self.monitor = Monitor()

    def insert(self, bit_segments):
        if self.need_logs:
            print("Insert the error-correction code to the bit segments.")
        self.segment_lengths = []
        verified_bit_segments = []
        if type(bit_segments) == list and type(bit_segments[0]) == list:
            for index, bit_segment in enumerate(bit_segments):
                self.segment_lengths.append(len(bit_segment))
                verified_bit_segments.append(self.insert_one(bit_segment))
                if self.need_logs:
                    self.monitor.output(index + 1, len(bit_segments))
        elif type(bit_segments) == list and type(bit_segments[0]) == int:
            self.segment_lengths = [len(bit_segments)]
            verified_bit_segments = self.insert_one(bit_segments)
        else:
            raise ValueError("The matrix must be 1-dimensional or 2-dimensional, and the value is of type \"int\".")

        return verified_bit_segments, len(verified_bit_segments[0]) - len(bit_segments[0])

    def remove(self, verified_bit_segments):
        if self.need_logs:
            print("Check and remove the error-correction code from the bit segments.")
        bit_segments = []

        error_bit_segments = []
        error_indices = []

        if type(verified_bit_segments) == list and type(verified_bit_segments[0]) == list:
            error_rate = 0
            for index, verified_bit_segment in enumerate(verified_bit_segments):
                if verified_bit_segment is not None:
                    output = self.remove_one(verified_bit_segment)
                    data, data_type = output.get("data"), output.get("type")
                    if data_type and len(data) >= self.segment_lengths[index]:
                        bit_segments.append(data[len(data) - self.segment_lengths[index]:])
                    else:
                        error_rate += 1
                        error_indices.append(index)
                        error_bit_segments.append(data)
                else:
                    error_rate += 1
                    error_indices.append(index)
                    error_bit_segments.append(None)

                if self.need_logs:
                    self.monitor.output(index + 1, len(verified_bit_segments))

            error_rate /= len(verified_bit_segments)

        elif type(verified_bit_segments) == list and type(verified_bit_segments[0]) == int:
            output = self.remove_one(verified_bit_segments[0])
            data, data_type = output.get("data"), output.get("type")
            if data_type:
                error_rate = 0
                bit_segments = [data[len(data) - self.segment_lengths[0]:]]
            else:
                error_rate = 1
                error_indices.append(0)
                error_bit_segments.append(data)
        else:
            raise ValueError("The matrix must be 1-dimensional or 2-dimensional, and the value is of type \"int\".")

        return {"bit": bit_segments, "e_r": error_rate, "e_i": error_indices, "e_bit": error_bit_segments}

    def insert_one(self, input_list):
        raise NotImplementedError("\"insert_one\" interface needs to be implemented!")

    def remove_one(self, input_list):
        raise NotImplementedError("\"remove_one\" interface needs to be implemented!")

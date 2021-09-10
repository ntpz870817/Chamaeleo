import copy
from reedsolo import RSCodec, ReedSolomonError
from Chamaeleo.methods.default import AbstractErrorCorrectionCode


class Hamming(AbstractErrorCorrectionCode):

    def __init__(self, need_logs=False):
        super().__init__(need_logs)

    def insert_one(self, input_list):
        # calculate the length needed for detection site.
        detect_site_length = 0
        while (len(input_list) + detect_site_length + 1) > (pow(2, detect_site_length)):
            detect_site_length += 1

        input_list.reverse()

        # Add detection site in the origin list.
        detect_site, list_site, output_list = 0, 0, []
        for index in range(detect_site_length + len(input_list)):
            if pow(2, detect_site) == index + 1:
                output_list.append(0)
                detect_site += 1
            else:
                output_list.append(input_list[list_site])
                list_site += 1

        # XOR operations on each detection site
        # From the 2^(k - 1) bit of the new code, the k-bit parity-check code calculates
        # the exclusive or of 2^(k - 1) bits, jumps 2^(k - 1) bits,
        # calculates the exclusive or of the next set of 2^(k - 1) bits, and fills in 2^(k - 1) bits.
        detect_site = 0
        for parity in range(len(output_list)):
            if pow(2, detect_site) == parity + 1:
                start_index = pow(2, detect_site) - 1
                index = start_index
                xor = []

                while index < len(output_list):
                    xor.extend(output_list[index: index + pow(2, detect_site)])
                    index += pow(2, detect_site + 1)

                for xor_index in range(1, len(xor)):
                    output_list[start_index] = output_list[start_index] ^ xor[xor_index]
                detect_site += 1

        output_list.reverse()

        return output_list

    def remove_one(self, input_list):
        original_input_list = copy.deepcopy(input_list)

        input_list.reverse()
        detect_site, output_list, output_list_copy = 0, [], []
        for index in range(0, len(input_list)):
            output_list.append(input_list[index])
            output_list_copy.append(input_list[index])
            if pow(2, detect_site) == index + 1:
                detect_site += 1

        detect_site, parity_list = 0, []
        for parity in range(0, (len(output_list))):
            if pow(2, detect_site) == parity + 1:
                start_index = pow(2, detect_site) - 1
                index = start_index
                xor = []

                while index < len(output_list):
                    block = output_list[index: index + pow(2, detect_site)]
                    xor.extend(block)
                    index += pow(2, detect_site + 1)

                for xor_index in range(1, len(xor)):
                    output_list[start_index] = output_list[start_index] ^ xor[xor_index]
                parity_list.append(output_list[parity])
                detect_site += 1
        parity_list.reverse()

        error = sum(int(parity_list) * pow(2, index) for index, parity_list in enumerate(parity_list[::-1]))

        if error >= len(output_list_copy):
            return {"data": original_input_list, "type": False}
        elif error > 0:
            if output_list_copy[error - 1] == 0:
                output_list_copy[error - 1] = 1
            else:
                output_list_copy[error - 1] = 0

        detect_site, output_list = 0, []
        # Remove the detection site.
        for index in range(len(output_list_copy)):
            if pow(2, detect_site) == index + 1:
                detect_site += 1
            else:
                output_list.append(output_list_copy[index])

        output_list.reverse()

        return {"data": output_list, "type": True}


class ReedSolomon(AbstractErrorCorrectionCode):

    def __init__(self, check_size=3, need_logs=False):
        self.check_size = check_size
        self.tool = RSCodec(check_size)
        super().__init__(need_logs)

    def insert_one(self, input_list):
        if len(input_list) % 8 != 0:
            raise ValueError("The length of inputted binary segment must be divided by 8!")

        byte_list = []
        for index in range(0, len(input_list), 8):
            byte_list.append(int(str("".join(list(map(str, input_list[index: index + 8])))), 2))

        output_list = []
        for one_byte in list(self.tool.encode(byte_list)):
            temp_bits = list(map(int, list(bin(one_byte))[2:]))
            temp_bits = [0 for _ in range(8 - len(temp_bits))] + temp_bits
            output_list += temp_bits

        return output_list

    def remove_one(self, input_list):
        original_input_list = copy.deepcopy(input_list)

        byte_list = []
        for index in range(0, len(input_list), 8):
            byte_list.append(int(str("".join(list(map(str, input_list[index: index + 8])))), 2))

        try:
            decode_byte_list = list(self.tool.decode(byte_list))
            # fix error in Linux or Mac OS, TypeError: 'bytearray' object cannot be interpreted as an integer
            if type(decode_byte_list[0]) is not int:
                decode_byte_list = list(decode_byte_list[0])

            output_list = []
            for one_byte in list(decode_byte_list):
                temp_bits = list(map(int, list(bin(one_byte))[2:]))
                temp_bits = [0 for _ in range(8 - len(temp_bits))] + temp_bits
                output_list += temp_bits
        except ReedSolomonError:
            # Irreparable
            return {"data": original_input_list, "type": False}
        except IndexError:
            # No data acquisition
            return {"data": original_input_list, "type": False}

        return {"data": output_list, "type": True}

import random
import unittest
from reedsolo import RSCodec


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.test_bit_list = [random.randint(0, 1) for _ in range(12)]
        self.test_verify_list = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1]

        self.tool = RSCodec(1)

    def test_add_rs(self):
        byte_list = [0, 0, 0, 0] + self.test_bit_list
        target_list = []
        for index in range(0, len(byte_list), 8):
            target_list.append(int(str("".join(list(map(str, byte_list[index: index + 8])))), 2))

        v_seq = self.tool.encode(bytearray(target_list))

        output_list = []
        for one_byte in v_seq:
            temp_bits = list(map(int, list(bin(int(str(one_byte), 10)))[2:]))
            temp_bits = [0 for _ in range(8 - len(temp_bits))] + temp_bits
            output_list += temp_bits

        self.assertEqual(output_list, self.test_verify_list)

    def test_remove_rs(self):
        byte_list = []
        for index in range(0, len(self.test_verify_list), 8):
            byte_list.append(int(str("".join(list(map(str, self.test_verify_list[index: index + 8])))), 2))

        output_list = []
        v_seq = self.tool.decode(bytearray(byte_list))

        for one_byte in v_seq:
            temp_bits = list(map(int, list(bin(int(str(one_byte), 10)))[2:]))
            temp_bits = [0 for _ in range(8 - len(temp_bits))] + temp_bits
            output_list += temp_bits

        self.assertEqual(output_list[4:], self.test_bit_list)

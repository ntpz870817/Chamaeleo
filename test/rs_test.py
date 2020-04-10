import random
import unittest
from reedsolo import RSCodec


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.test_bit_list = [random.randint(0, 1) for _ in range(12)]
        self.test_verify_list = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1]

        self.tool = RSCodec(1)

    def test_total(self):
        byte_list = [0, 0, 0, 0] + self.test_bit_list
        target_list = []
        for index in range(0, len(byte_list), 8):
            target_list.append(int(str("".join(list(map(str, byte_list[index: index + 8])))), 2))

        print("ord list before encode = " + str(target_list))

        v_seq = list(self.tool.encode(target_list))

        print("ord list after encode = " + str(v_seq))

        v_seq = list(self.tool.decode(v_seq))

        print("ord list after decode = " + str(v_seq))

        output_list = []
        for one_byte in v_seq:
            temp_bits = list(map(int, list(bin(int(str(one_byte), 10)))[2:]))
            temp_bits = [0 for _ in range(8 - len(temp_bits))] + temp_bits
            output_list += temp_bits

        self.assertEqual(output_list[4:], self.test_bit_list)

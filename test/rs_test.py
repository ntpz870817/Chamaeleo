import random
import unittest
from reedsolo import RSCodec
import platform


class TestEncodeDecode(unittest.TestCase):

    def setUp(self):
        random.seed(30)
        self.test_bit_list = [random.randint(0, 1) for _ in range(120)]
        self.tool = RSCodec(1)

    def test_total(self):
        target_list = []
        for index in range(0, len(self.test_bit_list), 8):
            target_list.append(int(str("".join(list(map(str, self.test_bit_list[index: index + 8])))), 2))

        print("ord list before encode = " + str(target_list))
        print("type v_seq[0] = " + str(type(target_list[0])))
        print(bytearray(target_list))

        v_seq = self.tool.encode(target_list)
        print("ord list after encode = " + str(v_seq))

        v_seq = self.tool.decode(list(v_seq))
        if platform.system() == "Linux":
            v_seq = v_seq[0]

        print("ord list after decode = " + str(v_seq))

        output_list = []
        for one_byte in list(v_seq):
            temp_bits = list(map(int, list(bin(one_byte))[2:]))
            temp_bits = [0 for _ in range(8 - len(temp_bits))] + temp_bits
            output_list += temp_bits

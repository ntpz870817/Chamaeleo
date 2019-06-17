"""
Name: Functional testing for HC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of Huffman code transformation
"""

import random

import methods.hc as hc

if __name__ == '__main__':
    tool = hc.HC()
    tool.__huffman_dict__()
    tool.segment_length = 120
    tool.index_binary_length = 0
    test_list = [random.randint(0, 1) for index in range(120)]
    print(test_list)
    dna_motif = tool.__list_to_motif__(tool.__huffman_compressed__(test_list))
    print(dna_motif)
    binary_list = tool.__huffman_decompressed__(tool.__motif_to_list__(dna_motif), 2)
    print(binary_list)

    # test_list1 = [[random.randint(0, 1) for col in range(160)] for row in range(3)]
    # print(test_list1)
    # tool = hc.HC()
    # dna_motifs = tool.encode(test_list1, 300, True, True)
    # output_list = tool.decode(dna_motifs, True)
    # print()
    # print(output_list)
    # print(test_list1 == output_list)

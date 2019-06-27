"""
Name: Functional testing for GC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of 256^2 and 47^3 transformation
"""

import random

import methods.gc as gc

if __name__ == '__main__':
    tool = gc.GC([index for index in range(0, 48)])
    tool.segment_length = 160
    tool.index_binary_length = 0
    test_list = [random.randint(0, 1) for index in range(160)]
    print(test_list)
    dna_motif = tool.__list_to_motif__(test_list)
    print(dna_motif)
    binary_list = tool.__motif_to_list__(dna_motif)
    print(binary_list)

    print(test_list == binary_list)

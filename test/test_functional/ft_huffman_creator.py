"""
Name: Functional testing for HC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The reliability of Huffman code creator
"""

import random

import methods.components.huffman_creator as creator

if __name__ == '__main__':
    matrix = [[random.randint(0, 1) for col in range(8000)] for row in range(30)]
    size = 30000
    print(creator.get_map(matrix, size, 3))

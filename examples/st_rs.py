"""
Name: Symmetrical testing for Reed-Solomon Coding

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The Feasibility of Testing the Whole Process of Reed-Solomon Coding.
"""

import copy
import random

from Chamaeleo.methods.verifies import rs


method = rs.RS()
segment_length = 16
origin = [random.randint(0, 1) for i in range(segment_length)]


# Add error correction code to the original list.
def add_error_correction(original_list):
    add_list = method.add_for_list(original_list)
    print(str(add_list) + ": list after adding error correction.")
    return add_list


# Remove error correction code in the original list.
def remove_error_correction(original_list):
    remove_list = method.remove_for_list(original_list)
    print(str(remove_list) + ": list after removing error correction.")
    return remove_list


# Verify error correction in the original list.
def verify_error_correction(original_list):
    verify_list = method.verify_for_list(original_list)
    print(str(verify_list) + ": list after verifying.")
    return verify_list


# Modify the original list in process.
def modify_list_in_process(original_list):
    modify_list = copy.deepcopy(original_list)
    error_position = random.randint(0, len(original_list) - 1)
    if modify_list[error_position] == 0:
        modify_list[error_position] = 1
    else:
        modify_list[error_position] = 0
    print(str(modify_list) + ": list after modifying error, and error position is " + str(error_position) + ".")
    return modify_list


if __name__ == "__main__":
    print("no error situation: ")
    print(str(origin) + ": original list.")
    in_process = add_error_correction(origin)
    verify = verify_error_correction(in_process)
    remove_error_correction(verify)


    print("error situation: ")
    print(str(origin) + ": original list.")
    in_process = add_error_correction(origin)
    error = modify_list_in_process(in_process)
    verify = verify_error_correction(error)
    remove_error_correction(verify)

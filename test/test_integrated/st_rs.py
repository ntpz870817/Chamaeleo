import random

from Chamaeleo.methods.verifies import rs

length = 16

origin = [random.randint(0, 1) for i in range(length)]
print(origin)

verify = rs.RS()
add_list = verify.add_for_list(origin)
print(add_list)

modify_list = add_list
error_position = random.randint(0, len(modify_list) - 1)
if modify_list[error_position] == 0:
    modify_list[error_position] = 1
else:
    modify_list[error_position] = 0
print(str(modify_list) + " error position = " + str(error_position))
verify_list = verify.verify_for_list(modify_list)
print(verify_list)

remove_list = verify.remove_for_list(verify_list, length)
print(remove_list)
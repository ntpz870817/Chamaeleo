from Chamaeleo.utils.monitor import Monitor


def connect_all(bit_segments, index_binary_length=None, need_logs=False):
    if index_binary_length is None:
        index_binary_length = int(len(str(bin(len(bit_segments)))) - 2)

    if need_logs:
        print("Add index (with the length " + str(index_binary_length) + ") in the binary matrix.")

    monitor = Monitor()
    connected_bit_segments = []
    for row in range(len(bit_segments)):
        connected_bit_segments.append(connect(row, bit_segments[row], index_binary_length))
        if need_logs:
            monitor.output(row + 1, len(bit_segments))

    return connected_bit_segments, index_binary_length


def connect(index, bit_segment, index_binary_length):
    bin_index = list(map(int, list(str(bin(index))[2:].zfill(index_binary_length))))
    one_list = bin_index + bit_segment

    return one_list


def divide_all(bit_segments, index_binary_length=None, need_logs=False):
    if index_binary_length is None:
        index_binary_length = int(len(str(bin(len(bit_segments)))) - 2)

    if need_logs:
        print("Divide index and data from binary matrix.")

    monitor = Monitor()
    indices = []
    divided_matrix = []

    for row in range(len(bit_segments)):
        index, data = divide(bit_segments[row], index_binary_length)
        indices.append(index)
        divided_matrix.append(data)
        if need_logs:
            monitor.output(row + 1, len(bit_segments))

    return indices, divided_matrix


def divide(bit_segment, index_binary_length):
    # Convert binary index to decimal.
    index = int("".join(list(map(str, bit_segment[:index_binary_length]))), 2)
    divided_list = bit_segment[index_binary_length:]

    return index, divided_list


def sort_order(indices, bit_segments, need_logs=False):
    monitor = Monitor()

    if need_logs:
        print("Restore data order according to index.")

    sorted_bit_segments = []

    for index in range(max(indices) + 1):
        if index in indices:
            sorted_bit_segments.append(bit_segments[indices.index(index)])
        else:
            sorted_bit_segments.append([0 for _ in range(len(bit_segments[0]))])

        if need_logs:
            monitor.output(index + 1, max(indices) + 1)

    return sorted_bit_segments

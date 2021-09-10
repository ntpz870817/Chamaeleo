import gzip
import pickle
import struct
from numpy import fromfile, array, uint8
from Chamaeleo.utils.monitor import Monitor


def read_bits_from_str(string, segment_length=120, need_logs=False):
    monitor = Monitor()

    if need_logs:
        print("Read binary matrix from string: " + string)

    data = []

    for value in bytes(string, encoding="utf8"):
        data += list(map(int, list(str(bin(value))[2:].zfill(8))))

    matrix = []
    for index in range(0, len(data), segment_length):
        if index + segment_length < len(data):
            matrix.append(data[index: index + segment_length])
        else:
            matrix.append(data[index:] + [0] * (segment_length - len(data[index:])))

        if need_logs:
            monitor.output(max(index + segment_length, len(data)), len(data))

    return matrix, len(data)


def write_bits_to_str(matrix, bit_size, need_logs=False):
    if need_logs:
        print("Write binary matrix to string.")
    monitor = Monitor()

    temp_list = []
    for index, row in enumerate(matrix):
        temp_list += row
        if need_logs:
            monitor.output(index, len(matrix))
    temp_list = temp_list[: bit_size]
    values = []
    for index in range(0, len(temp_list), 8):
        values.append(int("".join(list(map(str, temp_list[index: index + 8]))), 2))

    return str(bytes(values), encoding="utf8")


def compress_from_file(path):
    new_path = path + ".gz"
    compress_file = gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=open(new_path, "wb"))
    with open(path, "wb") as file:
        compress_file.write(file.read())
    compress_file.close()
    return new_path


def decompress_from_file(path):
    new_path = path[:-3]
    decompress_file = gzip.GzipFile(mode="rb", fileobj=open(path, "rb"))
    with open(new_path, "wb") as file:
        file.write(decompress_file.read())
    decompress_file.close()
    return new_path


def read_bits_from_file(path, segment_length=120, need_logs=True):
    monitor = Monitor()
    if need_logs:
        print("Read binary matrix from file: " + path)

    matrix, values = [], fromfile(file=path, dtype=uint8)
    for current, value in enumerate(values):
        matrix += list(map(int, list(str(bin(value))[2:].zfill(8))))
        if need_logs:
            monitor.output(current + 1, len(values))
    if len(matrix) % segment_length != 0:
        matrix += [0] * (segment_length - len(matrix) % segment_length)

    matrix = array(matrix)
    matrix = matrix.reshape(int(len(matrix) / segment_length), segment_length)

    if need_logs:
        print("There are " + str(len(values) * 8) + " bits in the inputted file. "
              + "Please keep this information in mind if you do not consider storing the model in serialization!")

    return matrix.tolist(), len(values) * 8


def write_bits_to_file(path, matrix, bit_size, need_logs=True):
    monitor = Monitor()

    with open(path, "wb+") as file:
        if need_logs:
            print("Write file from binary matrix: " + path)

        matrix = array(matrix).reshape(-1)
        for position in range(0, bit_size, 8):
            file.write(struct.pack("B", int("".join(list(map(str, matrix[position: position + 8]))), 2)))

            if need_logs:
                monitor.output(int(position / 8 + 1), int(bit_size / 8))

    return True


def read_dna_file(path, need_logs=True):
    monitor = Monitor()

    dna_sequences = []

    with open(path, "r") as file:
        if need_logs:
            print("Read DNA sequences from file: " + path)

        # Read current file by line
        lines = file.readlines()

        for index, line in enumerate(lines):
            dna_sequences.append(list(line.replace("\n", "")))

            if need_logs:
                monitor.output(index + 1, len(lines))

    return dna_sequences


def write_dna_file(path, dna_sequences, need_logs=False):
    monitor = Monitor()

    with open(path, "w") as file:
        if need_logs:
            print("Write DNA sequences to file: " + path)

        for index, dna_sequence in enumerate(dna_sequences):
            file.write("".join(dna_sequence) + "\n")

            if need_logs:
                monitor.output(index + 1, len(dna_sequences))

    return True


def save_model(path, model, need_logs=False):
    if need_logs:
        print("Save model to file: " + path)

    with open(path, "wb") as file:
        pickle.dump(model, file)


def load_model(path, need_logs=False):
    if need_logs:
        print("Load model from file: " + path)

    with open(path, "rb") as file:
        return pickle.load(file)

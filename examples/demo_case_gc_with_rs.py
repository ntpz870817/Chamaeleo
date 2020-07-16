"""
Name: Symmetrical testing for YYC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The demo case of Grass' Code with Reed-Solomon Code.
"""

import os
import Chamaeleo
import Chamaeleo.codec_factory as codec_factory
import Chamaeleo.utils.dir_checker as checker
from Chamaeleo.methods import gc
from Chamaeleo.methods.verifies import rs
from Chamaeleo.utils import data_handle
from Chamaeleo.utils.data_handle import DensityCalculator

root_path = os.path.dirname(Chamaeleo.__file__)
read_file_path = os.path.join(root_path, "data", "pictures", "Mona Lisa.jpg")
current_path = os.path.dirname(os.path.realpath(__file__))
generated_file_path = os.path.join(current_path, "generated_files")
checker.check_dir_exists(generated_file_path)
write_file_path = os.path.join(generated_file_path, "target.jpg")
dna_path = os.path.join(generated_file_path, "target.dna")
model_path = os.path.join(generated_file_path, "gc+rs.pkl")


if __name__ == "__main__":
    tool = gc.GC([index for index in range(48)])
    verify = rs.RS()
    codec_factory.encode(
        method=tool,
        input_path=read_file_path,
        output_path=dna_path,
        model_path=model_path,
        verify=verify,
        need_index=True,
        need_log=True
    )
    # del tool, verify
    codec_factory.decode(
        model_path=model_path,
        input_path=dna_path,
        output_path=write_file_path,
        has_index=True,
        need_log=True
    )

    print()
    matrix_1, _ = data_handle.read_binary_from_all(read_file_path, 120, False)
    dna_sequences = data_handle.read_dna_file(dna_path, False)
    calculator = DensityCalculator(matrix_1)
    calculator.set_final(dna_sequences)
    print("actual information density = " + str(round(calculator.get_density(), 2)))

    # compare two file
    matrix_2, _ = data_handle.read_binary_from_all(write_file_path, 120, False)
    print("source digital file == target digital file: " + str(matrix_1 == matrix_2))

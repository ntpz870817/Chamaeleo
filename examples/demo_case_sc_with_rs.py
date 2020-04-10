"""
Name: Symmetrical testing for YYC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The demo case of Yin-Yang Code.
"""

import os
import Chamaeleo
import Chamaeleo.codec_factory as codec_factory
import Chamaeleo.utils.dir_checker as checker
from Chamaeleo.methods import sc
from Chamaeleo.methods.verifies import rs

root_path = os.path.dirname(Chamaeleo.__file__)
read_file_path = os.path.join(root_path, "data", "books", "A Tale of Two Cities.pdf")
current_path = os.path.dirname(os.path.realpath(__file__))
generated_file_path = os.path.join(current_path, "generated_files")
checker.check_dir_exists(generated_file_path)
write_file_path = os.path.join(generated_file_path, "target.pdf")
dna_path = os.path.join(generated_file_path, "target.dna")
model_path = os.path.join(generated_file_path, "sc+rs.pkl")


if __name__ == "__main__":
    tool = sc.SC()
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
    del tool, verify
    codec_factory.decode(
        model_path=model_path,
        input_path=dna_path,
        output_path=write_file_path,
        has_index=True,
        need_log=True
    )

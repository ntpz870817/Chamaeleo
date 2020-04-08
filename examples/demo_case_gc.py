"""
Name: Symmetrical testing for GC

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): The demo case of Grass' Code.
"""

import os.path
import Chamaeleo
import Chamaeleo.codec_factory as codec_factory
import Chamaeleo.methods.gc as cc
import Chamaeleo.utils.dir_checker as checker

root_path = os.path.dirname(Chamaeleo.__file__)
read_file_path = os.path.join(root_path, "data", "books", "A Tale of Two Cities.pdf")
current_path = os.path.dirname(os.path.realpath(__file__))
generated_file_path = os.path.join(current_path, "generated_files")
checker.check_dir_exists(generated_file_path)
write_file_path = os.path.join(generated_file_path, "target.pdf")
dna_path = os.path.join(generated_file_path, "target.dna")
model_path = os.path.join(generated_file_path, "gc.pkl")


# noinspection PyProtectedMember
if __name__ == "__main__":
    tool = cc.GC([index for index in range(48)])
    codec_factory.encode(
        method=tool,
        input_path=read_file_path,
        output_path=dna_path,
        model_path=model_path,
        need_index=True,
        need_log=True,
    )
    del tool
    codec_factory.decode(
        model_path=model_path,
        input_path=dna_path,
        output_path=write_file_path,
        has_index=True,
        need_log=True,
    )

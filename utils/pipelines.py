import copy
import csv
import os
import random

import numpy
from terminaltables import AsciiTable
from Chamaeleo.methods.default import AbstractCodingAlgorithm, AbstractErrorCorrectionCode
from Chamaeleo.utils import data_handle, indexer
from Chamaeleo.utils.monitor import Monitor


class DefaultPipeline(object):

    def __init__(self, **info):
        self.need_logs = info["need_logs"] if "need_logs" in info else False
        self.monitor = Monitor()
        self.records = {}

    def __init_check__(self):
        if type(self.need_logs) != bool:
            raise ValueError("\"need_logs\" must be bool type!")

    def output_records(self, **info):
        raise NotImplementedError("\"output_records\" interface needs to be implemented!")


class TranscodePipeline(DefaultPipeline):

    def __init__(self, **info):
        super().__init__(**info)
        self.coding_scheme = info["coding_scheme"] if "coding_scheme" in info else None
        self.error_correction = info["error_correction"] if "error_correction" in info else None

        self.__init_check__()

        if self.need_logs:
            print("Create a transcoding pipeline.")
            self.coding_scheme.need_logs = True
            if self.error_correction is not None:
                self.error_correction.need_logs = True

    def __init_check__(self):
        super().__init_check__()
        if self.coding_scheme is None:
            raise ValueError("No coding scheme!")

        if not isinstance(self.coding_scheme, AbstractCodingAlgorithm):
            raise ValueError("The \"coding_scheme\" needs to "
                             + "inherit AbstractCodingScheme in methods/default.py!")

        if self.error_correction is not None and not isinstance(self.error_correction, AbstractErrorCorrectionCode):
            raise ValueError("The error correction needs to "
                             + "inherit AbstractErrorCorrectionCode in methods/default.py!")

    def transcode(self, **info):
        if "direction" in info:
            if info["direction"] == "t_c":
                segment_length = info["segment_length"] if "segment_length" in info else 120

                self.records["payload length"] = segment_length

                if "input_path" in info:
                    bit_segments, bit_size = data_handle.read_bits_from_file(info["input_path"], segment_length,
                                                                             self.need_logs)
                elif "input_string" in info:
                    bit_segments, bit_size = data_handle.read_bits_from_str(info["input_string"], segment_length,
                                                                            self.need_logs)
                else:
                    raise ValueError("There is no digital data input here!")

                original_bit_segments = copy.deepcopy(bit_segments)

                if "index" in info and info["index"]:
                    if "index_length" in info:
                        bit_segments, index_length = indexer.connect_all(bit_segments, info["index_length"],
                                                                         self.need_logs)
                    else:
                        bit_segments, index_length = indexer.connect_all(bit_segments, None, self.need_logs)

                    self.records["index length"] = index_length
                else:
                    self.records["index length"] = 0

                if self.error_correction is not None:
                    bit_segments, error_correction_length = self.error_correction.insert(bit_segments)
                    self.records["error-correction length"] = error_correction_length
                else:
                    self.records["error-correction length"] = 0

                results = self.coding_scheme.silicon_to_carbon(bit_segments, bit_size)

                dna_sequences = results["dna"]

                self.records["information density"] = round(results["i"], 3)
                self.records["encoding runtime"] = round(results["t"], 3)

                if "output_path" in info:
                    data_handle.write_dna_file(info["output_path"], dna_sequences, self.need_logs)

                return {"bit": original_bit_segments, "dna": dna_sequences}
            elif info["direction"] == "t_s":
                if "input_path" in info:
                    dna_sequences = data_handle.read_dna_file(info["input_path"], self.need_logs)
                elif "input_string" in info:
                    dna_sequences = []
                    for index, string in enumerate(info["input_string"]):
                        dna_sequences.append(string)
                else:
                    raise ValueError("There is no digital data input here!")

                original_dna_sequences = copy.deepcopy(dna_sequences)

                results = self.coding_scheme.carbon_to_silicon(dna_sequences)
                self.records["decoding runtime"] = round(results["t"], 3)

                bit_segments = results["bit"]
                bit_size = results["s"]

                if not bit_segments:
                    self.records["error rate"] = "100.00%"
                    return {"bit": None, "dna": original_dna_sequences}

                if self.error_correction is not None:
                    verified_data = self.error_correction.remove(bit_segments)
                    bit_segments = verified_data["bit"]
                    self.records["error rate"] = str(round(verified_data["e_r"] * 100, 2)) + "%"
                    self.records["error indices"] = str(verified_data["e_i"]).replace(", ", "-") \
                        if verified_data["e_i"] != [] else None
                    self.records["error bit segments"] = str(verified_data["e_bit"]).replace(", ", "-") \
                        if verified_data["e_bit"] != [] else None
                else:
                    self.records["error rate"] = None
                    self.records["error indices"] = None
                    self.records["error bit segments"] = None

                if not bit_segments:
                    return {"bit": None, "dna": original_dna_sequences}

                if "index" in info and info["index"]:
                    if "index_length" in info:
                        indices, bit_segments = indexer.divide_all(bit_segments, info["index_length"], self.need_logs)
                    else:
                        indices, bit_segments = indexer.divide_all(bit_segments, None, self.need_logs)

                    bit_segments = indexer.sort_order(indices, bit_segments, self.need_logs)

                if "output_path" in info:
                    data_handle.write_bits_to_file(info["output_path"], bit_segments, bit_size, self.need_logs)
                elif "output_string" in info:
                    string = data_handle.write_bits_to_str(bit_segments, bit_size, self.need_logs)
                    if self.need_logs:
                        print(string)

                return {"bit": bit_segments, "dna": original_dna_sequences}
            else:
                raise ValueError("Unknown parameter \"direction\", please use \"t_c\" or \"t_s\".")
        else:
            raise ValueError("Unknown parameter \"direction\", please use \"t_c\" or \"t_s\".")

    def output_records(self, **info):
        if "type" in info:
            if info["type"] == "path":
                if "path" in info:
                    with open(info["path"], "w", encoding="utf-8") as save_file:
                        for key, value in self.records.items():
                            if type(value) == str:
                                save_file.write(key + "," + value + "\n")
                            else:
                                save_file.write(key + "," + str(value) + "\n")
                else:
                    raise ValueError("\"path\" is unknown!")
            elif info["type"] == "string":
                if self.need_logs:
                    print("Transcoding log: ")
                    for key, value in self.records.items():
                        if type(value) == str:
                            print(key + ": " + value)
                        else:
                            print(key + ": " + str(value))

        return self.records


class RobustnessPipeline(DefaultPipeline):

    def __init__(self, **info):
        super().__init__(**info)

        self.coding_schemes = info["coding_schemes"] if "coding_schemes" in info else None
        self.error_corrections = info["error_corrections"] if "error_corrections" in info else None

        self.needed_indices = info["needed_indices"] if "needed_indices" in info else None

        self.file_paths = info["file_paths"] if "file_paths" in info else None

        self.nucleotide_insertion = info["nucleotide_insertion"] if "nucleotide_insertion" in info else 0
        self.nucleotide_mutation = info["nucleotide_mutation"] if "nucleotide_mutation" in info else 0
        self.nucleotide_deletion = info["nucleotide_deletion"] if "nucleotide_deletion" in info else 0
        self.sequence_loss = info["sequence_loss"] if "sequence_loss" in info else 0
        self.iterations = info["iterations"] if "iterations" in info else 1

        self.segment_length = info["segment_length"] if "segment_length" in info else 120
        self.index_length = info["index_length"] if "index_length" in info else None

        self.__init_check__()

        self.records = {
            "evaluation parameters": {
                "evaluated coding schemes": list(self.coding_schemes.keys()),
                "evaluated files": list(self.file_paths.keys()),
                "evaluated error correction": list(self.error_corrections.keys()),
                "original segment length": self.segment_length,
                "perturbation": {
                    "nucleotide insertion": self.nucleotide_insertion,
                    "nucleotide mutation": self.nucleotide_mutation,
                    "nucleotide deletion": self.nucleotide_deletion,
                    "sequence loss": self.sequence_loss,
                    "iterations": self.iterations
                }
            }
        }

    def __init_check__(self):
        super().__init_check__()
        if self.coding_schemes is None:
            raise ValueError("No coding scheme!")
        for name, coding_scheme in self.coding_schemes.items():
            if not isinstance(coding_scheme, AbstractCodingAlgorithm):
                raise ValueError("\"coding_scheme \" " + str(name) + "[" + str(type(coding_scheme))
                                 + "] needs to inherit AbstractCodingScheme in methods/default.py!")

        if self.error_corrections is None:
            raise ValueError("No error correction!")
        for name, error_correction in self.error_corrections.items():
            if error_correction is not None and not isinstance(error_correction, AbstractErrorCorrectionCode):
                raise ValueError("\"error_correction \" " + str(name) + "[" + str(type(error_correction))
                                 + "] needs to inherit AbstractErrorCorrectionCode in methods/default.py!")

        if self.needed_indices is None:
            raise ValueError("Whether each coding scheme needs \"index\" needs to be explained!")
        if len(self.coding_schemes) != len(self.needed_indices):
            raise ValueError("Coding scheme and its index requirements need to be matched one by one!")
        for index, needed_index in enumerate(self.needed_indices):
            if type(needed_index) is not bool:
                raise ValueError(str(index) in "\"needed_indices\" must be bool type!")

        if self.file_paths is None:
            raise ValueError("No digital file path!")
        for file_name, file_path in self.file_paths.items():
            if not os.path.exists(file_path):
                raise ValueError("The path of digital file " + str(file_name) + ": " + file_path + " does not exist!")

        if self.nucleotide_insertion > 1 or self.nucleotide_insertion < 0:
            raise ValueError("Wrong value in the \"nucleotide_insertion\", the value is in the range of [0, 1]!")
        if self.nucleotide_mutation > 1 or self.nucleotide_mutation < 0:
            raise ValueError("Wrong value in the \"nucleotide_mutation\", the value is in the range of [0, 1]!")
        if self.nucleotide_deletion > 1 or self.nucleotide_deletion < 0:
            raise ValueError("Wrong value in the \"nucleotide_deletion\", the value is in the range of [0, 1]!")
        if self.sequence_loss > 1 or self.sequence_loss < 0:
            raise ValueError("Wrong value in the \"sequence_loss\", the value is in the range of [0, 1]!")

        if self.segment_length <= -1 or type(self.segment_length) != int:
            raise ValueError("Wrong value in the \"segment_length\", "
                             "the value is in the range of [-1, +inf) and the type is int!")

        if self.iterations < 1 or type(self.iterations) != int:
            raise ValueError("Wrong value in the \"iterations\", "
                             "the value is in the range of [1, +inf) and the type is int!")

    def evaluate(self):
        results = {}
        task_index = 0
        total_task = len(self.coding_schemes) * len(self.error_corrections) * len(self.file_paths)
        for (scheme_name, coding_scheme), needed_index in zip(self.coding_schemes.items(), self.needed_indices):
            for correct_name, error_correction in self.error_corrections.items():
                for file_name, file_path in self.file_paths.items():
                    if self.need_logs:
                        print(">" * 50)
                        print("*" * 50)
                        print("Run task (" + str(task_index + 1) + "/" + str(total_task) + ").")
                        print("*" * 50)

                    pipeline = TranscodePipeline(coding_scheme=coding_scheme, error_correction=error_correction,
                                                 need_logs=self.need_logs)

                    encoded_data = pipeline.transcode(direction="t_c", input_path=file_path,
                                                      segment_length=self.segment_length,
                                                      index=needed_index, index_length=self.index_length)

                    pipeline_logs = []
                    for iteration in range(self.iterations):
                        chosen_count = int(len(encoded_data["dna"]) * (1 - self.sequence_loss))
                        dna_sequences = random.sample(copy.deepcopy(encoded_data["dna"]), chosen_count)

                        total_indices = [sequence_index for sequence_index in range(len(dna_sequences))]

                        # insertion errors
                        for insertion_iteration in range(int(len(dna_sequences) * self.nucleotide_insertion)):
                            chosen_index = random.choice(total_indices)
                            dna_sequences[chosen_index].insert(random.randint(0, len(dna_sequences[chosen_index]) - 1),
                                                               random.choice(['A', 'C', 'G', 'T']))

                        # mutation errors
                        for mutation_iteration in range(int(len(dna_sequences) * self.nucleotide_mutation)):
                            chosen_index = random.choice(total_indices)
                            chosen_index_in_sequence = random.randint(0, len(dna_sequences[chosen_index]) - 1)
                            chosen_nucleotide = dna_sequences[chosen_index][chosen_index_in_sequence]
                            dna_sequences[chosen_index][chosen_index_in_sequence] = \
                                random.choice(list(filter(lambda nucleotide: nucleotide != chosen_nucleotide,
                                                          ['A', 'C', 'G', 'T'])))

                        # deletion errors
                        for deletion_iteration in range(int(len(dna_sequences) * self.nucleotide_deletion)):
                            chosen_index = random.choice(total_indices)
                            del dna_sequences[chosen_index][random.randint(0, len(dna_sequences[chosen_index]) - 1)]

                        decoded_data = pipeline.transcode(direction="t_s", input_string=dna_sequences,
                                                          index=needed_index, index_length=self.index_length)

                        bit_segments = decoded_data["bit"]

                        temps = []
                        for bit_segment in bit_segments:
                            if bit_segment is not None:
                                temps.append(bit_segment)
                        bit_segments = temps

                        if len(bit_segments) == 0:
                            bit_segments = None

                        if bit_segments is None:
                            iter_log = pipeline.output_records()
                            iter_log["transcoding state"] = False
                            iter_log["success rate"] = "0.000%"
                        else:
                            iter_log = pipeline.output_records()
                            decoded_bit_segments, encoded_bit_segments = set(), set()
                            for bit_segment in bit_segments:
                                decoded_bit_segments.add(str(bit_segment))
                            for bit_segment in encoded_data["bit"]:
                                encoded_bit_segments.add(str(bit_segment))
                            intersection = encoded_bit_segments & decoded_bit_segments
                            success_count, total_count = len(intersection), len(encoded_bit_segments)
                            iter_log["transcoding state"] = (total_count == success_count)
                            iter_log["success count"] = success_count
                            iter_log["total count"] = total_count
                            iter_log["success rate"] = str(round(success_count / total_count * 100, 3)) + "%"

                        string = scheme_name + ", " + correct_name + ", " + file_name + ", "
                        string += str(iter_log["information density"]) + ", "
                        string += str(iter_log["encoding runtime"]) + ", "
                        string += str(iter_log["decoding runtime"]) + ", "
                        string += str(iter_log["transcoding state"]) + ", "
                        string += str(iter_log["success count"]) + ", "
                        string += str(iter_log["total count"]) + ", "
                        string += str(iter_log["success rate"])
                        if self.need_logs:
                            print(string)
                        pipeline_logs.append(iter_log)

                    result = {
                        "coding scheme": scheme_name, "error-correction": correct_name,
                        "file": file_name, "result": pipeline_logs
                    }
                    results["task " + str(task_index)] = result
                    task_index += 1

                    if self.need_logs:
                        print(">" * 50)
                        print()

        self.records["results"] = results

    def output_records(self, **info):
        if "type" in info:
            param_names = []
            param_values = []

            for key, value in self.records["evaluation parameters"].items():
                param_names.append(key)
                param_values.append(value)

            result_names = [
                "task id", "coding scheme", "error-correction", "file",
                "payload length", "index length", "error-correction length",
                "information density", "encoding runtime", "decoding runtime",
                "error rate", "error indices", "error bit segments",
                "transcoding state", "success rate"
            ]
            result_data_group = []
            for task_id, data in self.records["results"].items():
                result_data = [
                    task_id, data["coding scheme"], data["error-correction"], data["file"],
                ]
                for one_data in data["result"]:
                    one_iteration = [
                        one_data["payload length"], one_data["index length"], one_data["error-correction length"],
                        one_data["information density"], one_data["encoding runtime"], one_data["decoding runtime"],
                        one_data["error rate"], one_data["error indices"], one_data["error bit segments"],
                        one_data["transcoding state"], one_data["success rate"]
                    ]

                    result_data_group.append(result_data + copy.deepcopy(one_iteration))
            if info["type"] == "path":
                if "path" in info:
                    with open(info["path"], "w", encoding="utf-8") as save_file:
                        save_file.write(str(param_names)[1: -1].replace("\'", "") + "\n")
                        save_file.write(str(param_values)[1: -1].replace("\'", "") + "\n")
                        save_file.write(str(result_names)[1: -1].replace("\'", "") + "\n")
                        for result_data in result_data_group:
                            save_file.write(str(result_data)[1: -1].replace("\'", "") + "\n")
                else:
                    raise ValueError("\"path\" is unknown!")
            elif info["type"] == "string":
                if self.need_logs:
                    print("Evaluation log: ")
                    print(str(param_names)[1: -1].replace("\'", ""))
                    print(str(param_values)[1: -1].replace("\'", ""))
                    print(str(result_names)[1: -1].replace("\'", ""))
                    for result_data in result_data_group:
                        print(str(result_data)[1: -1].replace("\'", ""))

        return self.records


class BasicFeaturePipeline(DefaultPipeline):

    def __init__(self, **info):
        super().__init__(**info)

        self.coding_schemes = info["coding_schemes"] if "coding_schemes" in info else None
        self.needed_indices = info["needed_indices"] if "needed_indices" in info else None

        self.file_paths = info["file_paths"] if "file_paths" in info else None

        self.segment_length = info["segment_length"] if "segment_length" in info else 120
        self.index_length = info["index_length"] if "index_length" in info else None

        self.__init_check__()

        self.records = {
            "index parameters": {
                "evaluated coding schemes": list(self.coding_schemes.keys()),
                "evaluated files": list(self.file_paths.keys()),
                "segment length": self.segment_length
            }
        }

    def __init_check__(self):
        super().__init_check__()
        if self.coding_schemes is None:
            raise ValueError("No coding scheme!")
        for name, coding_scheme in self.coding_schemes.items():
            if not isinstance(coding_scheme, AbstractCodingAlgorithm):
                raise ValueError("\"coding_scheme \" " + str(name) + "[" + str(type(coding_scheme))
                                 + "] needs to inherit AbstractCodingScheme in methods/default.py!")

        if self.needed_indices is None:
            raise ValueError("Whether each coding scheme needs \"index\" needs to be explained!")
        if len(self.coding_schemes) != len(self.needed_indices):
            raise ValueError("Coding scheme and its index requirements need to be matched one by one!")
        for index, needed_index in enumerate(self.needed_indices):
            if type(needed_index) is not bool:
                raise ValueError(str(index) in "\"needed_indices\" must be bool type!")

        if self.file_paths is None:
            raise ValueError("No digital file path!")
        for file_name, file_path in self.file_paths.items():
            if not os.path.exists(file_path):
                raise ValueError("The path of digital file " + str(file_name) + ": " + file_path + " does not exist!")

        if self.segment_length <= -1 or type(self.segment_length) != int:
            raise ValueError("Wrong value in the \"segment_length\", "
                             "the value is in the range of [-1, +inf) and the type is int!")

    def calculate(self):
        results = {}
        task_index = 0
        total_task = len(self.coding_schemes) * len(self.file_paths)
        for file_name, file_path in self.file_paths.items():
            original_bit_segments, bit_size = data_handle.read_bits_from_file(file_path,
                                                                              self.segment_length,
                                                                              self.need_logs)
            bit_segments_with_indices, index_length = indexer.connect_all(original_bit_segments, self.index_length,
                                                                          self.need_logs)
            for (scheme_name, coding_scheme), needed_index in zip(self.coding_schemes.items(), self.needed_indices):
                coding_scheme.need_logs = True
                if self.need_logs:
                    print(">" * 50)
                    print("*" * 50)
                    print("Run task (" + str(task_index + 1) + "/" + str(total_task) + ").")
                    print("*" * 50)

                if needed_index:
                    bit_segments = bit_segments_with_indices
                else:
                    bit_segments = original_bit_segments

                dna_sequences = coding_scheme.silicon_to_carbon(bit_segments, bit_size)["dna"]

                gc_distribution = [0 for _ in range(101)]
                homo_distribution = [0 for _ in range(max(list(map(len, dna_sequences))))]

                for dna_sequence in dna_sequences:
                    dna_segment = "".join(dna_sequence)
                    gc_content = int(((dna_segment.count("C") + dna_segment.count("G")) / len(dna_segment) * 100) + 0.5)
                    gc_distribution[gc_content] += 1
                    for homo_length in [homo + 1 for homo in range(len(dna_sequence))][::-1]:
                        is_find = False
                        missing_segments = ["A" * homo_length, "C" * homo_length, "G" * homo_length, "T" * homo_length]
                        for missing_segment in missing_segments:
                            if missing_segment in dna_segment:
                                is_find = True
                                homo_distribution[homo_length] += 1
                                break
                        if is_find:
                            break
                if self.need_logs:
                    print(">" * 50)
                    print()

                results["task " + str(task_index)] = {
                    "coding scheme": scheme_name,
                    "file": file_name,
                    "gc": str(gc_distribution).replace(", ", "-"),
                    "homo": str(homo_distribution).replace(", ", "-")
                }
                task_index += 1

        self.records["results"] = results

    # noinspection PyTypeChecker
    def output_records(self, **info):
        if "type" in info:
            param_names = []
            param_values = []

            for key, value in self.records["index parameters"].items():
                param_names.append(key)
                param_values.append(value)

            result_names = [
                "task id", "coding scheme", "file", "gc content", "maximum homopolymer"
            ]
            result_data_group = []
            for task_id, data in self.records["results"].items():
                result_data_group.append([task_id, data["coding scheme"], data["file"], data["gc"] + data["homo"]])
            if info["type"] == "path":
                if "path" in info:
                    with open(info["path"], "w", encoding="utf-8") as save_file:
                        save_file.write(str(param_names)[1: -1].replace("\'", "") + "\n")
                        save_file.write(str(param_values)[1: -1].replace("\'", "") + "\n")
                        save_file.write(str(result_names)[1: -1].replace("\'", "") + "\n")
                        for result_data in result_data_group:
                            save_file.write(str(result_data)[1: -1].replace("\'", "") + "\n")
                else:
                    raise ValueError("\"path\" is unknown!")
            elif info["type"] == "string":
                if self.need_logs:
                    print("Index log: ")
                    print(str(param_names)[1: -1].replace("\'", ""))
                    print(str(param_values)[1: -1].replace("\'", ""))
                    print(str(result_names)[1: -1].replace("\'", ""))
                    for result_data in result_data_group:
                        print(str(result_data)[1: -1].replace("\'", ""))

        return self.records


class OptimalChoicePipeline(DefaultPipeline):

    def __init__(self, **info):
        super().__init__(**info)

        self.coding_schemes = info["coding_schemes"] if "coding_schemes" in info else None
        self.feature_log_path = info["feature_log_path"] if "feature_log_path" in info else None
        self.robustness_log_path = info["robustness_log_path"] if "robustness_log_path" in info else None

        self.__init_check__()

    def __init_check__(self):
        super().__init_check__()
        if self.coding_schemes is None:
            raise ValueError("No coding scheme!")
        for name, coding_scheme in self.coding_schemes.items():
            if not isinstance(coding_scheme, AbstractCodingAlgorithm):
                raise ValueError("\"coding_scheme \" " + str(name) + "[" + str(type(coding_scheme))
                                 + "] needs to inherit AbstractCodingScheme in methods/default.py!")

        if self.feature_log_path is None:
            raise ValueError("\"feature_log_path\" must be available!")

        if self.robustness_log_path is None:
            raise ValueError("\"robustness_log_path\" must be available!")

    def calculate_best(self):
        information_density_results = {}
        gc_suitable_rate_results = {}
        gc_bias_results = {}
        homopolymer_results = {}
        recover_results = {}

        with open(self.feature_log_path, "r") as file:
            rows = csv.reader(file)
            for index, row in enumerate(rows):
                if index > 2:
                    name = row[1][1:]
                    [r1, r2] = row[3].split("][")
                    gc = numpy.array(list(map(int, r1[1:].replace("[", "").split("-"))))
                    gc = gc / numpy.sum(gc)
                    rate = numpy.sum(gc[41: 61])
                    if row[1] in gc_suitable_rate_results:
                        gc_suitable_rate_results[name].append(rate)
                    else:
                        gc_suitable_rate_results[name] = [rate]
                    max_bias = max(numpy.nonzero(gc)[0][-1] - 51, 51 - numpy.nonzero(gc)[0][1])
                    if row[1] in gc_bias_results:
                        gc_bias_results[name].append(max_bias)
                    else:
                        gc_bias_results[name] = [max_bias]
                    ho = numpy.array(list(map(int, r2[:-1].split("-"))))
                    if row[1] in homopolymer_results:
                        homopolymer_results[name].append(numpy.nonzero(ho)[0][-1])
                    else:
                        homopolymer_results[name] = [numpy.nonzero(ho)[0][-1]]

        with open(self.robustness_log_path, "r") as file:
            rows = csv.reader(file)
            for index, row in enumerate(rows):
                if index > 2:
                    name = row[1][1:]
                    information_density = float(row[7])
                    recover = float(row[14].replace("%", "")) / 100.0
                    if row[1] in information_density_results:
                        information_density_results[name].append(information_density)
                    else:
                        information_density_results[name] = [information_density]
                    if row[1] in recover_results:
                        recover_results[name].append(recover)
                    else:
                        recover_results[name] = [recover]

        names = set()
        for name, value in gc_suitable_rate_results.items():
            names.add(name)
        for name, value in recover_results.items():
            names.add(name)

        title = [
            "scheme id", "coding scheme", "average information density",
            "GC content within 40% - 60%", "maximum bias of GC content", "maximum homopolymer",
            "average recover rate"
        ]

        record_group = [title]
        for index, name in enumerate(list(names)):
            one_record = [
                str(index + 1), name,
                str(numpy.mean(numpy.array(information_density_results[name]))),
                str(round(numpy.mean(numpy.array(gc_suitable_rate_results[name])) * 100, 2)) + "%",
                str(round(numpy.max(numpy.array(gc_bias_results[name])), 2)) + "%",
                str(numpy.max(numpy.array(homopolymer_results[name]))) + "nt",
                str(round(numpy.mean(numpy.array(recover_results[name])) * 100, 2)) + "%"
            ]
            record_group.append(one_record)

        print("Evaluation results.")
        table_instance = AsciiTable(record_group, title)
        for i in range(len(title)):
            table_instance.justify_columns[i] = 'center'
        print(table_instance.table)

    def output_records(self, **info):
        selected_coding_scheme = self.coding_schemes[info["selected_coding_scheme"]]
        pipeline = TranscodePipeline(coding_scheme=selected_coding_scheme, error_correction=info["error_correction"],
                                     need_logs=info["need_logs"])
        encoded_data = pipeline.transcode(direction="t_c",
                                          input_path=info["input_path"], output_path=info["output_path"],
                                          segment_length=info["segment_length"], index=info["needed_index"])
        return {
            "dna": encoded_data["dna"],
            "information density": pipeline.records["information density"],
            "encoding runtime": pipeline.records["encoding runtime"]
        }

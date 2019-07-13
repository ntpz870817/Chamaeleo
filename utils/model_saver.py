"""
Name: Model Saver

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): (1) Save model to file.
             (2) Load model from file.
"""


import pickle

import sys

from utils import log


# noinspection PyProtectedMember
def save_model(path, model):
    """
    introduction: Save model to file.

    :param path: The path of file.
                  Usually in the models directory.

    :param model: Current model for encoding.
                   Type: .pkl
                   i.e. YYC or DDC.
    """

    log.output(
        log.NORMAL,
        str(__name__),
        str(sys._getframe().f_code.co_name),
        "Save model to file: " + path,
    )
    with open(path, "wb") as file:
        pickle.dump(model, file)


# noinspection PyProtectedMember
def load_model(path):
    """
    introduction: Load model from file.

    :param path: The path of file.
                  Type: .pkl

    :return: needed model.
              i.e. YYC or DDC.
    """

    log.output(
        log.NORMAL,
        str(__name__),
        str(sys._getframe().f_code.co_name),
        "Load model from file: " + path,
    )
    with open(path, "rb") as file:
        return pickle.load(file)

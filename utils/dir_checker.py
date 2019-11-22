import os


def check_dir_exists(path: str):
    if not os.path.isfile(path):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            pass
    else:
        raise ValueError("The given path can not be found/created.")

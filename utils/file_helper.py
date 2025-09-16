import constants
import os


def get_highscore() -> int:
    if not os.path.exists(constants.HIGHSCORE_FILE_PATH):
        return 0
    with open(constants.HIGHSCORE_FILE_PATH, "r") as f:
        try:
            val = int(f.read())
        except ValueError:
            val = 0
    return val


def set_highscore(score: int) -> None:
    if not os.path.exists(constants.HIGHSCORE_FILE_PATH):
        os.mkdir("/".join(constants.HIGHSCORE_FILE_PATH.split("/")[:-1]))
    with open(constants.HIGHSCORE_FILE_PATH, "w") as f:
        f.write(str(score))


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def write_file(path: str, data: str) -> None:
    with open(path, "w") as f:
        f.write(data)


def append_file(path: str, data: str) -> None:
    with open(path, "a") as f:
        f.write(data)

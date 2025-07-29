from app.config import PICKLE_FILE_PATH
from functools import lru_cache
import pickle
import dataclasses as dc


@dc.dataclass
class PickleHandler:
    """Class to handle pickle methods. Doesn't handle exceptions, Parent need to handle exceptions"""

    @staticmethod
    def save_data_to_pickle(data, file_name: str = "facts.pkl"):
        with open(f"{PICKLE_FILE_PATH}/{file_name}", "wb") as fp:
            # noinspection PyTypeChecker
            pickle.dump(data, fp)

        return True

    @staticmethod
    @lru_cache
    def load_data_from_cache(file_name: str = "facts.pkl"):
        with open(f"{PICKLE_FILE_PATH}/{file_name}", "rb") as fp:
            data = pickle.load(fp)

        return data

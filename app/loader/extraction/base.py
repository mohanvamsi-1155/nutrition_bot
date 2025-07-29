from abc import ABC, abstractmethod
from app.helper.utils.logger import Logger

from app.config import PICKLE_FILE_PATH
from app.helper.utils.chunk_processor import Chunk
import json
import time
from app.helper.data.pickle_helper import PickleHandler
from app.ai.embeddings_handler import EmbeddingsHandler


class Extractor(ABC):
    def __init__(self, file_type):
        self.file_type = file_type
        self.logger = Logger(name="main_logger", level="DEBUG")
        self.pickle_helper = PickleHandler()
        self.embeddings_handler = EmbeddingsHandler()

    @abstractmethod
    def extract_info(self):
        pass

    def dump_data_to_pickle(self, chunks: list[Chunk]):
        try:
            self.logger.debug(f"Formatted Chunks {len(chunks)}")
            _pickle_obj = {
                "data": chunks,
                "last_modified_time": int(time.time())
            }
            self.logger.debug(f"Dumping data to pickle : {_pickle_obj}")

            _ = self.pickle_helper.save_data_to_pickle(_pickle_obj)

            self.logger.info("Successfully saved data to obj")
            return True
        except Exception as e:
            self.logger.exception(f"Unhandled Exception : {e}")
            return False

    def load_data_from_pickle(self):
        try:
            self.logger.info(f"Fetching data from path : {PICKLE_FILE_PATH}")

            return self.pickle_helper.load_data_from_cache()
        except Exception as e:
            self.logger.exception(f"Unable to parse the data for path {PICKLE_FILE_PATH}/facts.pkl : {e}")
            return None

    def create_embeddings(self, sentences: list):
        """
        Compute embeddings for a given list of sentences
        :param sentences: A list containing sentences parsed from source
        :return: A List of tensors
        """

        return self.embeddings_handler.encode_sentences(sentences=sentences)

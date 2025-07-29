from app.loader.extraction.base import Extractor
from app.config import SupportedMIMETypes


class TextExtractor(Extractor):
    def __init__(self, text_file_path):
        super().__init__(SupportedMIMETypes.TEXT.value)
        self.text_file_path = text_file_path

    def extract_info(self):
        pass

    def save_data_to_pickle(self):
        pass
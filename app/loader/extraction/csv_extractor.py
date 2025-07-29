from app.loader.extraction.base import Extractor
from app.config import SupportedMIMETypes


class CSVContentExtractor(Extractor):
    def __init__(self, csv_file_path):
        super().__init__(SupportedMIMETypes.CSV.value)
        self.csv_file_path = csv_file_path

    def extract_info(self):
        pass

    def save_data_to_pickle(self):
        pass
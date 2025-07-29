from app.loader.extraction.base import Extractor
from app.config import SupportedMIMETypes


class WebCrawlExtractor(Extractor):
    def __init__(self, file_url):
        super().__init__(SupportedMIMETypes.HTML.value)
        self.file_url = file_url

    def extract_info(self):
        pass

    def save_data_to_pickle(self):
        pass
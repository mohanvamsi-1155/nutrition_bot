from app.loader.extraction.base import Extractor
from app.config import SupportedMIMETypes


class WebCrawlExtractor(Extractor):
    def __init__(self, http_url):
        super().__init__(SupportedMIMETypes.HTML.value)
        self.http_url = http_url

    def extract_info(self):
        NotImplemented()

    def save_data_to_pickle(self):
        NotImplemented()
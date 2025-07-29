import dataclasses as dc
from app.config import SupportedMIMETypes
from app.loader.extraction.pdf_extractor import PDFDataExtractor
from app.loader.extraction.api_extractor import APIExtractor
from app.loader.extraction.html_extractor import WebCrawlExtractor
from app.loader.extraction.csv_extractor import CSVContentExtractor
from app.loader.extraction.text_extractor import TextExtractor


@dc.dataclass
class ExtractorMapper:
    __MAPPING__ = {
        SupportedMIMETypes.CSV.value: CSVContentExtractor,
        SupportedMIMETypes.EXCEL.value: CSVContentExtractor,
        SupportedMIMETypes.PDF.value: PDFDataExtractor,
        SupportedMIMETypes.HTML.value: WebCrawlExtractor,
        SupportedMIMETypes.TEXT.value: TextExtractor,
        SupportedMIMETypes.API.value: APIExtractor
    }

    @classmethod
    def get_mapper_class(cls, mime_type):
        """Return the appropriate class object for the given mime_type"""
        return cls.__MAPPING__.get(mime_type)

    @classmethod
    def invoke_mapper_class(cls, mime_type, **kwargs):
        mapping_class = cls.get_mapper_class(mime_type)
        return mapping_class(**kwargs).extract_info()


if __name__ == "__main__":
    file_path = "/media/mohan/NewVolume/zenoti_study/nutrition_bot/docs/caffeine_on_health.pdf"
    print(ExtractorMapper().invoke_mapper_class(mime_type="PDF", pdf_path=file_path))

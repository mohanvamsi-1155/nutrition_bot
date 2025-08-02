import dataclasses as dc
from typing import Union, Type

from app.config import SupportedMIMETypes, COLLECTION_NAME
from app.helper.data.chroma_helper import ChromaHelper
from app.loader.extraction.pdf_extractor import PDFDataExtractor
from app.loader.extraction.api_extractor import APIExtractor
from app.loader.extraction.html_extractor import WebCrawlExtractor
from app.loader.extraction.csv_extractor import CSVContentExtractor
from app.loader.extraction.text_extractor import TextExtractor
from app.models.model import DataLoaderMethod
from app.helper.utils.logger import Logger


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
    def get_mapper_class(cls, mime_type) -> Type:
        """Return the appropriate class object for the given mime_type"""
        return cls.__MAPPING__.get(mime_type)

    @classmethod
    def invoke_mapper_class(cls, mime_type, payload: DataLoaderMethod):
        mapping_class = cls.get_mapper_class(mime_type)
        if not mapping_class:
            raise ValueError("Invalid mime_type")
        if mapping_class == CSVContentExtractor:
            return CSVContentExtractor(csv_file_path=payload.csv_file_path).extract_info()
        elif mapping_class == PDFDataExtractor:
            return PDFDataExtractor(pdf_path=payload.pdf_path).extract_info()
        elif mapping_class == WebCrawlExtractor:
            return WebCrawlExtractor(http_url=payload.http_url).extract_info()
        elif mapping_class == TextExtractor:
            return TextExtractor(text_file_path=payload.text_file_path).extract_info()
        elif mapping_class == APIExtractor:
            return APIExtractor(
                api_url=payload.api_url,
                api_method=payload.api_method,
                authorization_type=payload.authorization_type,
                authorization_key=payload.authorization_key,
                custom_headers=payload.custom_headers,
                custom_query_params=payload.custom_query_params,
                custom_request_body=payload.custom_request_body
            ).extract_info()
        raise ValueError("Invalid instance class")


class Loader:
    def __init__(self, payload: DataLoaderMethod):
        self.payload = payload
        self.logger = Logger(name="loader_logger", level="INFO")

    @staticmethod
    def _respond_(status_code: int = 200, response_body: Union[str, dict] = "Success!"):
        return {
            "body": response_body if isinstance(response_body, dict) else {"status": response_body},
            "status_code": status_code
        }

    def load_data(self):
        """Load the data from appropriate sources and store the data in a chromaDB"""
        try:
            # Step 01: Identify the appropriate type and extract data
            chunks = ExtractorMapper.invoke_mapper_class(self.payload.mime_type, self.payload)
            self.logger.info("Chunks processed successfully")

            # Step 02: initialize chroma client
            chroma_helper = ChromaHelper(collection_name=COLLECTION_NAME)
            chroma_helper.create_client()

            # Step 03: Save chunks
            chroma_helper.upsert_data(chunks)
            self.logger.info("Chunks saved to chroma DB!")

            # Step 04: Respond
            return self._respond_()
        except ValueError as ve:
            self.logger.exception(f"Invalid Parameters : {ve}")
            return self._respond_(status_code=400, response_body=f"Invalid data : {ve}")
        except Exception as e:
            self.logger.exception(f"Unhandled Exception : {e}")
            return self._respond_(status_code=500, response_body=f"Unhandled Exception: {e}")


if __name__ == "__main__":
    file_path = "/media/mohan/NewVolume/zenoti_study/nutrition_bot/docs/caffeine_on_health.pdf"
    print(ExtractorMapper.invoke_mapper_class(mime_type="PDF", payload=DataLoaderMethod(
        **{"mime_type": "PDF", "pdf_path": file_path})))

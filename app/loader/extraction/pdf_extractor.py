from app.loader.extraction.base import Extractor
from app.config import SupportedMIMETypes
from unstructured.partition.auto import partition
import app.decorators.timing as decorator
from app.helper.utils.chunk_processor import Chunk


class PDFDataExtractor(Extractor):
    _SUPPORTED_CATEGORIES_ = {"NarrativeText"}

    def __init__(self, pdf_path):
        super().__init__(SupportedMIMETypes.PDF.value)
        self.pdf_path = pdf_path

    @decorator.timing
    def extract_info(self):
        try:
            chunks = []
            file_name = self.pdf_path.split("/")[-1] if len(self.pdf_path.split("/")) > 1 else self.pdf_path
            elements = partition(self.pdf_path)
            for element in elements:
                if element.category not in self._SUPPORTED_CATEGORIES_:
                    continue
                # compute embeddings
                embeddings = self.create_embeddings([element.text])
                chunks.append(
                    Chunk(chunk_text=element.text, chunk_embeddings=embeddings, chunk_metadata={"source": file_name})
                )
            return chunks

        except Exception as e:
            self.logger.exception(f"Unhandled Exception : {e}")
            raise

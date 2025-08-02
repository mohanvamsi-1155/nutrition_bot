from app.loader.extraction.base import Extractor
from app.config import SupportedMIMETypes
from unstructured.partition.auto import partition
import app.decorators.timing as decorator
from app.helper.utils.chunk_processor import Chunk
from nltk.tokenize import sent_tokenize

import nltk

nltk.download("punkt")


class PDFDataExtractor(Extractor):
    _SUPPORTED_CATEGORIES_ = {"NarrativeText"}

    def __init__(self, pdf_path):
        super().__init__(SupportedMIMETypes.PDF.value)
        self.pdf_path = pdf_path

    @decorator.timing
    def process_elements(self, semantic_chunks):

        chunks = []
        for para in semantic_chunks:
            sentences = sent_tokenize(para)
            chunks.append(" ".join(sentences))

        final_chunks = []

        for chunk in chunks:
            if chunk.startswith("References"):
                break
            else:
                final_chunks.append(chunk)

        return final_chunks

    @decorator.timing
    def extract_info(self):
        try:
            chunks = []
            file_name = self.pdf_path.split("/")[-1] if len(self.pdf_path.split("/")) > 1 else self.pdf_path
            elements = partition(self.pdf_path)
            semantic_chunks = []
            for element in elements:
                if element.category not in self._SUPPORTED_CATEGORIES_ and element.text.strip() == "":
                    continue
                semantic_chunks.append(element.text.strip())

            processed_chunks = self.process_elements(semantic_chunks)

            for processed_chunk in processed_chunks:
                # compute embeddings
                embeddings = self.create_embeddings(processed_chunk)
                chunks.append(
                    Chunk(chunk_text=processed_chunk, chunk_embeddings=embeddings, chunk_metadata={"source": file_name})
                )

            return chunks

        except Exception as e:
            self.logger.exception(f"Unhandled Exception : {e}")
            raise

import dataclasses as dc
from app.ai.embeddings_handler import EmbeddingsHandler
from app.ai.llm_handler import LLMHandler
from app.helper.data.chroma_helper import ChromaHelper
from app.config import COLLECTION_NAME
from app.helper.utils.logger import Logger


@dc.dataclass
class Searcher:
    query: str
    embedding_helper = EmbeddingsHandler()
    chroma_handler = ChromaHelper(COLLECTION_NAME)
    llm_handler = LLMHandler()
    logger = Logger(name="searcher_logger", level="DEBUG")

    def search(self, metadata: None):
        """Search function"""
        try:
            # compute embeddings for query
            self.logger.info(f"Query : {self.query} & metadata: {metadata}")
            query_embeddings = self.embedding_helper.encode_sentence(self.query)

            # find the relative matches
            self.chroma_handler.create_client()
            results = self.chroma_handler.fetch_data(query_embeddings)
            self.logger.debug(f"Results : {results}")

            documents = results.get("documents", [])

            # query llm
            response = self.llm_handler.query_model(self.query, documents[0])

            return response

        except ValueError as ve:
            self.logger.exception(f"Invalid Parameters: {ve}")
        except Exception as e:
            self.logger.exception(f"Unhandled Exception: {e}")

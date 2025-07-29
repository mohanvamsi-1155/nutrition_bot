from app.helper.utils.logger import Logger

from torch import Tensor

from app.config import EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer
import dataclasses as dc
import app.decorators.timing as decorator
import numpy as np
from numpy.linalg import norm


@dc.dataclass
class EmbeddingsHandler:
    """
    Helper for computing and comparing embeddings for chunks
    """
    logger = Logger(name="embedding_logger", level="DEBUG")
    embedding_model = None

    @decorator.timing
    def load_model(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

    @decorator.timing
    def encode_sentence(self, sentence: str) -> Tensor:
        if not self.embedding_model:
            self.logger.info("model instance not found, loading")
            self.load_model()

        embeddings = self.embedding_model.encode(sentence)
        self.logger.info("embeddings prepared")
        self.logger.debug(f"Shape: {embeddings.shape}")

        return embeddings

    @decorator.timing
    def encode_sentences(self, sentences: list):
        if not self.embedding_model:
            self.logger.info("model instance not found, loading")
            self.load_model()

        embeddings = self.embedding_model.encode(sentences)
        self.logger.info("embeddings prepared")
        self.logger.debug(f"Shape: {embeddings.shape}")

        return embeddings

    @staticmethod
    def cosine_similarity(_array1, _array2):
        return np.dot(_array1, _array2) / (norm(_array1) * norm(_array2))

    @decorator.timing
    def compute_cosine_similarity(self, train_encodings, query_encoding):
        """Calculate cosine similarity scores and return the scores as an array for index lookup"""

        scores = []
        try:
            for idx, train_encoding in enumerate(train_encodings):
                score = self.cosine_similarity(train_encoding, query_encoding)
                self.logger.debug(f"Para : {idx} || Score : {score}")
                scores.append(score)

        except Exception as e:
            self.logger.exception(f"unhandled exception : {e}")
            scores.append(0.0)

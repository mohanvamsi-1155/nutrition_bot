import dataclasses as dc
import chromadb
from typing import List
from app.config import PERSISTENT_CHROMA_STORAGE

from chromadb import QueryResult

from app.helper.utils.chunk_processor import Chunk
import app.decorators.timing as decorator


@dc.dataclass
class ChromaHelper:
    collection_name: str
    chroma_client = None

    @decorator.timing
    def create_client(self):
        if not self.chroma_client:
            self.chroma_client = chromadb.PersistentClient(path=PERSISTENT_CHROMA_STORAGE)

    @decorator.timing
    def get_or_create_collection(self) -> chromadb.Collection:
        return self.chroma_client.get_or_create_collection(self.collection_name)

    @decorator.timing
    def upsert_data(self, chunks: List[Chunk]):
        _docs = []
        _embeddings = []
        _ids = []
        _mappings = []
        for chunk in chunks:
            _docs.append(chunk.chunk_text)
            if isinstance(chunk.chunk_embeddings[0], list):
                _embeddings.append(chunk.chunk_embeddings[0])
            else:
                _embeddings.append(chunk.chunk_embeddings)
            _ids.append(chunk.chunk_id)
            _mappings.append({
                "chunk_id": chunk.chunk_id,
                "source": chunk.chunk_metadata.get("source", "NA")
            })

        _collection = self.get_or_create_collection()

        _collection.upsert(
            embeddings=_embeddings,
            metadatas=_mappings,
            documents=_docs,
            ids=_ids
        )

    @decorator.timing
    def fetch_data(self, query_embedding) -> QueryResult:
        _collection = self.get_or_create_collection()
        results = _collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["distances", "documents", "embeddings"]
        )

        return results

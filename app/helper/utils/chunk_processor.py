import dataclasses as dc
import uuid


@dc.dataclass
class Chunk:
    chunk_metadata: str
    chunk_embeddings: list
    chunk_summary: str = ""
    chunk_id: str = str(uuid.uuid4())

    def save_embeddings(self, embeddings):
        self.chunk_embeddings = embeddings

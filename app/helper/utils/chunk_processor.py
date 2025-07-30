import dataclasses as dc
import uuid


@dc.dataclass
class Chunk:
    chunk_text: str
    chunk_embeddings: list
    chunk_summary: str = ""
    chunk_id: str = dc.field(default_factory=lambda: str(uuid.uuid4()))
    chunk_metadata: dict = dc.field(default_factory=dict)

    def save_embeddings(self, embeddings):
        self.chunk_embeddings = embeddings

from enum import Enum


class SupportedMIMETypes(Enum):
    CSV = "CSV"
    EXCEL = "EXCEL"
    PDF = "PDF"
    HTML = "HTML"
    TEXT = "TEXT"
    API = "API"


DATA_STORAGE_DIR = "docs/"
PICKLE_FILE_PATH = "storage/"

################
### AI STUFF ###
################

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "nutrition_chunks"
PERSISTENT_CHROMA_STORAGE = "/media/mohan/NewVolume/zenoti_study/nutrition_bot/storage/chromaDB"
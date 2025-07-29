from app.loader.extraction.base import Extractor
from app.config import SupportedMIMETypes
import requests
import app.decorators.timing as decorator
from app.helper.utils.chunk_processor import Chunk
from nltk.tokenize import sent_tokenize


class APIExtractor(Extractor):
    REQUESTS_GET = "GET"
    REQUESTS_POST = "POST"
    AUTH_TYPE_BASIC = "BASIC"
    AUTH_TYPE_BEARER = "BEARER"
    AUTH_TYPE_API_KEY = "API_KEY"
    TIMEOUT = 10

    def __init__(self, **kwargs):
        super().__init__(SupportedMIMETypes.API.value)
        self.api_url = kwargs.get("api_url", None)
        self.api_method = kwargs.get("api_method", "GET").upper()
        self.authorization_key = kwargs.get("authorization_key", None)
        self.authorization_type = kwargs.get("authorization_type", None)
        self.custom_headers = kwargs.get("custom_headers", None)
        self.custom_request_body = kwargs.get("custom_request_body", None)
        self.custom_query_params = kwargs.get("custom_query_params", None)

    def __fetch_headers__(self):
        if self.authorization_type == self.AUTH_TYPE_BASIC:
            auth_header = {"Authorization": f"Basic {self.authorization_key}"}
        elif self.authorization_type == self.AUTH_TYPE_BEARER:
            auth_header = {"Authorization": f"Bearer {self.authorization_key}"}
        elif self.authorization_type == self.AUTH_TYPE_API_KEY:
            auth_header = {"X-API-Key": self.authorization_key}
        else:
            auth_header = {}

        headers = {
            "Content_type": "application/json"
        }

        if self.custom_headers and isinstance(self.custom_headers, dict):
            headers.update(self.custom_headers)

        headers.update(auth_header)
        return headers

    @decorator.timing
    def chunk_data(self, response_text):
        chunks: list[Chunk] = []
        for sentence in sent_tokenize(response_text):
            embeddings = self.create_embeddings([sentence])
            chunks.append(Chunk(chunk_metadata=sentence, chunk_embeddings=embeddings))

        return chunks

    @decorator.timing
    def extract_info(self):
        try:
            if not self.api_url or len(self.api_url.strip()) == 0:
                raise ValueError(f"Invalid API URL : {self.api_url}")

            headers = self.__fetch_headers__()
            if self.api_method == self.REQUESTS_GET:
                response = requests.get(url=self.api_url, params=self.custom_query_params, headers=headers,
                                        timeout=self.TIMEOUT)
            elif self.api_method == self.REQUESTS_POST:
                response = requests.post(url=self.api_url, data=self.custom_request_body, headers=headers,
                                         timeout=self.TIMEOUT)
            else:
                raise ValueError(
                    f"Invalid method for fetching data, currently we support GET/POST. Given : {self.api_method}")

            # we get the response text and try to chunk the data
            response.raise_for_status()
            chunks = self.chunk_data(response.text)
            return chunks

        except ValueError as e:
            self.logger.warning(f"invalid request params : {str(e)}")
            raise e

        except Exception as e:
            self.logger.exception(f"unhandled exception : {str(e)}")
            raise e

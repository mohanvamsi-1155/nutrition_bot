from pydantic import BaseModel, Field, ValidationError, model_validator
from typing import Optional, Any

from typing_extensions import Self
from app.config import SupportedMIMETypes

MIME_TYPES = {element.name: element.value for element in SupportedMIMETypes}


class DataLoaderMethod(BaseModel):
    mime_type: str = Field(...)
    csv_file_path: Optional[str] = Field(default=None, description="path for csv file")
    pdf_path: Optional[str] = Field(default=None, description="path for pdf file")
    http_url: Optional[str] = Field(default=None, description="http url for capturing data from website")
    text_file_path: Optional[str] = Field(default=None, description="text file path to extract data")
    api_url: Optional[str] = Field(default=None, description="API URL for capturing data")
    api_method: Optional[str] = Field(default="GET", description="API request method")
    authorization_key: Optional[str] = Field(default=None, description="Authorization key for api")
    authorization_type: Optional[str] = Field(default=None, description="Authorization type for the api")
    custom_headers: Optional[dict] = Field(default=None, description="Custom headers for the api")
    custom_request_body: Optional[dict] = Field(default=None, description="Custom request body for the api")
    custom_query_params: Optional[dict] = Field(default=None, description="Custom query params for the api")

    @model_validator(mode="after")
    def validate(self, values: Any) -> Self:
        # check for valid mime_type
        if self.mime_type not in MIME_TYPES:
            raise ValidationError(f"Invalid MIME type : {self.mime_type}")

        elif self.mime_type == SupportedMIMETypes.TEXT.value and self.text_file_path is None:
            raise ValidationError(f"Mandatory params missing for MIME type {self.mime_type} : text_file_path")
        elif self.mime_type == SupportedMIMETypes.HTML.value and self.http_url is None:
            raise ValidationError(f"Mandatory params missing for MIME type {self.mime_type} : text_file_path")
        elif self.mime_type == SupportedMIMETypes.API.value and self.api_url is None:
            raise ValidationError(f"Mandatory params missing for MIME type {self.mime_type} : api_url")
        elif self.mime_type == SupportedMIMETypes.PDF.value and self.pdf_path is None:
            raise ValidationError(f"Mandatory params missing for MIME type {self.mime_type} : pdf_path")
        elif self.mime_type in {SupportedMIMETypes.CSV.value,
                                SupportedMIMETypes.EXCEL.value} and self.csv_file_path is None:
            raise ValidationError(f"Mandatory params missing for MIME type {self.mime_type} : csv_file_path")

        return self

class DataSearcherMethod(BaseModel):
    query: str = Field(...)
    metadata: Optional[dict] = Field(default={})

from pydantic import BaseModel, HttpUrl

class URLBase(BaseModel):
    original_url: HttpUrl

class URLInfo(URLBase):
    short_code: str
    class Config:
        orm_mode = True

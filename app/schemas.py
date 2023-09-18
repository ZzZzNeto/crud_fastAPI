from pydantic import BaseModel

class BookBase(BaseModel):
    titulo: str
    author: str

class BookRequest(BookBase):
    ...

class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True
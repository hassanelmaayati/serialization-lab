from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



class BookBase(BaseModel):
    title: str
    author_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = None
    author_id: int | None = None

class BookRead(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author: AuthorRead | None = None   
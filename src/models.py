from sqlalchemy import Column, String, Integer
from pydantic import BaseModel

from .database import Base


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    uses = Column(Integer, default=0)


# Pydantic models for I/O
class LinkBase(BaseModel):
    url: str


class LinkCreate(LinkBase):
    pass


class LinkSchema(LinkBase):
    id: int
    uses: int

    class Config:
        orm_mode = True

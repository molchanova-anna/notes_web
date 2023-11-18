from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteSchema(BaseModel):
   id: int = Field(id, title="id")
   text: str = Field(str, title="Text of note")
   dt_created: datetime = Field(datetime, title="Create date")
   dt_edited: Optional[datetime] = None

   class Config:
      from_attributes = True


class RequestAddNoteSchema(BaseModel):
   text: str = Field(str, title="Text of note")


class ResponseAddNoteSchema(NoteSchema):
   pass


class RequestEditNoteSchema(BaseModel):
   text: str = Field(str, title="Text of note")

# Edit schema is the same like NoteSchema, but using one class in many places can be confusing
class ResponseEditNoteSchema(NoteSchema):
   pass


class ResponseNoteSchema(NoteSchema):
   pass
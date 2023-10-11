from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from routers.notes.schemas import NoteSchema


class BoardSchema(BaseModel):
   id: int = Field(id, title="id")
   name: str = Field(str, title="Name of board")
   dt_created: datetime = Field(datetime, title="Create date")
   dt_edited: Optional[datetime] = None
   notes: Optional[List[NoteSchema]] = []
   class Config:
      from_attributes = True


class RequestAddBoardSchema(BaseModel):
   name: str = Field(str, title="Name of board")

class ResponseAddBoardSchema(BoardSchema):
   pass

class RequestEditBoardSchema(BaseModel):
   name: str = Field(str, title="Name of board")

class ResponseEditBoardSchema(BoardSchema):
   pass

class ResponseBoardSchema(BoardSchema):
   pass

class RequestBoardChangeNoteList(BaseModel):
   board_id: int = Field(int, title="board_id")
   note_id: int = Field(int, title="note_id")

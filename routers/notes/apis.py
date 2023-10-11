from fastapi import APIRouter

from database.db_functions import db_add_note, db_edit_note, db_get_note, db_delete_note
from routers.notes.schemas import (ResponseAddNoteSchema, RequestAddNoteSchema,
                                   RequestEditNoteSchema, ResponseEditNoteSchema, ResponseNoteSchema)

notes_router = APIRouter(
    prefix="/notes",
    tags=["Note"]
)

@notes_router.post('/', response_model=ResponseAddNoteSchema)
async def new_note(request: RequestAddNoteSchema):
    result = await db_add_note(**request.model_dump())
    return ResponseAddNoteSchema.model_validate(result).model_dump()


@notes_router.post('/{note_id:int}', response_model=ResponseEditNoteSchema)
async def edit_note_by_id(note_id: int, request: RequestEditNoteSchema):
    result = await db_edit_note(note_id, **request.model_dump())
    return ResponseEditNoteSchema.model_validate(result).model_dump()

@notes_router.get('/{note_id:int}', response_model=ResponseNoteSchema)
async def get_note_by_id(note_id: int):
    result = await db_get_note(note_id)
    return ResponseNoteSchema.model_validate(result).model_dump()

@notes_router.delete('/{note_id:int}')
async def delete_note_by_id(note_id: int):
    await db_delete_note(note_id)
    return 204, 'Deleted successfully'
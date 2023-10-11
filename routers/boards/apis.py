from fastapi import APIRouter

from database.db_functions import db_add_board, db_edit_board, db_delete_board, db_get_board, db_add_note_to_board, \
    db_delete_note_from_board
from routers.boards.schemas import ResponseAddBoardSchema, RequestAddBoardSchema, ResponseEditBoardSchema, \
    RequestEditBoardSchema, ResponseBoardSchema, RequestBoardChangeNoteList

boards_router = APIRouter(
    prefix="/boards",
    tags=["Board"]
)

@boards_router.post('/', response_model=ResponseAddBoardSchema)
async def new_board(request: RequestAddBoardSchema):
    result = await db_add_board(**request.model_dump())
    return ResponseAddBoardSchema.model_validate(result).model_dump()


@boards_router.post('/{board_id:int}', response_model=ResponseEditBoardSchema)
async def edit_board_by_id(board_id: int, request: RequestEditBoardSchema):
    result = await db_edit_board(board_id, **request.model_dump())
    return ResponseEditBoardSchema.model_validate(result).model_dump()

@boards_router.delete('/{board_id:int}')
async def delete_board_by_id(board_id: int):
    result = await db_delete_board(board_id)
    return 204, 'Deleted successfully'

@boards_router.get('/{board_id:int}', response_model=ResponseBoardSchema)
async def get_board_by_id(board_id: int):
    result = await db_get_board(board_id)
    return ResponseBoardSchema.model_validate(result).model_dump()

@boards_router.post('/note', response_model=ResponseBoardSchema)
async def add_one_note_to_board(request: RequestBoardChangeNoteList):
    result = await db_add_note_to_board(**request.model_dump())
    return ResponseBoardSchema.model_validate(result).model_dump()

@boards_router.delete('/note', response_model=ResponseBoardSchema)
async def delete_one_note_from_board(request: RequestBoardChangeNoteList):
    result = await db_delete_note_from_board(**request.model_dump())
    return ResponseBoardSchema.model_validate(result).model_dump()
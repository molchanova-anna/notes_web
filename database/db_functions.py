import functools

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from database.models import Note, Board
from database.database import async_session


def async_session_with_commit():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            async with async_session() as session: # TODO deco
                res = await func(session, *args, **kwargs)
                await session.commit()
                if res:
                    await session.refresh(res)
                return res
        return wrapped
    return wrapper

@async_session_with_commit()
async def db_add_note(session, **kwargs):
    db_note = Note(**kwargs)
    session.add(db_note)
    return db_note

@async_session_with_commit()
async def db_get_note(session, note_id: int):
    db_note = await session.get(Note, note_id, with_for_update=True)
    db_note.view_count += 1
    session.add(db_note)
    return db_note

@async_session_with_commit()
async def db_edit_note(session, note_id: int, **kwargs):
    db_note = await session.get(Note, note_id)
    for key, value in kwargs.items():
        setattr(db_note, key, value)
    db_note.dt_edited = func.now()
    session.add(db_note)
    return db_note

@async_session_with_commit()
async def db_delete_note(session, note_id: int): # TODO if not exists
    db_note = await session.get(Note, note_id)
    await session.delete(db_note)

@async_session_with_commit()
async def db_add_board(session, **kwargs):
    db_board = Board(**kwargs)
    session.add(db_board)
    return db_board

@async_session_with_commit()
async def db_edit_board(session, board_id: int, **kwargs):
    db_board = await session.get(Board, board_id, populate_existing=True)
    for key, value in kwargs.items():
        setattr(db_board, key, value)
    db_board.dt_edited = func.now()
    session.add(db_board)
    return db_board

@async_session_with_commit()
async def db_delete_board(session, board_id: int):
    db_board = await session.get(Board, board_id)
    await session.delete(db_board)

@async_session_with_commit()
async def db_get_board(session, board_id: int):
    db_board = await session.get(Board, board_id)
    return db_board

async def db_add_note_to_board(board_id: int, note_id: int):
    async with async_session() as session:
        db_board = await session.get(Board, board_id)
        db_note = await session.get(Note, note_id)
        try:
            db_board.notes.append(db_note)
            session.add(db_board)
            await session.commit()
            # if exists - do not raise error
        except IntegrityError as e:
            await session.rollback()
            db_board = await session.get(Board, board_id)
            if str(e.orig.pgcode) != str(23505):
                raise e
    return db_board

@async_session_with_commit()
async def db_delete_note_from_board(session, board_id: int, note_id: int):
    db_board = await session.get(Board, board_id)
    db_note = await session.get(Note, note_id)
    db_board.notes.remove(db_note)
    session.add(db_board)
    return db_board
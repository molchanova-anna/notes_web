from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, UniqueConstraint

from sqlalchemy.orm import declarative_base, relationship, declarative_mixin

Base = declarative_base()


@declarative_mixin
class IdMixin:
    id = Column('id', Integer, primary_key=True, autoincrement=True)


@declarative_mixin
class DtMixin:
    dt_created = Column('dt_created', DateTime, nullable=False, server_default=func.now()) # TODO with tz
    dt_edited = Column('dt_edited', DateTime) # TODO with tz


class Note(IdMixin, Base, DtMixin):
    __tablename__ = "note"
    text = Column('text', String, nullable=False)
    view_count = Column('view_count', Integer, nullable=False, default=0)
    boards = relationship("Board", secondary="board_note", back_populates="notes", lazy='selectin', uselist=True)


class Board(IdMixin, Base, DtMixin):
    __tablename__ = "board"
    name = Column('name', String, nullable=False)
    notes = relationship('Note', secondary='board_note', back_populates='boards', lazy='selectin', uselist=True)


class BoardNote(IdMixin, Base):
    __tablename__ = "board_note"
    board_id = Column(Integer, ForeignKey('board.id', ondelete='CASCADE'), index=True)
    note_id = Column(Integer, ForeignKey('note.id', ondelete='CASCADE'), index=True)
    __table_args__ = (UniqueConstraint('board_id', 'note_id', name='board_note_uidx'),
                      )

from pydantic import BaseModel

# Базовая схема заметки
class NoteBase(BaseModel):
    title: str
    content: str

# Схема для создания заметки
class NoteCreate(NoteBase):
    pass

# Схема для чтения заметки
class NoteRead(NoteBase):
    id: int

    class Config:
        orm_mode = True
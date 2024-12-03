from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Note
from schemas import NoteCreate, NoteRead

# Маршрутизатор
router = APIRouter()


# --- Эндпоинты ---

# Получить все заметки
@router.get("/notes", response_model=list[NoteRead])
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).all()


# Получить заметку по ID
@router.get("/notes/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


# Создать новую заметку
@router.post("/notes", response_model=NoteRead)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    db_note = Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


# Обновить заметку по ID
@router.put("/notes/{note_id}", response_model=NoteRead)
def update_note(note_id: int, updated_note: NoteCreate, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in updated_note.dict().items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note


# Удалить заметку по ID
@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"message": f"Note with ID {note_id} has been deleted"}
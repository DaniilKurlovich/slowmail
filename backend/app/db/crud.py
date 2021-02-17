from fastapi import HTTPException, status
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
import typing as t

from . import models, schemas
from app.core.security import get_password_hash


def get_chat_id(db: Session, from_id: int, to_id: int):
    chat = db.query(models.ConversationDialog).filter(or_(and_(models.ConversationDialog.from_id == from_id,
                                                               models.ConversationDialog.to_id == to_id),
                                                          and_(models.ConversationDialog.from_id == to_id,
                                                               models.ConversationDialog.to_id == from_id))).all()
    if not chat:
        chat = models.ConversationDialog(from_id=from_id, to_id=to_id)
        db.add(chat)
        db.commit()
    else:
        chat = chat[0]

    return chat.chat_id


def mark_as_read_letter(db: Session, id_letter: int):
    letter = db.query(models.MailBox).filter(models.MailBox.id == id_letter).one()
    letter.as_read = True
    db.add(letter)
    db.commit()
    return letter


JOIN_QUERY = lambda db: db.query(models.MailBox, models.ConversationDialog.chat_id).join(
    models.ConversationDialog, or_(models.MailBox.to_addr == models.ConversationDialog.to_id,
                                   models.MailBox.from_addr == models.ConversationDialog.to_id))


# :TODO лучше создать VIEW и не делать select каждый раз
def get_sorted_messages(db: Session, from_addr: int, to_addr: t.Optional[int]):
    if to_addr is not None:
        return JOIN_QUERY(db).filter(or_(and_(models.MailBox.from_addr == from_addr,
                                              models.MailBox.to_addr == to_addr),
                                         and_(models.MailBox.from_addr == to_addr,
                                              models.MailBox.to_addr == from_addr))).order_by(
            models.MailBox.received.desc()).all()
    else:
        return JOIN_QUERY(db).filter(or_(models.MailBox.to_addr == from_addr, models.MailBox.from_addr == from_addr)) \
            .order_by(models.MailBox.received.desc(), models.MailBox.to_addr.desc()).all()


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
        db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def get_coming_letter(db: Session, id_letter: int):
    return db.query(models.ComingMessages).filter(models.ComingMessages.id == id_letter).first()


def get_message_from_id(db: Session, id_letter: int):
    return db.query(models.MailBox).filter(models.MailBox.id == id_letter).first()


def save_letter_for_user(db: Session, letter_content: str, id_user: int, from_addr: int):
    letter = models.MailBox(to_addr=from_addr, from_addr=id_user, message=letter_content)
    db.add(letter)
    db.commit()
    return letter


def store_to_letter_queue(db: Session, letter_content: str, from_addr: int, to_addr: int, delay: int):
    letter = models.ComingMessages(from_addr=from_addr, to_addr=to_addr, message=letter_content, delay=delay)
    db.add(letter)
    db.commit()
    return letter


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
        db: Session, user_id: int, user: schemas.UserEdit
) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

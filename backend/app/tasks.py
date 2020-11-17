import asyncio

from app.db.models import ComingMessages
from app.core import celery_app
from app.db.crud import get_coming_letter, save_letter_for_user
from app.db.session import SessionLocal


# :TODO нужна зависимость от DB

async def store_letter_to_user(to_addr: int, id_letter: int, from_addr: int, delay: int, db=SessionLocal()):
    await asyncio.sleep(delay)
    letter: ComingMessages = get_coming_letter(db, id_letter)
    _id = save_letter_for_user(db, letter.message, from_addr, to_addr)
    return {'from_addr': from_addr, 'to_addr': to_addr, 'status': 'ok', 'letter_id': _id}


# @celery_app.task()
# def store_letter_to_user(to_addr: int, id_letter: int, from_addr: int, db=SessionLocal()):
#     letter: ComingMessages = get_coming_letter(db, id_letter)
#     _id = save_letter_for_user(db, letter.message, from_addr, to_addr)
#     return {'from_addr': from_addr, 'to_addr': to_addr, 'status': 'ok', 'letter_id': _id}

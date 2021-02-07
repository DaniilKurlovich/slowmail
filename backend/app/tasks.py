from __future__ import absolute_import

from app.core.celery_app import celery_app
from app.db.models import ComingMessages
from app.db.crud import get_coming_letter, save_letter_for_user
from app.db.session import SessionLocal
from app.db.schemas import Message


@celery_app.task()
def store_letter_to_user(to_addr: int, id_letter: int, from_addr: int, chat_id: int, db=SessionLocal()):
    letter: ComingMessages = get_coming_letter(db, id_letter)
    _id = save_letter_for_user(db, letter.message, from_addr, to_addr)
    return _id, from_addr, chat_id


@celery_app.task()
def test_task(res):
    print('res: %s' % res)
    return {'test': res}

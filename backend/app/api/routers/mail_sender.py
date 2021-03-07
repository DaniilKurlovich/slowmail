import asyncio
import json
from typing import Any, Optional, List

from fastapi import APIRouter, WebSocket, Depends

from app.core.auth import get_current_user
from app.db.session import get_db
from app.db.crud import (store_to_letter_queue,
                         get_sorted_messages,
                         get_user, mark_as_read_letter,
                         get_chat_id, get_message_from_id,
                         save_letter_for_user)
from app.db.schemas import ConversationDialog, Message, ResponseLetter

from app.db.crud import save_letter_for_user

mail_routers = r = APIRouter()
WS_POOL_CONNECTS = {}


@r.get('/getMessages', response_model=List[Message])
async def list_messages(to_addr: Optional[int] = None, current_user=Depends(get_current_user), db=Depends(get_db)) -> \
List[Message]:
    str_name = lambda x: '%s %s' % (x.first_name, x.last_name)
    from_id = current_user.id
    messages = get_sorted_messages(db, from_id, to_addr)
    from_name = str_name(get_user(db, from_id))
    id2username = {m.to_addr: get_user(db, m.to_addr) for m, _ in messages}
    res = []
    for m, chat_id in messages:
        is_your_message = True if m.from_addr == from_id else False
        res.append(Message(id=m.id, from_name=from_name, to_name=str_name(id2username[m.to_addr]), to_addr_id=m.to_addr,
                           letter=m.message, data=m.received, mark_as_read=m.as_read, is_your_message=is_your_message,
                           chat_id=chat_id))
    return res


@r.post('/markAsRead')
async def mark_letter_as_read(id_letter: int, db=Depends(get_db)) -> dict:
    try:
        letter = mark_as_read_letter(db, id_letter)
        await notify_about_marker_read_letter(letter.to_addr, id_letter)
    except Exception as exc:
        return {'status': 'error', 'reason': str(exc)}
    return {'status': 'ok'}


async def notify_about_marker_read_letter(to_addr: int, id_letter: int):
    ws_conn = WS_POOL_CONNECTS.get(to_addr, None)
    if ws_conn is None:
        return
    await ws_conn.send_text(json.dumps({'type': 'mark_read', 'data': {'id': id_letter}}))


async def notify_about_new_msg(letter, from_id, to_id, content, chat_id, db):
    ws_conn = WS_POOL_CONNECTS.get(to_id, None)
    if ws_conn is None:
        return

    from_user = get_user(db, from_id)
    to_user = get_user(db, to_id)
    msg = Message(id=letter.id, from_name=f'{from_user.first_name} {from_user.last_name}', from_id=from_id,
                  to_name=f'{to_user.first_name} {to_user.last_name}',
                  letter=content, data=letter.received,
                  mark_as_read=letter.as_read, is_your_message=False, chat_id=chat_id, to_addr_id=to_id)
    await ws_conn.send_text(json.dumps({'type': 'message', 'data': msg.json()}))


@r.post('/sendMessage', response_model=ResponseLetter)
async def send_mail(to_addr: int, content: str, delay: int = 5,
                    current_user=Depends(get_current_user), db=Depends(get_db)) -> Any:
    # :TODO обработка ошибок
    delay = int(delay)
    id_from = current_user.id
    if id_from == to_addr:
        raise Exception('You cant send letter to yourself')
    letter = save_letter_for_user(db, content, id_from, to_addr)
    chat_id = get_chat_id(db, id_from, to_addr)
    await notify_about_new_msg(letter, id_from, to_addr, content, chat_id, db)
    return {'status': True, 'delay': delay, 'chat_id': chat_id}


@r.websocket('/notification')
async def notification_message(websocket: WebSocket):
    await websocket.accept()
    to_id = None
    try:
        while True:
            data = await websocket.receive_json()
            to_id = data['from_id']
            WS_POOL_CONNECTS[to_id] = websocket
    finally:
        WS_POOL_CONNECTS.pop(to_id)

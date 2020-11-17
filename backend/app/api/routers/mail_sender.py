import asyncio
from typing import Union, Any, Dict, Optional, List
from starlette.websockets import WebSocketDisconnect
from fastapi import APIRouter, WebSocket, Depends

from app.core.auth import get_current_user
from app.db.session import get_db
from app.tasks import store_letter_to_user
from app.db.crud import store_to_letter_queue, get_sorted_messages, get_user, mark_as_read_letter, get_chat_id

from app.db.schemas import ConversationDialog, Message, ResponseLetter


mail_routers = r = APIRouter()
TASKS = {}


@r.get('/getMessages', response_model=List[Message])
async def list_messages(from_id: int, to_addr: Optional[int], db=Depends(get_db)) -> List[Message]:
    str_name = lambda x: '%s %s' % (x.first_name, x.last_name)

    messages = get_sorted_messages(db, from_id, to_addr)
    from_name = str_name(get_user(db, from_id))
    id2username = {m.to_addr: get_user(db, m.to_addr) for m in messages}
    res = []
    for m in messages:
        res.append(Message(id=m.id, from_name=from_name, to_name=str_name(id2username[m.to_addr]),
                           letter=m.message, data=m.received, mark_as_read=m.as_read))
    return res


@r.get('/markAsRead')
async def mark_letter_as_read(id_letter: int, db=Depends(get_db)) -> dict:
    try:
        mark_as_read_letter(db, id_letter)
    except Exception as exc:
        return {'status': 'error', 'reason': str(exc)}
    return {'status': 'ok'}


@r.post('/sendMessage', response_model=ResponseLetter)
async def send_mail(to_addr: int, content: str, delay: int = 5,
                    current_user=Depends(get_current_user), db=Depends(get_db)) -> Any:
    # :TODO обработка ошибок
    delay = int(delay)
    id_from = current_user.id
    id_letter = store_to_letter_queue(db, content, id_from, to_addr, delay)
    chat_id = get_chat_id(db, id_from, to_addr)
    loop = asyncio.get_event_loop()
    loop.create_task(store_letter_to_user(to_addr, id_letter, id_from, delay))
    return {'status': True, 'delay': delay, 'chat_id': chat_id}


@r.websocket('/notification')
async def notification_message(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            chat_id = data['chat_id']
            task = TASKS.get(chat_id, None)
            if task is None:
                break
            result = task.get()
            await websocket.send_json(result)
    except WebSocketDisconnect:
        print('Disconnect')
    await websocket.close(code=10000)

import asyncio
from typing import Any, Optional, List

# from fastapi_jwt_auth import AuthJWT
from celery.result import AsyncResult
from starlette import status
from starlette.websockets import WebSocketDisconnect
from fastapi import APIRouter, WebSocket, Depends, Query, Cookie
from fastapi_jwt_auth.exceptions import AuthJWTException

from app.core.auth import get_current_user
from app.db.session import get_db
from app.db.crud import store_to_letter_queue, get_sorted_messages, get_user, mark_as_read_letter, get_chat_id, get_message_from_id
from app.db.schemas import ConversationDialog, Message, ResponseLetter
from app.utils import NotificationStorage
from app.tasks import store_letter_to_user

mail_routers = r = APIRouter()
TASKS = NotificationStorage()


@r.get('/getMessages', response_model=List[Message])
async def list_messages(to_addr: Optional[int] = None, current_user=Depends(get_current_user), db=Depends(get_db)) -> List[Message]:
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
    global TASKS
    # :TODO обработка ошибок
    print('was here')
    delay = int(delay)
    id_from = current_user.id
    if id_from == to_addr:
        raise Exception('You cant send letter to yourself')
    id_letter = store_to_letter_queue(db, content, id_from, to_addr, delay)
    # store_to_letter_queue(db, content, , to_addr, delay)

    chat_id = get_chat_id(db, id_from, to_addr)
    task = store_letter_to_user.apply_async((to_addr, id_letter, id_from, chat_id, ), countdown=delay)
    TASKS.put(to_addr, task)
    return {'status': True, 'delay': delay, 'chat_id': chat_id}


# :TODO ГОВНО НА КОСТЫЛЯХ!!!!!!!!!!!!!!!!!
@r.websocket('/notification')
async def notification_message(websocket: WebSocket, db=Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            to_id = data['from_id']
            user_name = get_user(db, to_id)
            while True:
                tasks = TASKS.get_tasks(int(to_id))
                for t in tasks:
                    task_id = t.task_id
                    res = AsyncResult(task_id)
                    if res.ready():
                        letter_id, from_id, chat_id = t.get()
                        m = get_message_from_id(db, letter_id)
                        from_user = get_user(db, from_id)
                        msg = Message(id=letter_id, from_name=f'{from_user.first_name} {from_user.last_name}',
                                      to_name=f'{user_name.first_name} {user_name.last_name}',
                                      letter=m.message, data=m.received,
                                      mark_as_read=m.as_read, is_your_message=False, chat_id=chat_id, to_addr_id=to_id)
                        await websocket.send_text(msg.json())
                await asyncio.sleep(60)

            # task = TASKS.get(chat_id, {}).get(to_addr, None)
            # if task is None:
            #     break
            # result = task.get()

            # await websocket.send_json(result)
    except WebSocketDisconnect:
        print('Disconnect')
    await websocket.close(code=10000)


# async def get_cookie_or_token(
#     websocket: WebSocket,
#     session: Optional[str] = Cookie(None),
#     token: Optional[str] = Query(None),
# ):
#     if session is None and token is None:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#     return session or token


# @r.websocket('/ws')
# async def websocket(websocket: WebSocket, csrf_token: str = Query(...), Authorize: AuthJWT = Depends()):
#     await websocket.accept()
#     try:
#         Authorize.jwt_required("websocket", websocket=websocket, csrf_token=csrf_token)
#         # Authorize.jwt_optional("websocket",websocket=websocket,csrf_token=csrf_token)
#         # Authorize.jwt_refresh_token_required("websocket",websocket=websocket,csrf_token=csrf_token)
#         # Authorize.fresh_jwt_required("websocket",websocket=websocket,csrf_token=csrf_token)
#         await websocket.send_text("Successfully Login!")
#         decoded_token = Authorize.get_raw_jwt()
#         await websocket.send_text(f"Here your decoded token: {decoded_token}")
#     except AuthJWTException as err:
#         await websocket.send_text(err.message)
#         await websocket.close()

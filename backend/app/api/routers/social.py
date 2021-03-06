from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from app.db.schemas import Friend

from app.core.auth import get_current_user
from app.mongo_controller.crud import (recommend_friends_for_user_id, handshake_friends, get_user_by_id,
                                       add_friend, accept_handshake, add_category)


social = r = APIRouter()


@r.get('/categories')
async def get_categories():
    return ['movie', 'science', 'music', 'Putin', 'science', 'Jesus', 'parkour', 'LGBT']


@r.post('/setCategories')
async def set_categories(list_categories: List[str] = Query(None), user=Depends(get_current_user)):
    add_category(user.id, list_categories[0].split(','))
    return {'status': 'ok'}


@r.get('/myCategories')
async def my_categories(user=Depends(get_current_user)):
    user = get_user_by_id(user.id)
    return {'categories': user.get('category', [])}


@r.get('/possibleFriends', response_model=List[Friend])
async def get_recommendation(limit=30, user=Depends(get_current_user)):
    res = recommend_friends_for_user_id(user.id, limit)
    return list(res)


@r.get('/listHandshake')
async def get_list_handshakes(user=Depends(get_current_user)):
    res = get_user_by_id(user.id)
    return {'in': res['friendship_in'], 'out': res['friendship_out']}


@r.post('/sendHandshake')
async def request_to_friend(to_user_id: int, user=Depends(get_current_user)):
    request_user = get_user_by_id(to_user_id)
    if request_user is None:
        raise HTTPException(404, 'to_user_id not found')
    handshake_friends(user.id, request_user)
    return {'status': 'ok'}


@r.post('/acceptHandshake')
async def accept_to_friend(user_id: int, user=Depends(get_current_user)):
    accept_handshake(user.id, user_id)
    return {'status': 'ok'}


@r.get('/myFriends')
async def get_friends(user=Depends(get_current_user)):
    user_db = get_user_by_id(user.id)
    if user_db is None:
        raise HTTPException(500, 'user with id %s dont found' % user.id)
    return {'friends': user_db['friends']}
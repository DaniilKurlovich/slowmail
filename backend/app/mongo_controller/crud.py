import typing as ty

from app.db.schemas import UserFriend, Friend
from .controller import insert_document, find_similar, update_document_push, find_document, update_document_pull, \
    update_document_set
from ..errors import HandshakeSendedAlready


def get_user_by_id(user_id: int):
    return find_document({'id': user_id})


def reg_user(user_id: int, full_name: str, categories=None):
    """
    Функция должна сохранять юзеров и друзей в храниище
    """
    if categories is None:
        categories = []
    user = UserFriend(id=user_id, full_name=full_name, friends=[], category=categories, friendship_out=[],
                      friendship_in=[])
    insert_document(user.dict())


def accept_handshake(from_user_id: int, to_user_id: int):
    """
    from_user_id - id того кто принимает рукопажатие
    to_user_id - id того кто его отсылает
    """
    # Нужно добавить в списки friends
    from_user = get_user_by_id(from_user_id)
    to_user = get_user_by_id(to_user_id)
    for key in ['_id', 'friends', 'friendship_in', 'friendship_out']:
        from_user.pop(key, None)
        to_user.pop(key, None)
    add_friend(from_user_id, to_user)
    add_friend(to_user_id, from_user)
    # очистить запрос
    update_document_pull({'id': from_user_id}, {'friendship_in': {'id': to_user_id}})
    update_document_pull({'id': to_user_id}, {'friendship_out': {'id': from_user_id}})


def add_friend(user_id: int, friend: Friend):
    """
    Функция должна обновлять список текущей друзей у user_id
    """
    update_document_push({'id': user_id}, {'friends': friend})


def handshake_friends(from_id: int, possible_friend: dict):
    from_user = get_user_by_id(from_id)
    for friend in from_user['friendship_out']:
        if friend['id'] == possible_friend['id']:
            raise HandshakeSendedAlready()
    for key in ['_id', 'friends', 'friendship_in', 'friendship_out']:
        from_user.pop(key, None)
        possible_friend.pop(key, None)
    update_document_push({'id': from_id}, {'friendship_out': possible_friend})
    update_document_push({'id': possible_friend['id']}, {'friendship_in': from_user})


def recommend_friends_by_tags(user_id: int, categories: ty.List[str], limit: int) -> ty.Iterator[Friend]:
    cursor = find_similar(user_id, categories, limit)
    for r in cursor:
        yield Friend(id=r['id'], full_name=r['full_name'], category=r['category'])


def recommend_friends_for_user_id(user_id: int, limit: int) -> ty.Iterator[Friend]:
    user = find_document({'id': user_id})
    if user is None:
        yield
    yield from recommend_friends_by_tags(user_id, user['category'], limit=limit)


def add_category(user_id: int, categories: ty.List[str]):
    """
    Функция должна обновлять список категорий
    """
    update_document_set({'id': user_id}, {'category': categories})

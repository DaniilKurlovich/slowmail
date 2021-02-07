from . import COLLECTION


def find_document(elements, multiple=False):
    if multiple:
        results = COLLECTION.find(elements)
        return [r for r in results]
    else:
        return COLLECTION.find_one(elements)


def find_similar(id_, elements, _limit):
    return COLLECTION.find({'$and': [{'id': {'$ne': id_}}, {'category': {'$in': elements}}]}).limit(_limit)


def insert_document(data):
    return COLLECTION.insert_one(data).inserted_id


def update_document_push(query_elements, new_value):
    COLLECTION.update_one(query_elements, {'$push': new_value})


def update_document_pull(query_elements, pull_elements):
    COLLECTION.update_one(query_elements, {'$pull': pull_elements})


def update_document_set(query_elements, pull_elements):
    COLLECTION.update_one(query_elements, {'$set': pull_elements})

import pymongo as pym


def find_document(collection, elements, multiple=False):
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def insert_document(collection, data):
    return collection.insert_one(data).inserted_id


def update_document(collection, query_elements, new_values):
    for v in new_values:
        collection.update_one(query_elements, {'$push': v})
    # collection.update_one(query_elements, {'$set': new_values})


client = pym.MongoClient('mongodb://slowmail:slowmail@0.0.0.0', 27017)

# Connect to our database
db = client['mongo_slowmail']

# # Fetch our series collection
# # series_collection.ensureIndex({"ingredients": "category"})
# print(series_collection)
#
# new_show = {
#     "name": "FRIENDS3",
#     "year": 1994,
#     'category': ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# }
# # print(insert_document(series_collection, new_show))
#
# print(update_document(series_collection, {'name': 'FRIENDS4'}, {'category': ['tes4', 'tes5']}))
#
# print(find_document(series_collection, {'name': 'FRIENDS4'}))
series_collection = db['series']

test_man = {
    'id': 1,
    'full_name': 'test_name',
    'friends': [],
    'category': ['a', 'b', 'c', 'd', 'e', 'f', 'g'],
    'request_from_users_id': [],
    'request_to_users_id': [
        {'id': 2, 'full_name': 'pull_test2', 'categories': ['a', 'b', 'z']},
        {'id': 3, 'full_name': 'pull_test3', 'categories': ['f']}
    ]
}

# print(insert_document(series_collection, test_man))
print(find_document(series_collection, {'full_name': 'test_name'}))
series_collection.update_one({'id': 1}, {'$pull': {'request_to_users_id': {'id': 2}}})
print(find_document(series_collection, {'full_name': 'test_name'}))

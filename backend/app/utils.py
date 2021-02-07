from collections import defaultdict


class NotificationStorage:
    def __init__(self):
        self._storage_notification = defaultdict(list)  # user_id: list[IncomingMessage]

    def get_tasks(self, user):
        return self._storage_notification.get(user, [])

    def put(self, user, task):
        self._storage_notification[user].append(task)

    def restore(self, user, index):
        self._storage_notification[user].pop(index)

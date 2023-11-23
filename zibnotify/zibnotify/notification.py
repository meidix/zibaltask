from pymongo import MongoClient

class NotificationManager:
    def __init__(self, backend_uri, db_name, collection):
        self.mediums = {}
        self.backend = backend_uri
        self.db_name = db_name

        self._get_db(collection)

    def _get_db(self, collection):
        if self.backend:
            client = MongoClient(self.backend)
            self.db = client[self.db_name].get_collection(collection)

    def register(self, medium_name, send_handler):
        self.mediums[medium_name] = send_handler

    def notify(self, medium_name, receiver, messege):
        if medium_name not in self.mediums:
            raise Exception("No such medium registered")

        handler = self.mediums[medium_name]
        return handler.delay((receiver, messege)).task_id

    def follow(self, task_id):
        task = self.db.find_one({ '_id': task_id})
        return task
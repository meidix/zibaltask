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

    def notify(self, medium_name, notification):
        if medium_name not in self.mediums:
            raise Exception("No such medium registered")

        handler = self.mediums[medium_name]
        return handler.delay(notification).task_id

    def follow(self, task_id):
        task = self.db.find_one({ '_id': task_id})
        return task


class BaseNotification:

    def __init__(self, receiver, messege):
        self.receiver = receiver
        self.messege = messege

    def to_dict(self):
        return {
            'receiver': self.receiver,
            'messege': self.messege
        }

    def __repr__(self) -> str:
        return f'deliver {self.messege} to {self.receiver}'

    @classmethod
    def from_dict(cls, dict_data):
        return cls(**dict_data)


class EmailNotification(BaseNotification):

    def __init__(self, receiver, subject, messege):
        super().__init__(receiver, messege)
        self.subject = subject

    def to_dict(self):
        res = super().to_dict()
        res.update({
            'subject': self.subject
        })
        return res

class PushNotification(BaseNotification):
    pass

class SMSNotification(BaseNotification):
    pass
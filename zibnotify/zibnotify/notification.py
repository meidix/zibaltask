
class NotificationManager:
    def __init__(self):
        self.mediums = {}

    def register(self, medium_name, send_handler):
        self.mediums[medium_name] = send_handler

    def notify(self, medium_name, receiver, messege):
        if medium_name not in self.mediums:
            raise Exception("No such medium registered")

        handler = self.mediums[medium_name]
        handler.delay((receiver, messege))

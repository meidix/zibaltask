from django.http import JsonResponse, HttpResponse, HttpRequest
from bson.json_util import dumps
from django.db.models import TextChoices

class Request:
    def __init__(self, request: HttpRequest, validators=[]):
        self.request = request
        self._initial_params = eval(request.body.decode("UTF-8"))
        self.validators = validators
        self.validate()

    def validate(self):
        for validator in self.validators:
            validator(self._initial_params)
        self.params = self._initial_params

    def get_param(self, param_name, default=None):
        return self.params.get(param_name, default)



class Response:
    def __init__(self, data=None, status=200):
        self.data = data
        self.status = status

    def to_json_response(self):
        return HttpResponse(dumps(self.data), content_type="application/json", status=self.status)
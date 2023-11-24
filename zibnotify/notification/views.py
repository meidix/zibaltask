from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from zibnotify import manager
from .utils import Request, Response

@method_decorator(csrf_exempt, name='dispatch')
class NotificationService(View):

    def get(self, request, *args, **kwargs):
        try:
            req = Request(request)
            res = manager.follow(req.params['taskId'])
            response = Response(res, 200)
            return response.to_json_response()
        except:
            response = Response({'error': "An error occured"}, 400)
            return response.to_json_response()

    def post(self, request, *args, **kwargs):
        # try:
            req = Request(request)
            res = manager.notify(req.params['medium'], req.params['payload'])
            response = Response({'taskId': res}, 200)
            return response.to_json_response()
        # except:
        #     response = Response({'error': "An error occured"}, 400)
        #     return response.to_json_response()

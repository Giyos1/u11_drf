from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from config.celery import app
from .tasks import add, send_gmail


class TestView(APIView):
    # def get(self, request, *args, **kwargs):
    #     a = add.delay(1, 2)  # background ga yuborish!
    #     return Response({"task_id": a.id})
    #
    # def post(self, request, *args, **kwargs):
    #     task_id = request.data['task_id']
    #     result = AsyncResult(task_id, app=app)
    #
    #     if result.ready():  # Tayormi?
    #         return Response({"result": result.result})
    #     return Response({"status": "processing..."})

    def post(self, request, *args, **kwargs):
        mail = request.data.get("mail")
        message = request.data.get("message")

        send_gmail.delay(mail=mail, message=message)
        return Response({"status": "success"})

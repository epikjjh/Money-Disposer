from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from apiServer.models import Ticket, UserList
import json
import random
import string
from datetime import datetime


class DisposeView(APIView):
    renderer_classes = (JSONRenderer, )

    def generate_token(self):
        random.seed(datetime.now())
        return "".join([random.choice(string.ascii_letters) for _ in range(3)])

    # Spread api
    def post(self, request):
        user_id, room_id = request.META.get(
            'HTTP_X_USER_ID'), request.META.get('HTTP_X_ROOM_ID')
        if not user_id or not room_id:
            return Response({"Error: missing required header"}, status=412)
        request = json.loads(request.body)
        num, amount = request['num'], request['amount']
        if not num or not amount:
            return Response({"Error: missing required data"}, status=412)

        token = self.generate_token()
        ticket = Ticket(token=token, room_id=room_id,
                        owner=user_id, amount=amount, num=num)
        ticket.save()
        return Response({"token": token})

    # Receive api
    def put(self, request):
        user_id, room_id = request.META.get(
            'HTTP_X_USER_ID'), request.META.get('HTTP_X_ROOM_ID')
        if not user_id or not room_id:
            return Response({"Error: missing required header"}, status=412)
        return Response("PUT")

    # Retrieve api
    def get(self, request):
        user_id, room_id = request.META.get(
            'HTTP_X_USER_ID'), request.META.get('HTTP_X_ROOM_ID')
        if not user_id or not room_id:
            return Response({"Error: missing required header"}, status=412)
        return Response("GET")

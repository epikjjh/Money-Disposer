from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from apiServer.models import Ticket, UserList
import json
import random
import string
from datetime import datetime, timedelta
from pytz import timezone
from functools import reduce


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

        request = json.loads(request.body)
        token = request['token']
        if not token:
            return Response({"Error: missing required data"}, status=412)

        try:
            ticket = Ticket.objects.get(token=token)
        except Ticket.DoesNotExist:
            return Response({"Error: unauthorized token"}, status=401)

        if ticket.owner == user_id:
            return Response({"Error: unauthorized user"}, status=401)

        if datetime.now(timezone('Asia/Seoul')) - ticket.date > timedelta(minutes=10):
            return Response({"Error: unauthorized time"}, status=401)

        receivers = UserList.objects.filter(ticket=ticket)
        receivers_num = receivers.count()
        total_num = ticket.num
        is_receive = receivers.filter(user=user_id).count()

        if is_receive:
            return Response({"Error: unauthorized user. Already received"}, status=401)

        if receivers_num >= total_num:
            return Response({"Error: unauthorized user. No remaining amount"}, status=401)

        ret_amount = ticket.amount // total_num if receivers_num != total_num - 1 \
            else ticket.amount // total_num + ticket.amount % total_num

        new_list = UserList(ticket=ticket, user=user_id)
        new_list.save()

        return Response({"amount": ret_amount})

    # Retrieve api
    def get(self, request):
        user_id, room_id = request.META.get(
            'HTTP_X_USER_ID'), request.META.get('HTTP_X_ROOM_ID')
        if not user_id or not room_id:
            return Response({"Error: missing required header"}, status=412)

        request = json.loads(request.body)
        token = request['token']
        if not token:
            return Response({"Error: missing required data"}, status=412)

        try:
            ticket = Ticket.objects.get(token=token)
        except Ticket.DoesNotExist:
            return Response({"Error: unauthorized token"}, status=401)

        if ticket.owner != user_id:
            return Response({"Error: unauthorized user"}, status=401)

        if datetime.now(timezone('Asia/Seoul')) - ticket.date > timedelta(days=7):
            return Response({"Error: unauthorized time"}, status=401)

        receivers = UserList.objects.filter(ticket=ticket)
        receivers_num = receivers.count()
        total_num = ticket.num
        ret_info = [[ticket.amount // total_num if i+1 != total_num - 1
                     else ticket.amount // total_num + ticket.amount % total_num, recevier.user] for i, recevier in enumerate(receivers)]
        ret_amount = reduce(lambda x, y: x + y[0], ret_info, 0)

        return Response({"date": ticket.date, "amount": ticket.amount, "received amount": ret_amount, "info": ret_info})

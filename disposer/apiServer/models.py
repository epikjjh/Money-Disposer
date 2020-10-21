from django.db import models


class Ticket(models.Model):
    token = models.CharField(max_length=3)
    room_id = models.TextField()
    owner = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(default=0)
    num = models.IntegerField(default=0)


class UserList(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.TextField()

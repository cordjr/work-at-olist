from django.db import models


class Subscriber(models.Model):
    phone_number = models.IntegerField(primary_key=True)


class CallRecord(models.Model):
    destination_number = models.IntegerField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)

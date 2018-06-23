from django.db import models


class CallRecord(models.Model):
    source_number = models.IntegerField(db_index=True)
    destination_number = models.IntegerField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

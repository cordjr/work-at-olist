from django.core.exceptions import ValidationError
from django.db import models


class CallRecord(models.Model):
    call_id = models.IntegerField(primary_key=True)
    source_number = models.IntegerField(db_index=True, null=True)
    destination_number = models.IntegerField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    minute_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError({'start_time': "Start time must not be after end_time",
                                   'end_time': 'End time must not be before start time'})

    @property
    def total_price(self):
        return self.total_minutes * self.minute_price

    @property
    def total_minutes(self):
        delta = (self.end_time - self.start_time)
        return delta.seconds // 60


class PricePolice(models.Model):
    start = models.DateField(default=None)
    end = models.DateField(default=None)

    def clean(self):
        if self.start >= self.end:
            raise ValidationError({'start': "Start time must not be after end_time",
                                   'end': 'End time must not be before start time'})


class PriceRule(models.Model):
    TYPES = (('S', 'STANDARD'),
             ('R', 'REDUCED'))
    policy = models.ForeignKey(PricePolice, on_delete=models.CASCADE)
    start_time = models.TimeField
    end_time = models.TimeField
    type = models.CharField(max_length=1, choices=TYPES)
    value = models.DecimalField(max_digits=20, decimal_places=2)

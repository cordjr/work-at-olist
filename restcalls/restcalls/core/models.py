from django.db import models


class CallRecord(models.Model):
    source_number = models.IntegerField(db_index=True)
    destination_number = models.IntegerField()
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)


class PricePolice(models.Model):
    start = models.DateField
    end = models.DateField


class PriceRule(models.Model):
    TYPES = (('S', 'STANDARD'),
             ('R', 'REDUCED'))
    policy = models.ForeignKey(PricePolice, on_delete=models.CASCADE)
    start_time = models.TimeField
    end_time = models.TimeField
    type = models.CharField(max_length=1, choices=TYPES)
    value = models.DecimalField(max_digits=20, decimal_places=2)

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_DOWN, Context

from django.core.exceptions import ValidationError
from django.db import models

DEFAULT_CONTEXT = Context(rounding=ROUND_HALF_DOWN, prec=2)


class CallRecord(models.Model):
    call_id = models.IntegerField(primary_key=True)
    source_number = models.IntegerField(db_index=True, null=True)
    destination_number = models.IntegerField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    call_price = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError({'start_time': "Start time must not be after end_time",
                                   'end_time': 'End time must not be before start time'})

    @property
    def total_minutes(self):
        delta = (self.end_time - self.start_time)
        return delta.seconds // 60


class PricePolicy(models.Model):
    start = models.DateField(default=None)
    end = models.DateField(default=None)
    standing_rate = models.DecimalField(max_digits=20, decimal_places=2)

    def calculate_price(self, call_start, call_end):
        return self.standing_rate + sum([p.calculate_price(call_start, call_end) for p in self.pricerule_set.all()])


class PriceRule(models.Model):
    TYPES = (('S', 'STANDARD'),
             ('R', 'REDUCED'))
    policy = models.ForeignKey(PricePolicy, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=1, choices=TYPES)
    value = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.value:
            if self.value is not Decimal:
                self.value = Decimal(self.value, context=DEFAULT_CONTEXT)
            self.value = round(self.value, 2)

        self.full_clean()
        super(PriceRule, self).save(force_insert=False, force_update=False, using=None,
                                    update_fields=None)

    def calculate_price(self, call_start, call_end):
        if call_end < call_start:
            raise ValidationError("call end can't be before  call start")
        ctx = DEFAULT_CONTEXT

        begin_range = datetime.combine(call_start.date(), self.start_time)
        end_range = datetime.combine(call_end.date(), self.end_time)
        if end_range < begin_range:
            end_range += timedelta(days=1)

        if begin_range <= call_start <= end_range and call_end <= end_range:
            delta = call_end - call_start
        elif begin_range <= call_start <= end_range and not (call_end <= end_range):
            delta = end_range - call_start
        elif call_start < begin_range <= call_end <= end_range:
            delta = call_end - begin_range
        else:
            return 0
        value = round(self.value, 2)
        minutes = Decimal(delta.seconds // 60, context=ctx)

        return value * minutes

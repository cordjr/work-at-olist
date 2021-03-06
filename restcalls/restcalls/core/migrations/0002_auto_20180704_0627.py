# Generated by Django 2.0 on 2018-07-04 06:27

from django.db import migrations
from restcalls.core.models import PricePolicy, PriceRule, CallRecord
from datetime import datetime
from decimal import  Decimal

def create_initial_price_policy(apps, schema_editor):
    # PricePolicy = apps.get_model('core', 'PricePolicy')
    # PriceRule = apps.get_model('core', 'PriceRule')

    price_policy = PricePolicy.objects.create(
        start=datetime.strptime('2018-01-01', '%Y-%m-%d'),
        end=datetime.strptime('2018-2-01', '%Y-%m-%d'),
        standing_rate=0.25
    )
    price_rule = PriceRule.objects.create(
        policy=price_policy,
        start_time=datetime.strptime('06:01', '%H:%M'),
        end_time=datetime.strptime('22:00', '%H:%M'),
        value=0.15,
        type='S'
    )
    price_rule = PriceRule.objects.create(
        policy=price_policy,
        start_time= datetime.strptime('06:00', '%H:%M'),
        end_time=datetime.strptime('22:00', '%H:%M'),
        type='R',
        value=0.00
    )
def create_initial_call_records(apps, schema_editor):
    call_list = [
        CallRecord(call_id=70, start_time=datetime.strptime("2016-02-29T12:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
                   end_time=datetime.strptime("2016-02-29T14:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
                   source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
        CallRecord(call_id=71, start_time=datetime.strptime("2017-12-12T15:07:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                   end_time=datetime.strptime("2017-12-12T15:14:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                   source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
        CallRecord(call_id=72, start_time=datetime.strptime("2017-12-12T22:47:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                   end_time=datetime.strptime("2017-12-12T22:50:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                   source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
        CallRecord(call_id=73, start_time=datetime.strptime("2017-12-12T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                   end_time=datetime.strptime("2017-12-12T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                   source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
        CallRecord(call_id=74, start_time=datetime.strptime("2017-12-12T04:57:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                   end_time=datetime.strptime("2017-12-12T06:10:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                   source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
        CallRecord(call_id=75, start_time=datetime.strptime("2017-12-12T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                   end_time=datetime.strptime("2017-12-13T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                   source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
        CallRecord(call_id=76, start_time=datetime.strptime("2017-12-12T15:07:58Z", "%Y-%m-%dT%H:%M:%SZ"),
                   end_time=datetime.strptime("2017-12-12T15:12:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                   source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23')),
        CallRecord(call_id=77, start_time=datetime.strptime("2018-02-28T21:57:13Z", "%Y-%m-%dT%H:%M:%SZ"),
                   end_time=datetime.strptime("2018-03-01T22:10:56Z", "%Y-%m-%dT%H:%M:%SZ"),
                   source_number=99988526423, destination_number=99988526423, call_price=Decimal('0.23'))]
    CallRecord.objects.bulk_create(call_list)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_price_policy),
        migrations.RunPython(create_initial_call_records),
    ]

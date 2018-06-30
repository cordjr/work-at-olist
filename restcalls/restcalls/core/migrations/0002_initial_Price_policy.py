# Generated by Django 2.0 on 2018-06-29 11:01

from datetime import datetime

from django.db import migrations


from restcalls.core.models import PricePolicy, PriceRule


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


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_price_policy),
    ]

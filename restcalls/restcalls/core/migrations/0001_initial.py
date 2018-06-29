# Generated by Django 2.0 on 2018-06-29 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallRecord',
            fields=[
                ('call_id', models.IntegerField(primary_key=True, serialize=False)),
                ('source_number', models.IntegerField(db_index=True, null=True)),
                ('destination_number', models.IntegerField()),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('minute_price', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PricePolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(default=None)),
                ('end', models.DateField(default=None)),
                ('standing_rate', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='PriceRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('S', 'STANDARD'), ('R', 'REDUCED')], max_length=1)),
                ('value', models.DecimalField(decimal_places=2, max_digits=20)),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.PricePolicy')),
            ],
        ),
    ]

# Generated by Django 5.0.4 on 2024-09-17 13:17

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0002_parkingprice_alter_parking_parked_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='parked_time',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parking',
            name='unparked_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='parking',
            name='value',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]

# Generated by Django 2.1.3 on 2018-11-24 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QnSapp', '0002_auto_20181121_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveypost',
            name='useTemplate',
            field=models.BooleanField(default='True'),
        ),
    ]

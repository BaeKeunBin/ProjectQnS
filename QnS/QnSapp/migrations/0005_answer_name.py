# Generated by Django 2.1.3 on 2018-11-25 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QnSapp', '0004_auto_20181125_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='name',
            field=models.CharField(default='default', max_length=100),
        ),
    ]

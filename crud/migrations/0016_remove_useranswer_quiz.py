# Generated by Django 3.0.4 on 2020-05-22 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0015_auto_20200522_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='quiz',
        ),
    ]

# Generated by Django 3.0.5 on 2020-06-17 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0020_auto_20200617_1434'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='useranswer',
            unique_together=set(),
        ),
    ]

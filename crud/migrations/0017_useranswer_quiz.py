# Generated by Django 3.0.4 on 2020-05-22 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0016_remove_useranswer_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='quiz',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='crud.Quiz'),
        ),
    ]

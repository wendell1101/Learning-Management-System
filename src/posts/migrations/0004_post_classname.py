# Generated by Django 3.0.4 on 2020-05-24 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0017_useranswer_quiz'),
        ('posts', '0003_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='classname',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='crud.ClassName'),
        ),
    ]

# Generated by Django 3.0.4 on 2020-05-24 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_classname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='attachment',
            field=models.FileField(blank=True, default='', upload_to='file_attachments/'),
        ),
    ]

# Generated by Django 4.2 on 2023-05-05 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

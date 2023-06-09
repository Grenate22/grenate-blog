# Generated by Django 4.2 on 2023-05-05 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_comment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='email',
            field=models.EmailField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.CharField(default='null', max_length=50),
            preserve_default=False,
        ),
    ]

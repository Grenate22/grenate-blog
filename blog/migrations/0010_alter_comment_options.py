# Generated by Django 4.2 on 2023-05-05 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_remove_post_views_popularpost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['timestamp']},
        ),
    ]
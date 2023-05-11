# Generated by Django 4.2 on 2023-05-06 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_comment_email_comment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published')], default='DF', max_length=2),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-date'], name='blog_post_date_55752c_idx'),
        ),
    ]
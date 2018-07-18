# Generated by Django 2.0.6 on 2018-07-10 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180710_2101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='userinfo',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='nickname',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='blog',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='tel',
            field=models.CharField(max_length=11, null=True, unique=True),
        ),
    ]

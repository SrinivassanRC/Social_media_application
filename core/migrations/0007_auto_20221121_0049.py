# Generated by Django 3.0.5 on 2022-11-21 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_post_liked_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='liked_user',
            field=models.ManyToManyField(to='core.Profile'),
        ),
    ]
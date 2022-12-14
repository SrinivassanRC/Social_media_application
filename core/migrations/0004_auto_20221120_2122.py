# Generated by Django 3.0.5 on 2022-11-21 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_profile_img',
            field=models.ImageField(default=2, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.TextField(blank=True, default='path/to/image.png'),
        ),
    ]

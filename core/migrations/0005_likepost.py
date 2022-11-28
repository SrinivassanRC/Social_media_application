# Generated by Django 3.0.5 on 2022-11-21 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20221120_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
                ('profileimg', models.ImageField(default='blank-profile-picture.png', upload_to='profile_images')),
            ],
        ),
    ]
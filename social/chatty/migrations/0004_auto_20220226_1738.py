# Generated by Django 3.0.3 on 2022-02-26 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatty', '0003_auto_20220226_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='pfp',
            field=models.ImageField(default='profile_pics/default.png', upload_to='profile_pics/'),
        ),
    ]
# Generated by Django 3.0.3 on 2022-02-27 01:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatty', '0008_auto_20220226_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reciever', to='chatty.AppUser'),
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='posts/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='chatty.AppUser')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]

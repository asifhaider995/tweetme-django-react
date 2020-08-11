# Generated by Django 3.0.8 on 2020-07-30 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, upload_to='images/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]

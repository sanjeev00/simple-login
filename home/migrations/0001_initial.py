# Generated by Django 3.0.5 on 2020-08-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
    ]

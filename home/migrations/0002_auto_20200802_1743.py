# Generated by Django 3.0.5 on 2020-08-02 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='userId',
            new_name='phone',
        ),
        migrations.AddField(
            model_name='userdata',
            name='mailVerified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdata',
            name='phoneVerified',
            field=models.BooleanField(default=False),
        ),
    ]

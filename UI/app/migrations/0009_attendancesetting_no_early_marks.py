# Generated by Django 2.0 on 2020-11-24 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20201124_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancesetting',
            name='no_early_marks',
            field=models.IntegerField(help_text='After which Absentee will be marked', null=True),
        ),
    ]

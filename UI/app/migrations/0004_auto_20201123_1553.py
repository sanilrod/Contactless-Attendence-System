# Generated by Django 2.0 on 2020-11-23 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_teacher_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='face_image1',
            field=models.ImageField(max_length=255, upload_to='media/uploaded_images/'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='face_image2',
            field=models.ImageField(blank=True, max_length=255, upload_to='media/uploaded_images/'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='face_image3',
            field=models.ImageField(blank=True, max_length=255, upload_to='media/uploaded_images/'),
        ),
    ]

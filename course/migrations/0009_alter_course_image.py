# Generated by Django 4.2.3 on 2024-08-11 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_alter_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, default='course/media/default.jpg', null=True, upload_to='uploads/'),
        ),
    ]

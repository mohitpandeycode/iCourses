# Generated by Django 5.0.3 on 2024-03-14 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_category_remove_course_coursecatagory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='AboutCourse',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

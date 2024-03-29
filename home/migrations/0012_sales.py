# Generated by Django 5.0.3 on 2024-03-16 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_event_participants'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('one_day_sale', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('one_week_sale', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('one_month_sale', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('one_year_sale', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('lifetime_sale', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
            options={
                'verbose_name_plural': 'Sales',
            },
        ),
    ]

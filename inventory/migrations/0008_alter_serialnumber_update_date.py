# Generated by Django 4.2.7 on 2023-12-05 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_serialnumber_in_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serialnumber',
            name='update_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

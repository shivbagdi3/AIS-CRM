# Generated by Django 4.2.7 on 2023-11-06 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_clients_amc_end_date_clients_amc_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='email',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_back', models.CharField(blank=True, max_length=1000)),
                ('feedback_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_id', to='client.clients')),
            ],
        ),
    ]

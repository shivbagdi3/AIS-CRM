# Generated by Django 4.2.7 on 2023-11-29 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(blank=True, max_length=100, unique=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128, region=None)),
                ('Alternate_no', phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128, region=None)),
                ('GST_no', models.CharField(max_length=150, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=50)),
                ('amc_client', models.BooleanField(default=False)),
                ('amc_start_date', models.DateField(blank=True, null=True)),
                ('amc_end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='update_at',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.DateField(blank=True)),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by_user', to=settings.AUTH_USER_MODEL)),
                ('update_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='update_at', to='client.clients')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_back', models.CharField(blank=True, max_length=1000)),
                ('feedback_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback_id', to='client.clients')),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
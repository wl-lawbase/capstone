# Generated by Django 2.0.8 on 2018-09-26 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capapi', '0007_auto_20180921_2052'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_date', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('institution', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('area_of_interest', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved'), ('denied', 'denied'), ('awaiting signature', 'awaiting signature')], default='pending', max_length=20)),
                ('notes', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='research_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-submitted_date'],
            },
        ),
    ]
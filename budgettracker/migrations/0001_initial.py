# Generated by Django 3.1.4 on 2021-03-30 15:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMadeAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UMA_name', models.CharField(max_length=100)),
                ('UMA_type', models.CharField(max_length=100)),
                ('UMA_balance', models.FloatField()),
                ('UMA_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccountTransactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AT_date', models.DateTimeField(auto_now=True)),
                ('AT_description', models.TextField()),
                ('AT_debit', models.FloatField()),
                ('AT_credit', models.FloatField()),
                ('AT_UMA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budgettracker.usermadeaccount')),
            ],
        ),
    ]

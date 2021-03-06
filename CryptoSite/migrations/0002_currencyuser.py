# Generated by Django 4.0.3 on 2022-04-04 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoSite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='currencyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique', models.CharField(default='N/A', max_length=100, null=True)),
                ('amount', models.CharField(default='0', max_length=100, null=True)),
                ('crypto_name', models.CharField(default='N/A', max_length=100, null=True)),
                ('bought_at', models.CharField(default='0', max_length=100, null=True)),
                ('total_price', models.CharField(default='0', max_length=100, null=True)),
            ],
        ),
    ]

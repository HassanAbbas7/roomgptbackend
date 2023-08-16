# Generated by Django 4.2.4 on 2023-08-15 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_customuser_credits'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('stripeId', models.CharField(max_length=40)),
                ('nextInvoice', models.DateField()),
            ],
        ),
    ]
# Generated by Django 4.2.4 on 2023-12-26 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmodel',
            name='transaction_type',
            field=models.IntegerField(choices=[(1, 'Deposit'), (2, 'Withdrawal'), (3, 'Recieve Loan'), (4, 'Pay Loan')], null=True),
        ),
    ]

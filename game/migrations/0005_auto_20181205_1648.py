# Generated by Django 2.1.1 on 2018-12-05 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_transaction_t_notive'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-timestamp']},
        ),
    ]

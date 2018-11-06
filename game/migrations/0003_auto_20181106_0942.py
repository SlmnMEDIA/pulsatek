# Generated by Django 2.1.1 on 2018-11-06 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20181017_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statustransaction',
            name='status',
            field=models.CharField(choices=[('IN', 'IN PROCESS'), ('PE', 'PENDING'), ('SS', 'SUCCESS'), ('FA', 'FAILED'), ('CA', 'CANCELED'), ('FS', 'SUCESSED')], default='IN', max_length=2),
        ),
    ]

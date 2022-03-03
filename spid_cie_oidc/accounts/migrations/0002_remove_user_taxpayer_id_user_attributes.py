# Generated by Django 4.0.2 on 2022-03-02 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spid_cie_oidc_accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='taxpayer_id',
        ),
        migrations.AddField(
            model_name='user',
            name='attributes',
            field=models.JSONField(blank=True, default={}, null=True),
        ),
    ]
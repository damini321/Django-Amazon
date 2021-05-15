# Generated by Django 3.1.7 on 2021-05-15 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_mobile', '0003_auto_20210515_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mobile_technology',
            name='amazon_mobile',
        ),
        migrations.AddField(
            model_name='amazon_mobile',
            name='mobile_technology',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='amazon_mobile.mobile_technology'),
        ),
    ]

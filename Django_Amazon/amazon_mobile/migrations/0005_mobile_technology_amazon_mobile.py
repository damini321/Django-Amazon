# Generated by Django 3.1.7 on 2021-05-02 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon_mobile', '0004_auto_20210502_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobile_technology',
            name='amazon_mobile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='amazon_mobile.amazon_mobile'),
        ),
    ]

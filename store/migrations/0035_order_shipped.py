# Generated by Django 4.0.4 on 2022-05-15 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_alter_address_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False, null=True),
        ),
    ]

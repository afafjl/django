# Generated by Django 4.0.4 on 2022-05-05 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stars',
            field=models.FloatField(default=0),
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-04 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='short_description',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]

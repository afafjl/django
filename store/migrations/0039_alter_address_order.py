# Generated by Django 4.0.4 on 2022-05-15 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_alter_orderitem_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order'),
        ),
    ]

# Generated by Django 4.0.4 on 2022-05-18 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0002_alter_company_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]

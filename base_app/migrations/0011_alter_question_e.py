# Generated by Django 4.0.6 on 2022-10-19 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0010_userresults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='e',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
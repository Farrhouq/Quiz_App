# Generated by Django 4.0.6 on 2022-10-15 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0006_alter_question_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.CharField(blank=True, choices=[(models.CharField(max_length=200, null=True), models.CharField(max_length=200, null=True)), (models.CharField(max_length=200, null=True), models.CharField(max_length=200, null=True)), (models.CharField(max_length=200, null=True), models.CharField(max_length=200, null=True)), (models.CharField(max_length=200, null=True), models.CharField(max_length=200, null=True))], max_length=1),
        ),
    ]

# Generated by Django 4.0.6 on 2022-10-15 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_remove_question_answer_question_a_question_b_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.CharField(choices=[(models.CharField(max_length=200, null=True), 'a'), (models.CharField(max_length=200, null=True), 'b'), (models.CharField(max_length=200, null=True), 'c'), (models.CharField(max_length=200, null=True), 'd')], default=models.CharField(max_length=200, null=True), max_length=1),
        ),
    ]

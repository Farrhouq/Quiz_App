# Generated by Django 4.0.6 on 2022-10-14 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
                ('answer', models.CharField(max_length=1000)),
                ('points', models.IntegerField()),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='HighScoreSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base_app.category')),
            ],
        ),
    ]
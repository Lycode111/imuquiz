# Generated by Django 4.2.3 on 2023-08-29 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='skipped_questions',
            field=models.IntegerField(default=1000),
        ),
        migrations.AddField(
            model_name='analysis',
            name='wrong_questions',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='correct_questions',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='total_questions',
            field=models.IntegerField(default=1000),
        ),
    ]

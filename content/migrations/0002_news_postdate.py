# Generated by Django 4.0.2 on 2022-02-10 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='postDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]

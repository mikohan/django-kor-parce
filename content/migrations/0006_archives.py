# Generated by Django 4.0.2 on 2022-02-20 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_news_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archives',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField()),
            ],
        ),
    ]

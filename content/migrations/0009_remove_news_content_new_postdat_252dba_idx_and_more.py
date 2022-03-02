# Generated by Django 4.0.2 on 2022-03-01 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_news_content_new_postdat_252dba_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='news',
            name='content_new_postDat_252dba_idx',
        ),
        migrations.AddIndex(
            model_name='news',
            index=models.Index(fields=['-postDate', 'newsId'], name='content_new_postDat_88cba5_idx'),
        ),
    ]
# Generated by Django 4.1.1 on 2022-10-03 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_delete_bookmark_delete_like_delete_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.IntegerField(default=0)),
                ('email', models.EmailField(default='', max_length=254)),
                ('is_marked', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.IntegerField(default=0)),
                ('email', models.EmailField(default='', max_length=254)),
                ('is_like', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_id', models.IntegerField(default=0)),
                ('email', models.EmailField(default='', max_length=254)),
                ('reply_content', models.TextField()),
            ],
        ),
    ]

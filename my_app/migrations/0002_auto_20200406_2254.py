# Generated by Django 3.0.4 on 2020-04-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitedArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_title', models.CharField(max_length=128)),
                ('article_url', models.CharField(max_length=500)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.AlterModelOptions(
            name='search',
            options={'verbose_name_plural': 'Searches'},
        ),
    ]

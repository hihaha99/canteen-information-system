# Generated by Django 3.0.3 on 2020-08-13 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_auto_20200812_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
                ('made_on', models.DateField()),
            ],
        ),
    ]

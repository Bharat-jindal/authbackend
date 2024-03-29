# Generated by Django 4.0 on 2021-12-08 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.TextField(max_length=1000)),
                ('password', models.TextField(max_length=1000)),
                ('service', models.TextField(default='oauth', max_length=1000)),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='UserLoginHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.TextField(max_length=1000)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'UserLoginHistory',
            },
        ),
    ]

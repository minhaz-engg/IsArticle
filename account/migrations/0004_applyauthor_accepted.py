# Generated by Django 3.2.7 on 2021-10-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_applyauthor'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyauthor',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]

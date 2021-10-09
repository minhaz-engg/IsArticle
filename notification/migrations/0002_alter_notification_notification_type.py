# Generated by Django 3.2.7 on 2021-10-02 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(1, 'Like'), (2, 'Comment'), (3, 'Follow'), (4, 'Welcome Message'), (5, 'Author Application Accepted'), (6, 'Author Application Denied')]),
        ),
    ]
# Generated by Django 3.2.5 on 2021-07-26 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hascomment',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]

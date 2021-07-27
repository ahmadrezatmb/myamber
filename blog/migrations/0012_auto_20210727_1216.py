# Generated by Django 3.2.5 on 2021-07-27 07:46

import blog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_amberuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amberuser',
            name='avatar',
            field=models.ImageField(blank=True, default=blog.models.get_default_avatar_img, null=True, upload_to='profiles'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.amberuser'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.amberuser'),
        ),
    ]

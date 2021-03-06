# Generated by Django 3.1 on 2020-08-10 20:01

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0006_annotation_shape'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='org_img_height',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='org_img_width',
            field=models.PositiveIntegerField(default=456),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='annotation',
            name='coordinates_x',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='annotation',
            name='coordinates_y',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='image',
            name='original_image',
            field=models.ImageField(height_field='org_img_height', null=True, upload_to='original_image', width_field='org_img_width'),
        ),
    ]

# Generated by Django 4.2.5 on 2023-10-15 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intSocial', '0005_alter_imagen_src'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagen',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

# Generated by Django 2.0.13 on 2019-08-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostmgr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pattern',
            name='name',
            field=models.CharField(blank=True, help_text='name/reference for this hostname pattern', max_length=16, null=True, unique=True),
        ),
    ]

# Generated by Django 4.0.6 on 2023-09-19 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentoria', '0008_diade_ano_lectivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentorando',
            name='nota',
        ),
        migrations.AddField(
            model_name='mentor',
            name='ativo',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AddField(
            model_name='mentorando',
            name='ativo',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]

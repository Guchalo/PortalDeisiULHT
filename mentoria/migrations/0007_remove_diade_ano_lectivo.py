# Generated by Django 4.0.6 on 2023-09-16 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mentoria', '0006_remove_diade_ano_diade_ano_lectivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diade',
            name='ano_lectivo',
        ),
    ]

# Generated by Django 4.0.6 on 2023-06-25 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_ocorrencia_colaborador_alter_ocorrencia_utente'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocorrencia',
            name='titulo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

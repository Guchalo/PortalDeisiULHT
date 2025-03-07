# Generated by Django 4.2.1 on 2023-11-27 12:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentoria', '0014_rename_comfirmado_sessao_confirmado'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessao',
            name='avaliacao_mentor',
            field=models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='sessao',
            name='avaliacao_mentorando',
            field=models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AddField(
            model_name='sessao',
            name='objetivo',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='sessao',
            name='observacoes',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='sessao',
            name='planificacao_proxima_sessao',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='sessao',
            name='recursos',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='sessao',
            name='sumario',
            field=models.CharField(default='', max_length=200),
        ),
    ]

# Generated by Django 4.0.6 on 2023-09-16 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_diade_sessao_mentorando_mentor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mentor',
            name='aluno',
        ),
        migrations.RemoveField(
            model_name='mentor',
            name='disciplina',
        ),
        migrations.RemoveField(
            model_name='mentorando',
            name='aluno',
        ),
        migrations.RemoveField(
            model_name='mentorando',
            name='disciplina',
        ),
        migrations.RemoveField(
            model_name='sessao',
            name='diade',
        ),
        migrations.DeleteModel(
            name='Diade',
        ),
        migrations.DeleteModel(
            name='Mentor',
        ),
        migrations.DeleteModel(
            name='Mentorando',
        ),
        migrations.DeleteModel(
            name='Sessao',
        ),
    ]

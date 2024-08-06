# Generated by Django 4.0.6 on 2023-09-09 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_aluno_curso_disciplina_turma_aluno_curso_aluno_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplina',
            name='alunos',
            field=models.ManyToManyField(blank=True, null=True, related_name='disciplinas', to='app.aluno'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='alunos',
            field=models.ManyToManyField(blank=True, null=True, related_name='turmas', to='app.aluno'),
        ),
    ]

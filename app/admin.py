from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Curso)

class DAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'semestre', 'inscritos')
    ordering = ('ano', 'semestre', 'nome')

admin.site.register(Disciplina, DAdmin)


class TurmaAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'nome', 'lotacao', 'inscritos')

admin.site.register(Turma, TurmaAdmin)

admin.site.register(Aluno)

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(AnoLectivo)


admin.site.register(Mentor)


admin.site.register(Mentorando)


class DiadeAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'mentorando')

admin.site.register(Diade, DiadeAdmin)


admin.site.register(Sessao)
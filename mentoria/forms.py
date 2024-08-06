from django import forms
from django.forms import ModelForm
from .models import Sessao

class SessaoForm(ModelForm):
    class Meta:
        model = Sessao
        fields = '__all__'
        labels = {
        'objetivo': 'Objetivos da sessão',
        'recursos': 'Recursos utilizados',
        'avaliacao_mentor': 'Avaliação do trabalho realizado pelo Mentorando',
        'avaliacao_mentorando': 'Avaliação do trabalho realizado pelo Mentor',
        'observacoes': 'Observações/Dificuldades encontradas',
        'planificacao_proxima_sessao': 'Planificação da sessão seguinte',
        'sumario': 'Sumário',
    }
        widgets = {
            'diade': forms.HiddenInput(),
            'avaliacao_mentorando': forms.HiddenInput(),
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'sumario':forms.Textarea(attrs={'rows': '5','cols': '30','style':'width:100%;height:50px;'}),
            'confirmado': forms.HiddenInput(),
            'reportado': forms.HiddenInput(),
            'objetivo':forms.Textarea(attrs={'rows': '5','cols': '30','style':'width:100%;height:50px;'}),
            'recursos':forms.Textarea(attrs={'rows': '5','cols': '30','style':'width:100%;height:50px;'}),
            'observacoes':forms.Textarea(attrs={'rows': '5','cols': '30','style':'width:100%;height:50px;'}),
            'planificacao_proxima_sessao':forms.Textarea(attrs={'rows': '5','cols': '30','style':'width:100%;height:50px;'}),
            
        }




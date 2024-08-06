from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import SessaoForm

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from datetime import datetime, date

from matplotlib import pyplot as plt
import io
import urllib, base64
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import matplotlib
import calendar
import locale
matplotlib.use('Agg')

ano = AnoLectivo.objects.get(id=1)
semestre = 2

# Create your views here.
@login_required
def mentores_view(request):


    if request.user.is_superuser:
        mentores = list(set(mentor.aluno for mentor in Mentor.objects.filter(ano_lectivo=ano)))
        alunoAtual = "admin"
    else:
        alunoAtual = Aluno.objects.get(user = request.user)
        mentores = list(set(mentor.aluno for mentor in Mentor.objects.filter(ano_lectivo=ano,aluno=alunoAtual,disciplina__semestre=semestre)))

    mentores.sort(key=lambda item:str(item))
    mentorandos = list(set(mentorando.aluno for mentorando in Mentorando.objects.filter(ano_lectivo=ano,disciplina__semestre=semestre)))
    mentorandos.sort(key=lambda item:str(item))

    diades = Diade.objects.filter(ano_lectivo = ano)


    candidatosSemMentoria = []
    mentores_info = []
    disciplinas_sem_mentoria = []
    for mentor in mentores:
        info = {}
        info['mentor'] = mentor


        mentorias = []

        for mentoria in mentor.mentorias.all():
            info_ = {}

            if mentoria.disciplina.semestre == semestre:
                info_['disciplina'] = mentoria.disciplina

                diades_ = []
                for diade in diades:
                    if mentoria.disciplina.semestre == semestre:
                        if diade.mentor.aluno == mentor and mentoria.disciplina == diade.mentor.disciplina:
                                diades_.append(diade.mentorando.aluno)
                info_['diades'] = diades_

                mentorias.append(info_)

            info['mentorias'] = mentorias


        candidatos = []
        listaMentores = []

        if request.user.is_superuser:
            listaMentores = list(Mentor.objects.filter(ano_lectivo=ano))
            allCandidatos = list(Mentorando.objects.filter(ano_lectivo=ano))
        else:
            allCandidatos = list(Mentorando.objects.filter(ano_lectivo=ano).exclude(aluno=alunoAtual))
            listaMentores = list(Mentor.objects.filter(ano_lectivo=ano).exclude(aluno=alunoAtual))




        for candidato in allCandidatos:
            flag = 0
            for diade in Diade.objects.all():
                if diade.mentorando == candidato:
                    flag = 1

            if flag == 0:
               candidatosSemMentoria.append(candidato)

        candidatosSemMentoria.sort(key=lambda x: x.aluno.nome_completo)

        for mentoria in Mentor.objects.filter(ano_lectivo=ano):
            if mentoria.aluno == mentor and mentoria.disciplina.semestre == semestre:
                for mentorando in allCandidatos:
                    if mentoria.disciplina == mentorando.disciplina:
                        for diade in Diade.objects.all():
                            if diade.mentorando == mentorando and diade.mentor.disciplina == mentorando.disciplina:
                                break
                        else:
                            candidatos.append(mentorando)



        info['candidatos'] = candidatos
        info['mentorias'] = mentorias


        disciplinas_com_mentoria = [mentoria['disciplina'] for mentoria in mentorias]
        info['disciplinas_sem_mentoria'] = Disciplina.objects.exclude(pk__in=[disciplina.pk for disciplina in disciplinas_com_mentoria])
        info['disciplinas_sem_mentoria'] = info['disciplinas_sem_mentoria'].filter(semestre=semestre)
        disciplinas_sem_mentoria = info['disciplinas_sem_mentoria']

        mentores_info.append(info)
    if len(disciplinas_sem_mentoria) == 0:
        disciplinas_sem_mentoria = Disciplina.objects.filter(semestre=semestre)




    context = {'mentores': mentores, 'mentorandos': mentorandos, 'ano':ano, 'diades':diades, 'mentores_info':mentores_info,
                'vazio':len(mentores),'aluno': alunoAtual,
                'disciplinas':disciplinas_sem_mentoria, 'allCandidatos': candidatosSemMentoria}

    return render(request, 'mentoria/mentores.html', context)


# Create your views here.
@login_required
def cria_diade_view(request):

    if request.method == 'POST':
        mentorando = Mentorando.objects.get(id=request.POST['mentorando_id'])

        aluno_mentor = Aluno.objects.get(id=request.POST['mentor_aluno_id'])
        mentor = Mentor.objects.get(
                        aluno=aluno_mentor,
                        disciplina = mentorando.disciplina,
                    )

        if not Diade.objects.filter(ano_lectivo=ano, mentor = mentor, mentorando=mentorando).exists():
            diade = Diade.objects.create(ano_lectivo=ano, mentor = mentor, mentorando=mentorando)


    return redirect('mentores')





# Create your views here.
@login_required
def mentorandos_view(request):


    if request.user.is_superuser:
        alunos_mentorando = set( m.aluno for m in Mentorando.objects.filter(ano_lectivo=ano) )
        alunoAtual = "admin"
    else:
        alunoAtual = Aluno.objects.get(user = request.user)
        alunos_mentorando = set( m.aluno for m in Mentorando.objects.filter(ano_lectivo=ano,aluno=alunoAtual) )




    alunos = Aluno.objects.all()



    mentorandos_info = []
    disciplinas_sem_mentoria = []

    for aluno_mentorando in alunos_mentorando:
        info = {}
        info['mentorando'] = aluno_mentorando

        mentorandias = []

        for mentorando in Mentorando.objects.filter( ano_lectivo=ano, aluno=aluno_mentorando ):
            info_ = {}

            info_['mentorando'] = mentorando
            info_['disciplina'] = mentorando.disciplina

            diades = Diade.objects.filter(ano_lectivo=ano, mentorando = mentorando )

            for diade in diades:
                    if diade.mentorando.disciplina == mentorando.disciplina:
                        info_['mentor'] = diade.mentor
                        break
            else:
                info_['mentor'] = '-'

            mentorandias.append(info_)

        mentorandias.sort(key=lambda item:item['disciplina'].nome)
        info['mentorandias'] = mentorandias

        disciplinas_com_mentoria = [mentorandia['disciplina'] for mentorandia in mentorandias]
        info['disciplinas_sem_mentoria'] = Disciplina.objects.exclude(pk__in=[disciplina.pk for disciplina in disciplinas_com_mentoria])
        info['disciplinas_sem_mentoria'] = info['disciplinas_sem_mentoria'].filter(semestre=semestre)
        disciplinas_sem_mentoria = info['disciplinas_sem_mentoria']
        mentorandos_info.append(info)

    if len(disciplinas_sem_mentoria) == 0:
        disciplinas_sem_mentoria = Disciplina.objects.filter(semestre=semestre)



    context = { 'ano':ano, 'mentorandos_info':mentorandos_info, 'vazio':len(mentorandos_info), 'aluno': alunoAtual,
                'disciplinas':disciplinas_sem_mentoria}

    return render(request, 'mentoria/mentorandos.html', context)



# Create your views here.
@login_required
def diades_view(request):
    context = {'diades': Diade.objects.all()}
    return render(request, 'mentoria/diades.html', context)

@login_required
def cria_mentor_view(request):

    if request.method == 'POST':
        aluno = Aluno.objects.get(id=request.POST['mentor_aluno_id'])
        disciplina = Disciplina.objects.get(id=request.POST['disciplina_id'])

        Mentor.objects.create(ano_lectivo=ano, aluno=aluno, disciplina=disciplina)

    return redirect('mentores')

@login_required
def cria_mentorando_view(request):

    if request.method == 'POST':
        aluno = Aluno.objects.get(id=request.POST['mentorando_aluno_id'])
        disciplina = Disciplina.objects.get(id=request.POST['disciplina_id'])

        Mentorando.objects.create(ano_lectivo=ano, aluno=aluno, disciplina=disciplina)

        mentores = list(Mentor.objects.filter(disciplina = disciplina))

       # for para enviar email aos mentores(dessa disciplina) quando um mentorando escolhe uma disciplina

       # for a in mentores:
            #email = a.aluno.user.email

            #send_mail(
            #'Aviso para Mentores',
           # f'Olá,\nExiste um novo aluno a precisar de mentoria a {disciplina}.\nCaso esteja interessado, entre na plataforma para aceitar a mentoria.',
           # 'goncalo.coelhonunes@gmail.com',
           # [email]
    #)

    return redirect('mentorandos')

@login_required
def remover_mentorando_view(request, mentorando_id):

    mentorando = Mentorando.objects.get(id=mentorando_id)
    diade = Diade.objects.filter(mentorando=mentorando)

    if len(diade):
        if mentorando.ativo == False & diade[0].ativo == False:
            mentorando.ativo = True
            mentorando.save()

            diade[0].ativo = True
            diade[0].save()
        else:
            mentorando.ativo = False
            mentorando.save()

            diade[0].ativo = False
            diade[0].save()
    else:
        mentorando.delete()

    return redirect('mentorandos')

@login_required
def sessoes_view(request,mentor_id,mentorando_id,sep):
    ano = AnoLectivo.objects.get(id=1)

    if request.user.is_superuser:
        context = {'sessoes': Sessao.objects.all()}
    else:
        mentor = Mentor.objects.get(id=mentor_id)
        mentorando = Mentorando.objects.get(id=mentorando_id)
        disciplina = mentor.disciplina
        diade = Diade.objects.get(mentor=mentor,mentorando=mentorando)

        # A variavel 'sep' é usada para distinguir quem entra na view da sessão
        # Mentor -> sep = 0
        # Mentorando -> sep = 1

        context = {'sessoes': Sessao.objects.filter(diade = diade),
                'diade': diade,
                'sep': sep,
                'disciplina':disciplina,
                'mentor':mentor,
                'mentorando':mentorando}



    return render(request, 'mentoria/sessoes.html', context)


@login_required
def criar_sessao_view(request, diade_id):

    diade = Diade.objects.get(id=diade_id)

    if request.method == 'POST':
        form = SessaoForm(request.POST)
        if form.is_valid():
            form.diade = diade
            form.save()
            return redirect('sessoes', diade.mentor_id, diade.mentorando_id, 0)
    else:
        form = SessaoForm(initial={'diade': diade})

    return render(request, 'mentoria/criar_sessao.html', { 'form': form, 'diade': diade})


@login_required
def edita_sessao_view(request, sessao_id):

    sessao = get_object_or_404(Sessao, id=sessao_id)
    diade = Sessao.objects.get(id=sessao_id).diade

    if request.method == 'POST':
        form = SessaoForm(request.POST, instance=sessao)

        if form.is_valid():
            form.save()
            return redirect('sessoes', diade.mentor_id, diade.mentorando_id, 0)

    else:
        form = SessaoForm(instance=sessao)

    context = {'form': form, 'sessao_id': sessao_id, 'diade': diade}
    return render(request, 'mentoria/editar_sessao.html', context)


@login_required
def apaga_sessao_view(request, sessao_id):
    diade = Sessao.objects.get(id=sessao_id).diade
    Sessao.objects.get(id=sessao_id).delete()
    return redirect('sessoes', diade.mentor_id, diade.mentorando_id, 0)

@login_required
def perfil_view(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)

    return render(request, 'mentoria/perfil.html', {'aluno': aluno})

@login_required
def vermais_view(request, sessao_id):
    sessao = Sessao.objects.get(id=sessao_id)

    return render(request, 'mentoria/ver_mais.html', {'sessao': sessao})

@login_required
def all_sessoes_view(request):
    if request.user.is_superuser:
        sessoes = list(Sessao.objects.all())

    else:
        alunoAtual = Aluno.objects.get(user = request.user)
        sessoes = list(sessao for sessao in Sessao.objects.filter(diade__mentor__aluno=alunoAtual))

    sessoes.sort(key=lambda x: x.data,reverse=True)
    return render(request, 'mentoria/all_sessoes.html', {'sessoes': sessoes, 'filtro': 'n'})

@login_required
def av_mentorando_view(request, sessao_id):
    sessao = get_object_or_404(Sessao, id=sessao_id)
    diade = Sessao.objects.get(id=sessao_id).diade

    if request.method == 'POST':

        sessao.confirmado = True
        avaliacao_mentorando = request.POST.get('avaliacao_mentorando')
        if avaliacao_mentorando is not None:
            sessao.avaliacao_mentorando = avaliacao_mentorando

        sessao.save()

        return redirect('sessoes', diade.mentor_id, diade.mentorando_id, 1)

    return render(request, 'mentoria/av_mentorando.html', {'sessao': sessao, 'diade': diade})

@login_required
def report_sessao_view(request, sessao_id):
    sessao = get_object_or_404(Sessao, id=sessao_id)
    diade = Sessao.objects.get(id=sessao_id).diade
    sessao.reportado = True
    sessao.save()
    return redirect('all_sessoes')

@login_required
def report_sessaoR_view(request):
    sessoes = list(Sessao.objects.filter(reportado = False))
    sessoes.sort(key=lambda x: x.data,reverse=True)
    return render(request, 'mentoria/all_sessoes.html', {'sessoes': sessoes , 'filtro': 'r'})

def info_view(request):
    return render(request, 'mentoria/info.html')

def dashboard_view(request):
    sessoes = list(Sessao.objects.all())
    mentores = list(Mentor.objects.all())
    diades = list(Diade.objects.all())
    mentorandos = list(Mentorando.objects.all())
    dataAtual = datetime.now()

    sessoesMes = [s for s in sessoes if s.data.month == dataAtual.now().month]

    mentoresMes = set(s.diade.mentor.aluno for s in sessoesMes)
    mentorandosMes = set(s.diade.mentorando.aluno for s in sessoesMes)

    disciplinas = {}
    for s in sessoesMes:
        if s.diade.mentor.disciplina not in disciplinas:
            disciplinas[s.diade.mentor.disciplina] = 1
        else:
            disciplinas[s.diade.mentor.disciplina] += 1





    return render(request, 'mentoria/dashboard.html',{'sessoes': sessoes,'diades': diades,'mentores': mentores,'mentorandos': mentorandos,
                                                      'sessoesMes': sessoesMes, 'mentoresMes':mentoresMes, 'mentorandosMes':mentorandosMes,
                                                      'disciplinas': disciplinas, 'data': cria_grafico()})



def cria_grafico():


    locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8')
    ano_atual = datetime.now().year

    sessoes_por_mes = Sessao.objects.filter(data__year=ano_atual).annotate(mes=ExtractMonth('data')).values('mes').annotate(count=Count('id')).order_by('mes')



    meses = [item['mes'] for item in sessoes_por_mes]
    count = [item['count'] for item in sessoes_por_mes]
    nomes_meses = [datetime(2023, mes, 1).strftime('%B') for mes in meses]

    plt.barh(meses, count)
    plt.ylabel("Mês")
    plt.yticks(ticks=meses, labels=nomes_meses)
    plt.xlabel("Nº de Sessoões")

    for index, value in enumerate(count):
        plt.text(value, meses[index], str(value))

    plt.autoscale()

    fig = plt.gcf()
    plt.close()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')


    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return uri
from django.core.management.base import BaseCommand
import pandas as pd
from django.contrib.auth.models import User
from app.models import *


class Command(BaseCommand):
    help = 'Descrição do seu comando personalizado'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to Excel file')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            nome_aluno = row['Nome']
            apelido = row['Apelido']
            numero_aluno = row['Número de identificação (ID)']
            email = row['Endereço de e-mail']

            # Criar um novo usuário Django usando o número de aluno como nome de usuário
            user = User.objects.create_user(username=str(numero_aluno), email=email, password=None)
            user.first_name = nome_aluno
            user.last_name = apelido
            user.save()

            curso = Curso.objects.get(nome='MEISI')

            aluno = Aluno.objects.create(user=user,numero=numero_aluno,curso=curso)


            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {nome_aluno} {apelido}'))



        self.stdout.write(self.style.SUCCESS('Comando executado nha'))
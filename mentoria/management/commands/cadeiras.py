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
            semestreA = row['Semestre']
            ciclo = row['Ciclo']
            anoA = row['Ano']
            disciplinaA = row['Disciplina']

            # Criar um novo usuário Django usando o número de aluno como nome de usuário

            cadeira = Disciplina.objects.create(nome=disciplinaA,ano=anoA,semestre=semestreA)



            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {cadeira}'))
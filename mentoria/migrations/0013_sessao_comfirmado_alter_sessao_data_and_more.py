# Generated by Django 4.2.1 on 2023-11-26 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentoria', '0012_alter_sessao_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessao',
            name='comfirmado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sessao',
            name='data',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sessao',
            name='sumario',
            field=models.CharField(max_length=200),
        ),
    ]

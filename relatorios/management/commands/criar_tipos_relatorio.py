"""
Management command para criar tipos de relatório padrão.
"""
from django.core.management.base import BaseCommand
from relatorios.models import TipoRelatorio


class Command(BaseCommand):
    help = 'Cria tipos de relatório padrão'

    def handle(self, *args, **options):
        tipos_relatorio = [
            {
                'nome': 'Relatório Completo de Progresso',
                'descricao': 'Relatório completo com gráficos, medidas corporais, frequência e evolução',
                'template_filename': 'relatorio_completo.html',
                'incluir_graficos': True,
                'incluir_fotos': True,
                'incluir_medidas': True,
                'incluir_frequencia': True,
            },
            {
                'nome': 'Relatório de Evolução de Peso',
                'descricao': 'Relatório focado na evolução do peso e IMC',
                'template_filename': 'relatorio_peso.html',
                'incluir_graficos': True,
                'incluir_fotos': False,
                'incluir_medidas': True,
                'incluir_frequencia': False,
            },
            {
                'nome': 'Relatório de Frequência',
                'descricao': 'Relatório focado na frequência e assiduidade dos treinos',
                'template_filename': 'relatorio_frequencia.html',
                'incluir_graficos': True,
                'incluir_fotos': False,
                'incluir_medidas': False,
                'incluir_frequencia': True,
            },
            {
                'nome': 'Relatório de Medidas Corporais',
                'descricao': 'Relatório focado na evolução das medidas corporais',
                'template_filename': 'relatorio_medidas.html',
                'incluir_graficos': True,
                'incluir_fotos': True,
                'incluir_medidas': True,
                'incluir_frequencia': False,
            },
            {
                'nome': 'Relatório Simplificado',
                'descricao': 'Relatório resumido sem gráficos, ideal para envio rápido',
                'template_filename': 'relatorio_simples.html',
                'incluir_graficos': False,
                'incluir_fotos': False,
                'incluir_medidas': True,
                'incluir_frequencia': True,
            },
        ]

        criados = 0
        for tipo_data in tipos_relatorio:
            tipo, created = TipoRelatorio.objects.get_or_create(
                nome=tipo_data['nome'],
                defaults=tipo_data
            )
            
            if created:
                criados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Criado: {tipo.nome}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ Já existe: {tipo.nome}')
                )

        if criados > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n{criados} tipo(s) de relatório criado(s) com sucesso!'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    '\nTodos os tipos de relatório já existem.'
                )
            )

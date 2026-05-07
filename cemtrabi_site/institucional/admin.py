from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from .models import Encaminhamento, Lead


def exportar_para_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Leads CEMTRABI"

    headers = [
        'Empresa',
        'CNPJ',
        'Responsável',
        'E-mail',
        'Telefone',
        'Serviço',
        'Status',
        'Origem',
        'Mensagem',
        'Data de Criação',
    ]
    ws.append(headers)

    for lead in queryset:
        ws.append([
            lead.empresa,
            lead.cnpj,
            lead.responsavel,
            lead.email,
            lead.telefone,
            lead.get_servico_display(),
            lead.get_status_display(),
            lead.origem,
            lead.mensagem,
            lead.criado_em.strftime('%d/%m/%Y %H:%M'),
        ])

    for column_cells in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column_cells[0].column)

        for cell in column_cells:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        ws.column_dimensions[column_letter].width = max_length + 2

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=leads_cemtrabi.xlsx'

    wb.save(response)
    return response


def listar_exames_encaminhamento(encaminhamento):
    exames = [
        ('Exame Clínico', encaminhamento.exame_clinico),
        ('Audiometria Tonal', encaminhamento.audiometria),
        ('Acuidade Visual', encaminhamento.acuidade_visual),
        ('Eletrocardiograma', encaminhamento.eletrocardiograma),
        ('Eletroencefalograma', encaminhamento.eletroencefalograma),
        ('Espirometria', encaminhamento.espirometria),
        ('Avaliação Psicossocial', encaminhamento.avaliacao_psicossocial),
        ('Raio X Tórax Padrão OIT', encaminhamento.raio_x_torax),
        ('Teste de Equilíbrio/Romberg', encaminhamento.teste_romberg),
        ('Hemograma Completo com Plaquetas', encaminhamento.hemograma),
        ('Glicemia em Jejum', encaminhamento.glicemia),
        ('Ácido Hipúrico', encaminhamento.acido_hipurico),
        ('Ácido Metil Hipúrico', encaminhamento.acido_metil_hipurico),
        ('Grupo Sanguíneo/Fator RH', encaminhamento.grupo_sanguineo_fator_rh),
    ]

    exames_selecionados = [nome for nome, marcado in exames if marcado]

    if encaminhamento.outro_exame and encaminhamento.descricao_outro_exame:
        exames_selecionados.append(encaminhamento.descricao_outro_exame)

    if encaminhamento.outro_exame and not encaminhamento.descricao_outro_exame:
        exames_selecionados.append('Outro exame')

    return '\n'.join(exames_selecionados)


def exportar_encaminhamentos_para_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Encaminhamentos'

    headers = [
        'Nome',
        'Empresa',
        'CNPJ',
        'Função',
        'Setor',
        'Tipo de Exame',
        'Exames Selecionados',
        'Telefone',
        'Email',
        'Nome do Emitente',
        'Data do Encaminhamento',
        'Data de Criação',
    ]
    ws.append(headers)

    for encaminhamento in queryset:
        ws.append([
            encaminhamento.nome,
            encaminhamento.empresa,
            encaminhamento.cnpj,
            encaminhamento.funcao,
            encaminhamento.setor,
            encaminhamento.get_tipo_exame_display(),
            listar_exames_encaminhamento(encaminhamento),
            encaminhamento.telefone,
            encaminhamento.email,
            encaminhamento.nome_emitente,
            encaminhamento.data_encaminhamento.strftime('%d/%m/%Y'),
            timezone.localtime(encaminhamento.created_at).strftime('%d/%m/%Y %H:%M'),
        ])

    header_fill = PatternFill(fill_type='solid', fgColor='D9EAD3')
    header_font = Font(bold=True)
    header_alignment = Alignment(horizontal='center', vertical='center')
    body_alignment = Alignment(vertical='top', wrap_text=True)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment

    for row in ws.iter_rows(min_row=2):
        max_lines = 1
        for cell in row:
            cell.alignment = body_alignment
            if isinstance(cell.value, str):
                max_lines = max(max_lines, cell.value.count('\n') + 1)
        ws.row_dimensions[row[0].row].height = max(18, max_lines * 15)

    for column_cells in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column_cells[0].column)

        for cell in column_cells:
            if cell.value:
                cell_lines = str(cell.value).split('\n')
                max_length = max(max_length, *(len(line) for line in cell_lines))

        ws.column_dimensions[column_letter].width = min(max_length + 2, 45)

    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions

    data_arquivo = timezone.localdate().strftime('%Y-%m-%d')
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = (
        f'attachment; filename=encaminhamentos_cemtrabi_{data_arquivo}.xlsx'
    )

    wb.save(response)
    return response


exportar_encaminhamentos_para_excel.short_description = (
    'Exportar encaminhamentos para Excel'
)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'empresa',
        'responsavel',
        'email',
        'telefone',
        'servico',
        'status',
        'criado_em',
    )
    list_filter = ('servico', 'status')
    search_fields = ('empresa', 'responsavel', 'email')
    actions = [exportar_para_excel]

    exportar_para_excel.short_description = "Exportar leads selecionados para Excel"


@admin.register(Encaminhamento)
class EncaminhamentoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'empresa',
        'funcao',
        'tipo_exame',
        'status_badge',
        'criado_em',
        'email_enviado',
        'link_docx',
        'link_pcmso',
    )
    list_filter = ('tipo_exame', 'status', 'created_at', 'empresa')
    search_fields = ('nome', 'cpf', 'empresa', 'funcao')
    readonly_fields = (
        'idade',
        'email_enviado',
        'link_docx',
        'link_pcmso',
        'created_at',
    )
    actions = [exportar_encaminhamentos_para_excel]

    fieldsets = (
        ('Dados do Colaborador', {
            'fields': (
                'nome',
                'cpf',
                'rg',
                'data_nascimento',
                'idade',
                'telefone',
                'email',
            )
        }),
        ('Dados da Empresa', {
            'fields': (
                'empresa',
                'cnpj',
                'nome_emitente',
                'endereco_empresa',
                'data_encaminhamento',
            )
        }),
        ('Tipo de Exame', {
            'fields': (
                'funcao',
                'setor',
                'data_admissao',
                'riscos_ocupacionais',
                'tipo_exame',
            )
        }),
        ('Exames Complementares', {
            'fields': (
                'exame_clinico',
                'audiometria',
                'hemograma',
                'glicemia',
                'acuidade_visual',
                'eletrocardiograma',
                'eletroencefalograma',
                'espirometria',
                'avaliacao_psicossocial',
                'raio_x_torax',
                'teste_romberg',
                'acido_hipurico',
                'acido_metil_hipurico',
                'grupo_sanguineo_fator_rh',
                'outro_exame',
                'descricao_outro_exame',
            )
        }),
        ('Arquivos', {
            'fields': (
                'pcmso',
                'link_pcmso',
                'docx_gerado',
                'link_docx',
            )
        }),
        ('Controle Interno', {
            'fields': (
                'status',
                'email_enviado',
                'created_at',
            )
        }),
    )

    def status_badge(self, obj):
        cores = {
            'pendente': '#6c757d',
            'recebido': '#0d6efd',
            'agendado': '#fd7e14',
            'concluido': '#0b6623',
            'cancelado': '#c82333',
        }
        return format_html(
            '<span style="background:{}; color:#fff; padding:4px 9px; '
            'border-radius:999px; font-weight:600; white-space:nowrap;">{}</span>',
            cores.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )

    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'status'

    def criado_em(self, obj):
        return timezone.localtime(obj.created_at).strftime('%d/%m/%Y %H:%M')

    criado_em.short_description = 'Criado em'
    criado_em.admin_order_field = 'created_at'

    def link_docx(self, obj):
        if not obj or not obj.docx_gerado:
            return '-'
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">Baixar DOCX</a>',
            obj.docx_gerado.url
        )

    link_docx.short_description = 'DOCX'

    def link_pcmso(self, obj):
        if not obj or not obj.pcmso:
            return '-'
        return format_html(
            '<a href="{}" target="_blank" rel="noopener">Baixar PCMSO</a>',
            obj.pcmso.url
        )

    link_pcmso.short_description = 'PCMSO'

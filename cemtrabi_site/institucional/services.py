from pathlib import Path
from tempfile import mkstemp
import os
import logging
import re
import unicodedata

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File
from django.core.mail import EmailMessage
from docxtpl import DocxTemplate


logger = logging.getLogger(__name__)


def _formatar_data(data):
    if not data:
        return ''
    return data.strftime('%d/%m/%Y')


def _marcar(valor):
    return 'X' if valor else ''


def _normalizar_nome_arquivo(valor):
    valor = unicodedata.normalize('NFKD', valor or '')
    valor = valor.encode('ascii', 'ignore').decode('ascii')
    valor = valor.lower()
    valor = re.sub(r'[^a-z0-9]+', '_', valor)
    valor = valor.strip('_')
    return valor or 'colaborador'


def montar_contexto_encaminhamento(encaminhamento):
    tipo_exame = encaminhamento.tipo_exame

    return {
        'cnpj': encaminhamento.cnpj,
        'empresa': encaminhamento.empresa,
        'endereco_empresa': encaminhamento.endereco_empresa,
        'nome_emitente': encaminhamento.nome_emitente,
        'telefone': encaminhamento.telefone,
        'data_encaminhamento': _formatar_data(encaminhamento.data_encaminhamento),
        'nome': encaminhamento.nome,
        'data_nascimento': _formatar_data(encaminhamento.data_nascimento),
        'Idade': encaminhamento.idade or encaminhamento.calcular_idade(),
        'data_admissao': _formatar_data(encaminhamento.data_admissao),
        'rg': encaminhamento.rg,
        'cpf': encaminhamento.cpf,
        'funcao': encaminhamento.funcao,
        'setor': encaminhamento.setor,
        'riscos_ocupacionais': encaminhamento.riscos_ocupacionais,
        'adm_x': _marcar(tipo_exame == 'admissional'),
        'dem_x': _marcar(tipo_exame == 'demissional'),
        'per_x': _marcar(tipo_exame == 'periodico'),
        'ret_trab_x': _marcar(tipo_exame == 'retorno_trabalho'),
        'mudanca_x': _marcar(tipo_exame == 'mudanca_funcao'),
        'exame_clinico_x': _marcar(encaminhamento.exame_clinico),
        'audiometria_tonal_x': _marcar(encaminhamento.audiometria),
        'acuidade_visual_x': _marcar(encaminhamento.acuidade_visual),
        'eletrocardiograma_x': _marcar(encaminhamento.eletrocardiograma),
        'eletroencefalograma_x': _marcar(encaminhamento.eletroencefalograma),
        'espirometria_x': _marcar(encaminhamento.espirometria),
        'avaliacao_psicossocial_x': _marcar(encaminhamento.avaliacao_psicossocial),
        'raio_x': _marcar(encaminhamento.raio_x_torax),
        'romberg_x': _marcar(encaminhamento.teste_romberg),
        'hemograma_completo_x': _marcar(encaminhamento.hemograma),
        'glicemia_jejum_x': _marcar(encaminhamento.glicemia),
        'acido_hipurico_x': _marcar(encaminhamento.acido_hipurico),
        'acido_metil_hipurico_x': _marcar(encaminhamento.acido_metil_hipurico),
        'grupo_sanguineo_x': _marcar(encaminhamento.grupo_sanguineo_fator_rh),
        'outro_exame_x': _marcar(encaminhamento.outro_exame),
        'descricao_outro_exame': encaminhamento.descricao_outro_exame,
    }


def gerar_docx_encaminhamento(encaminhamento):
    template_path = Path(settings.ENCAMINHAMENTO_DOCX_TEMPLATE)
    doc = DocxTemplate(template_path)
    doc.render(montar_contexto_encaminhamento(encaminhamento))

    nome_colaborador = _normalizar_nome_arquivo(encaminhamento.nome)
    data_encaminhamento = encaminhamento.data_encaminhamento.strftime('%Y-%m-%d')
    nome_arquivo = (
        f'encaminhamentos/docx/'
        f'encaminhamento_{nome_colaborador}_{data_encaminhamento}.docx'
    )

    descritor, caminho_temporario = mkstemp(suffix='.docx')
    os.close(descritor)

    try:
        doc.save(caminho_temporario)

        if default_storage.exists(nome_arquivo):
            default_storage.delete(nome_arquivo)

        with open(caminho_temporario, 'rb') as arquivo_temporario:
            caminho_salvo = default_storage.save(nome_arquivo, File(arquivo_temporario))
    finally:
        if os.path.exists(caminho_temporario):
            os.remove(caminho_temporario)

    encaminhamento.__class__.objects.filter(pk=encaminhamento.pk).update(
        docx_gerado=caminho_salvo
    )
    encaminhamento.docx_gerado.name = caminho_salvo
    return caminho_salvo


def enviar_email_encaminhamento(encaminhamento):
    if not encaminhamento.docx_gerado:
        return False

    corpo = f"""Olá,

Um novo encaminhamento foi realizado através do sistema.

Dados do colaborador:

* Nome: {encaminhamento.nome}
* Empresa: {encaminhamento.empresa}
* Função: {encaminhamento.funcao}
* Setor: {encaminhamento.setor}
* Tipo de exame: {encaminhamento.get_tipo_exame_display()}
* Data do encaminhamento: {_formatar_data(encaminhamento.data_encaminhamento)}

O documento de encaminhamento segue anexado neste email.

Mensagem automática do sistema de encaminhamentos.
"""

    email = EmailMessage(
        subject='Novo Encaminhamento Recebido',
        body=corpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ENCAMINHAMENTO_EMAIL_DESTINO],
    )

    try:
        email.attach_file(encaminhamento.docx_gerado.path)
        email.send(fail_silently=False)
    except Exception:
        logger.exception(
            'Erro ao enviar email do encaminhamento %s.',
            encaminhamento.pk
        )
        return False

    encaminhamento.__class__.objects.filter(pk=encaminhamento.pk).update(
        email_enviado=True
    )
    encaminhamento.email_enviado = True
    return True


def enviar_email_lote_encaminhamentos(encaminhamentos):
    encaminhamentos = list(encaminhamentos)

    if not encaminhamentos:
        return False

    primeiro = encaminhamentos[0]
    total = len(encaminhamentos)
    resumo_colaboradores = []

    for indice, encaminhamento in enumerate(encaminhamentos, start=1):
        resumo_colaboradores.append(
            '\n'.join([
                f'{indice}. {encaminhamento.nome}',
                f'   CPF: {encaminhamento.cpf}',
                f'   Função: {encaminhamento.funcao}',
                f'   Setor: {encaminhamento.setor}',
                f'   Tipo de exame: {encaminhamento.get_tipo_exame_display()}',
            ])
        )

    corpo = f"""Olá,

Um novo lote de encaminhamentos foi realizado através do sistema.

Empresa: {primeiro.empresa}
CNPJ: {primeiro.cnpj or '-'}
Emitente: {primeiro.nome_emitente or '-'}
Telefone: {primeiro.telefone}
Data do encaminhamento: {_formatar_data(primeiro.data_encaminhamento)}
Total de colaboradores: {total}

Colaboradores:

{chr(10).join(resumo_colaboradores)}

Os documentos de encaminhamento seguem anexados neste email.

Mensagem automática do sistema de encaminhamentos.
"""

    email = EmailMessage(
        subject=f'Novo lote de encaminhamentos recebido - {primeiro.empresa}',
        body=corpo,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ENCAMINHAMENTO_EMAIL_DESTINO],
    )

    try:
        for encaminhamento in encaminhamentos:
            if encaminhamento.docx_gerado:
                email.attach_file(encaminhamento.docx_gerado.path)
        email.send(fail_silently=False)
    except Exception:
        logger.exception(
            'Erro ao enviar email do lote de encaminhamentos da empresa %s.',
            primeiro.empresa,
        )
        return False

    ids = [encaminhamento.pk for encaminhamento in encaminhamentos]
    primeiro.__class__.objects.filter(pk__in=ids).update(email_enviado=True)

    for encaminhamento in encaminhamentos:
        encaminhamento.email_enviado = True

    return True

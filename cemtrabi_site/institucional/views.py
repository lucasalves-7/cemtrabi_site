import logging
from urllib.parse import quote

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .forms import (
    EncaminhamentoColaboradorFormSet,
    EncaminhamentoEmpresaForm,
    LeadForm,
)
from .models import Encaminhamento, Lead
from .services import gerar_docx_encaminhamento, enviar_email_lote_encaminhamentos


logger = logging.getLogger(__name__)


EXAMES_ENCAMINHAMENTO = [
    'exame_clinico',
    'audiometria',
    'acuidade_visual',
    'eletrocardiograma',
    'eletroencefalograma',
    'espirometria',
    'avaliacao_psicossocial',
    'raio_x_torax',
    'teste_romberg',
    'hemograma',
    'glicemia',
    'acido_hipurico',
    'acido_metil_hipurico',
    'grupo_sanguineo_fator_rh',
    'outro_exame',
]


def home(request):
    return render(request, 'home.html')


def medicina(request):
    return render(request, 'medicina.html')


def seguranca(request):
    return render(request, 'seguranca.html')


def treinamentos(request):
    return render(request, 'treinamentos.html')


def contato(request):
    servico_preselecionado = request.GET.get('servico')

    if request.method == 'POST':
        form = LeadForm(request.POST)

        if form.is_valid():
            cnpj = form.cleaned_data.get('cnpj')

            if cnpj and Lead.objects.filter(cnpj=cnpj).exists():
                messages.error(
                    request,
                    'Já recebemos uma solicitação com este CNPJ. '
                    'Por favor, aguarde que nossa equipe entrará em contato.'
                )
                return render(request, 'contato.html', {'form': form})

            lead = form.save(commit=False)
            lead.origem = 'formulario_site'

            try:
                lead.save()
            except IntegrityError:
                messages.error(
                    request,
                    'Já recebemos uma solicitação com este CNPJ. '
                    'Por favor, aguarde que nossa equipe entrará em contato.'
                )
                return render(request, 'contato.html', {'form': form})

            messages.success(
                request,
                'Recebemos seu contato! Nossa equipe retornará em breve.'
            )
            return redirect('contato')

        messages.error(
            request,
            'Não foi possível enviar sua solicitação. '
            'Verifique os campos destacados e tente novamente.'
        )
    else:
        form = LeadForm(initial={'servico': servico_preselecionado})

    return render(request, 'contato.html', {'form': form})


def encaminhamento(request):
    def normalizar_formularios_vazios(dados, arquivos):
        dados_normalizados = dados.copy()

        try:
            total_formularios = int(dados.get('colaboradores-TOTAL_FORMS', 0))
        except (TypeError, ValueError):
            return dados_normalizados
        total_formularios = max(0, min(total_formularios, 2000))

        campos_ignorados = {
            'DELETE',
            'tipo_exame',
            'copiar_de_indice',
            'anexar_pcmso',
        }

        for indice in range(total_formularios):
            prefixo = f'colaboradores-{indice}-'
            possui_dados = any(
                chave.startswith(prefixo)
                and chave.removeprefix(prefixo) not in campos_ignorados
                and bool(dados.get(chave))
                for chave in dados
            )
            possui_arquivo = any(
                chave.startswith(prefixo) and bool(arquivos.get(chave))
                for chave in arquivos
            )

            if not possui_dados and not possui_arquivo:
                dados_normalizados[f'{prefixo}DELETE'] = 'on'

        return dados_normalizados

    def colaborador_esta_vazio(colaborador_form):
        campos_ignorados = {
            'DELETE',
            'tipo_exame',
            'copiar_de_indice',
            'anexar_pcmso',
        }

        for campo_nome in colaborador_form.fields:
            if campo_nome in campos_ignorados:
                continue

            valor = colaborador_form[campo_nome].value()
            if valor not in (None, '', False, [], ()):
                return False

        return True

    def montar_colaborador_forms(formset):
        exames_nomes = [nome for nome in EXAMES_ENCAMINHAMENTO if nome != 'outro_exame']
        return [
            {
                'form': colaborador_form,
                'exames_fields': [colaborador_form[nome] for nome in exames_nomes],
                'descartado': (
                    bool(colaborador_form['DELETE'].value())
                    or (
                        colaborador_form.is_bound
                        and colaborador_esta_vazio(colaborador_form)
                    )
                ),
            }
            for colaborador_form in formset
        ]

    def montar_resumo_erros(empresa_form, colaborador_formset):
        resumo = []

        for campo_nome, mensagens in empresa_form.errors.items():
            campo = empresa_form.fields.get(campo_nome)
            rotulo = campo.label if campo else 'Dados da empresa'
            resumo.extend(f'{rotulo}: {mensagem}' for mensagem in mensagens)

        for posicao, colaborador_form in enumerate(colaborador_formset, start=1):
            if (
                colaborador_form.cleaned_data.get('DELETE')
                or colaborador_esta_vazio(colaborador_form)
            ):
                continue

            for campo_nome, mensagens in colaborador_form.errors.items():
                campo = colaborador_form.fields.get(campo_nome)
                rotulo = campo.label if campo else 'Dados do colaborador'
                resumo.extend(
                    f'{rotulo} do colaborador {posicao}: {mensagem}'
                    for mensagem in mensagens
                )

        resumo.extend(str(mensagem) for mensagem in colaborador_formset.non_form_errors())
        return resumo

    def marcar_campos_invalidos(formulario):
        for campo_nome in formulario.errors:
            campo = formulario.fields.get(campo_nome)
            if not campo:
                continue
            classes = campo.widget.attrs.get('class', '').split()
            if 'is-invalid' not in classes:
                classes.append('is-invalid')
            campo.widget.attrs['class'] = ' '.join(classes)

    erros_resumo = []

    if request.method == 'POST':
        empresa_form = EncaminhamentoEmpresaForm(request.POST)
        dados_colaboradores = normalizar_formularios_vazios(
            request.POST,
            request.FILES,
        )
        colaborador_formset = EncaminhamentoColaboradorFormSet(
            dados_colaboradores,
            request.FILES,
            prefix='colaboradores',
        )
        erro_exibido = False
        empresa_valida = empresa_form.is_valid()
        colaboradores_validos = colaborador_formset.is_valid()

        if empresa_valida and colaboradores_validos:
            empresa_data = empresa_form.cleaned_data.copy()
            empresa_data.pop('aceite_privacidade', None)
            encaminhamentos_salvos = []
            colaboradores_processados = {}

            for indice, colaborador_form in enumerate(colaborador_formset):
                if (
                    colaborador_form.cleaned_data.get('DELETE')
                    or not colaborador_form.cleaned_data.get('nome')
                ):
                    continue

                colaborador_data = colaborador_form.cleaned_data.copy()
                colaborador_data.pop('DELETE', None)
                copiar_de_indice = colaborador_data.pop('copiar_de_indice', None)
                colaborador_data.pop('anexar_pcmso', None)

                colaborador_referencia = colaboradores_processados.get(copiar_de_indice)

                if colaborador_referencia:
                    colaborador_data['riscos_ocupacionais'] = (
                        colaborador_referencia.get('riscos_ocupacionais') or ''
                    )
                    for exame_nome in EXAMES_ENCAMINHAMENTO:
                        colaborador_data[exame_nome] = colaborador_referencia.get(exame_nome)
                    colaborador_data['descricao_outro_exame'] = (
                        colaborador_referencia.get('descricao_outro_exame') or ''
                    )

                encaminhamento = Encaminhamento(
                    **empresa_data,
                    **colaborador_data,
                )
                encaminhamento._ignorar_geracao_docx = True
                encaminhamento.save()
                gerar_docx_encaminhamento(encaminhamento)
                encaminhamentos_salvos.append(encaminhamento)
                colaboradores_processados[indice] = colaborador_data.copy()

            if not encaminhamentos_salvos:
                messages.error(
                    request,
                    'Adicione pelo menos um colaborador para enviar o encaminhamento.'
                )
                erro_exibido = True
            else:
                email_enviado = enviar_email_lote_encaminhamentos(encaminhamentos_salvos)
                total_colaboradores = len(encaminhamentos_salvos)
                primeiro_encaminhamento = encaminhamentos_salvos[0]
                data_formatada = primeiro_encaminhamento.data_encaminhamento.strftime('%d/%m/%Y')
                mensagem_whatsapp = (
                    'Olá, eu acabei de solicitar encaminhamento para '
                    f'{total_colaboradores} colaborador(es) pela empresa '
                    f'{primeiro_encaminhamento.empresa} no dia {data_formatada}.'
                )
                request.session['encaminhamento_sucesso'] = {
                    'nome': primeiro_encaminhamento.nome,
                    'empresa': primeiro_encaminhamento.empresa,
                    'total_colaboradores': total_colaboradores,
                    'email_enviado': email_enviado,
                    'whatsapp_url': f'https://wa.me/5521975204123?text={quote(mensagem_whatsapp)}',
                }
                return redirect('encaminhamento')

        erros_resumo = montar_resumo_erros(empresa_form, colaborador_formset)
        marcar_campos_invalidos(empresa_form)
        for colaborador_form in colaborador_formset:
            marcar_campos_invalidos(colaborador_form)

        logger.warning(
            'Encaminhamento inválido. Erros: %s',
            erros_resumo,
        )

        if not erro_exibido:
            messages.error(
                request,
                'Não foi possível enviar o encaminhamento. Verifique os campos destacados.'
            )
    else:
        empresa_form = EncaminhamentoEmpresaForm()
        colaborador_formset = EncaminhamentoColaboradorFormSet(
            prefix='colaboradores',
            initial=[{}],
        )

    sucesso_modal = request.session.pop('encaminhamento_sucesso', None)

    return render(request, 'encaminhamento.html', {
        'empresa_form': empresa_form,
        'colaborador_formset': colaborador_formset,
        'colaborador_forms': montar_colaborador_forms(colaborador_formset),
        'empty_colaborador_form': montar_colaborador_forms([colaborador_formset.empty_form])[0],
        'sucesso_modal': sucesso_modal,
        'erros_resumo': erros_resumo,
    })


def sobre(request):
    return render(request, 'sobre.html')


def politica_privacidade(request):
    return render(request, 'politica_privacidade.html')

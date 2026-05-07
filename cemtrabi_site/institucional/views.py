from django.shortcuts import render, redirect
from django.contrib import messages
from urllib.parse import quote

from .forms import EncaminhamentoForm, LeadForm
from .models import Lead


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

            # 🔒 BLOQUEIO POR CNPJ
            if cnpj and Lead.objects.filter(cnpj=cnpj).exists():
                messages.error(
                    request,
                    'Já recebemos uma solicitação com este CNPJ. '
                    'Por favor, aguarde que nossa equipe entrará em contato.'
                )
                # ⚠️ NÃO REDIRECIONA
                return render(request, 'contato.html', {'form': form})

            lead = form.save(commit=False)
            lead.origem = 'formulario_site'
            lead.save()

            messages.success(
                request,
                'Recebemos seu contato! Nossa equipe retornará em breve.'
            )

            # ✅ REDIRECIONA APENAS NO SUCESSO
            return redirect('contato')

        else:
            # ❌ FORM INVÁLIDO (campos vazios, email errado etc)
            messages.error(
                request,
                'Já recebemos uma solicitação com este CNPJ. '
                'Por favor, aguarde que nossa equipe entrará em contato.'
            )

    else:
        form = LeadForm(initial={'servico': servico_preselecionado})

    return render(request, 'contato.html', {'form': form})


def encaminhamento(request):
    if request.method == 'POST':
        form = EncaminhamentoForm(request.POST, request.FILES)

        if form.is_valid():
            encaminhamento_salvo = form.save()
            data_formatada = encaminhamento_salvo.data_encaminhamento.strftime('%d/%m/%Y')
            mensagem_whatsapp = (
                'Olá, eu acabei de solicitar um encaminhamento para o colaborador '
                f'{encaminhamento_salvo.nome} pela empresa {encaminhamento_salvo.empresa} '
                f'no dia {data_formatada}.'
            )
            request.session['encaminhamento_sucesso'] = {
                'nome': encaminhamento_salvo.nome,
                'empresa': encaminhamento_salvo.empresa,
                'whatsapp_url': f'https://wa.me/5521975204123?text={quote(mensagem_whatsapp)}',
            }
            return redirect('encaminhamento')

        messages.error(
            request,
            'Não foi possível enviar o encaminhamento. Verifique os campos destacados.'
        )
    else:
        form = EncaminhamentoForm()

    sucesso_modal = request.session.pop('encaminhamento_sucesso', None)

    exames_fields = [
        form['exame_clinico'],
        form['audiometria'],
        form['acuidade_visual'],
        form['eletrocardiograma'],
        form['eletroencefalograma'],
        form['espirometria'],
        form['avaliacao_psicossocial'],
        form['raio_x_torax'],
        form['teste_romberg'],
        form['hemograma'],
        form['glicemia'],
        form['acido_hipurico'],
        form['acido_metil_hipurico'],
        form['grupo_sanguineo_fator_rh'],
    ]

    return render(request, 'encaminhamento.html', {
        'form': form,
        'exames_fields': exames_fields,
        'sucesso_modal': sucesso_modal,
    })


def sobre(request):
    return render(request, 'sobre.html')


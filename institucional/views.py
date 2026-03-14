from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LeadForm
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


def sobre(request):
    return render(request, 'sobre.html')


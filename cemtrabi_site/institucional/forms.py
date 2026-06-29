from pathlib import Path

from django import forms
from django.forms import formset_factory

from .models import Encaminhamento, Lead


ASSINATURAS_PCMSO = {
    '.pdf': [b'%PDF'],
    '.jpg': [b'\xff\xd8\xff'],
    '.jpeg': [b'\xff\xd8\xff'],
    '.png': [b'\x89PNG\r\n\x1a\n'],
}


def somente_digitos(valor):
    return ''.join(filter(str.isdigit, valor or ''))


def validar_assinatura_arquivo(arquivo):
    extensao = Path(arquivo.name).suffix.lower()
    assinaturas_esperadas = ASSINATURAS_PCMSO.get(extensao)

    if not assinaturas_esperadas:
        raise forms.ValidationError('Arquivo inválido. Envie apenas PDF, JPG, JPEG ou PNG.')

    posicao_atual = arquivo.tell()
    cabecalho = arquivo.read(12)
    arquivo.seek(posicao_atual)

    if not any(cabecalho.startswith(assinatura) for assinatura in assinaturas_esperadas):
        raise forms.ValidationError(
            'O conteúdo do arquivo não corresponde ao formato enviado. '
            'Envie um PDF ou imagem válida.'
        )


class LeadForm(forms.ModelForm):

    class Meta:
        model = Lead
        fields = [
            'empresa',
            'cnpj',
            'responsavel',
            'email',
            'telefone',
            'servico',
            'mensagem',
        ]

        labels = {
            'empresa': 'Empresa',
            'cnpj': 'CNPJ',
            'responsavel': 'Responsável',
            'email': 'E-mail',
            'telefone': 'Telefone / WhatsApp',
            'servico': 'Serviço desejado',
            'mensagem': 'Mensagem',
        }

        widgets = {
            'empresa': forms.TextInput(attrs={
                'placeholder': 'Nome da empresa',
            }),
            'cnpj': forms.TextInput(attrs={
                'placeholder': '00.000.000/0000-00',
                'inputmode': 'numeric',
            }),
            'responsavel': forms.TextInput(attrs={
                'placeholder': 'Nome do responsável',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'email@empresa.com',
            }),
            'telefone': forms.TextInput(attrs={
                'placeholder': '(00) 00000-0000',
                'inputmode': 'numeric',
            }),
            'servico': forms.Select(),
            'mensagem': forms.Textarea(attrs={
                'placeholder': 'Deixe sua mensagem aqui...',
                'rows': 5,
            }),
        }

    def clean_empresa(self):
        return self.cleaned_data['empresa'].strip()

    def clean_responsavel(self):
        return self.cleaned_data['responsavel'].strip()

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj', '').strip()
        cnpj_limpo = somente_digitos(cnpj)

        if len(cnpj_limpo) != 14:
            raise forms.ValidationError('Informe um CNPJ válido com 14 dígitos.')

        leads = Lead.objects.only('id', 'cnpj')
        if self.instance.pk:
            leads = leads.exclude(pk=self.instance.pk)

        if any(somente_digitos(lead.cnpj) == cnpj_limpo for lead in leads):
            raise forms.ValidationError(
                'Este CNPJ já possui uma solicitação cadastrada. '
                'Por gentileza, aguarde o contato da nossa equipe.'
            )

        return cnpj_limpo

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').strip()
        telefone_limpo = somente_digitos(telefone)

        if len(telefone_limpo) < 10:
            raise forms.ValidationError('Informe um telefone válido com DDD.')

        return telefone


class EncaminhamentoForm(forms.ModelForm):
    aceite_privacidade = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'É necessário confirmar a autorização e aceitar a Política de Privacidade.'
        }
    )

    tipo_exame = forms.ChoiceField(choices=[
        ('admissional', 'Admissional'),
        ('demissional', 'Demissional'),
        ('periodico', 'Periódico'),
        ('retorno_trabalho', 'Retorno ao trabalho'),
        ('mudanca_funcao', 'Mudança de função'),
    ])

    class Meta:
        model = Encaminhamento
        fields = [
            'cnpj',
            'empresa',
            'endereco_empresa',
            'nome_emitente',
            'telefone',
            'data_encaminhamento',
            'tipo_exame',
            'nome',
            'data_nascimento',
            'data_admissao',
            'rg',
            'cpf',
            'funcao',
            'setor',
            'riscos_ocupacionais',
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
            'descricao_outro_exame',
            'pcmso',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={
                'placeholder': '000.000.000-00',
                'inputmode': 'numeric',
            }),
            'rg': forms.TextInput(attrs={'placeholder': 'RG'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'data_encaminhamento': forms.DateInput(attrs={'type': 'date'}),
            'telefone': forms.TextInput(attrs={
                'placeholder': '(00) 00000-0000',
                'inputmode': 'numeric',
            }),
            'empresa': forms.TextInput(attrs={'placeholder': 'Nome da empresa'}),
            'cnpj': forms.TextInput(attrs={
                'placeholder': '00.000.000/0000-00',
                'inputmode': 'numeric',
            }),
            'nome_emitente': forms.TextInput(attrs={'placeholder': 'Nome do emitente'}),
            'endereco_empresa': forms.TextInput(attrs={'placeholder': 'Endereço da empresa'}),
            'funcao': forms.TextInput(attrs={'placeholder': 'Função'}),
            'setor': forms.TextInput(attrs={'placeholder': 'Setor'}),
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
            'tipo_exame': forms.Select(),
            'riscos_ocupacionais': forms.Textarea(attrs={
                'placeholder': 'Informe os riscos ocupacionais',
                'rows': 4,
            }),
            'descricao_outro_exame': forms.TextInput(attrs={
                'placeholder': 'Informe o exame personalizado',
            }),
            'pcmso': forms.FileInput(attrs={
                'accept': '.pdf,.jpg,.jpeg,.png',
            }),
        }

        labels = {
            'audiometria': 'Audiometria tonal',
            'hemograma': 'Hemograma completo com plaquetas',
            'glicemia': 'Glicemia em jejum',
            'raio_x_torax': 'Raio X tórax padrão OIT',
            'teste_romberg': 'Teste de equilíbrio/Romberg',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pcmso'].required = False

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj', '').strip()

        if not cnpj:
            return cnpj

        cnpj_limpo = somente_digitos(cnpj)
        if len(cnpj_limpo) != 14:
            raise forms.ValidationError('Informe um CNPJ válido com 14 dígitos.')

        return cnpj

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '').strip()
        cpf_limpo = somente_digitos(cpf)

        if len(cpf_limpo) != 11:
            raise forms.ValidationError('Informe um CPF válido com 11 dígitos.')

        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').strip()
        telefone_limpo = somente_digitos(telefone)

        if len(telefone_limpo) < 10:
            raise forms.ValidationError('Informe um telefone válido com DDD.')

        return telefone

    def clean_pcmso(self):
        arquivo = self.cleaned_data.get('pcmso')

        if arquivo:
            validar_assinatura_arquivo(arquivo)

        return arquivo


class EncaminhamentoEmpresaForm(forms.Form):
    cnpj = forms.CharField(
        label='CNPJ',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '00.000.000/0000-00',
            'inputmode': 'numeric',
        }),
    )
    empresa = forms.CharField(
        label='Empresa',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nome da empresa'}),
    )
    endereco_empresa = forms.CharField(
        label='Endereço da empresa',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Endereço da empresa'}),
    )
    nome_emitente = forms.CharField(
        label='Nome do emitente',
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Nome do emitente'}),
    )
    telefone = forms.CharField(
        label='Telefone',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '(00) 00000-0000',
            'inputmode': 'numeric',
        }),
    )
    data_encaminhamento = forms.DateField(
        label='Data do encaminhamento',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    aceite_privacidade = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'É necessário confirmar a autorização e aceitar a Política de Privacidade.'
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.errors:
            field = self.fields.get(field_name)
            if not field:
                continue
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_class} is-invalid'.strip()

    def clean_empresa(self):
        return self.cleaned_data['empresa'].strip()

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj', '').strip()

        if not cnpj:
            return cnpj

        cnpj_limpo = somente_digitos(cnpj)
        if len(cnpj_limpo) != 14:
            raise forms.ValidationError('Informe um CNPJ válido com 14 dígitos.')

        return cnpj

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').strip()
        telefone_limpo = somente_digitos(telefone)

        if len(telefone_limpo) < 10:
            raise forms.ValidationError('Informe um telefone válido com DDD.')

        return telefone


class EncaminhamentoColaboradorForm(forms.ModelForm):
    copiar_de_indice = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )
    anexar_pcmso = forms.BooleanField(
        label='Deseja anexar um novo PCMSO?',
        required=False,
    )
    tipo_exame = forms.ChoiceField(choices=[
        ('admissional', 'Admissional'),
        ('demissional', 'Demissional'),
        ('periodico', 'Periódico'),
        ('retorno_trabalho', 'Retorno ao trabalho'),
        ('mudanca_funcao', 'Mudança de função'),
    ])

    class Meta:
        model = Encaminhamento
        fields = [
            'tipo_exame',
            'nome',
            'data_nascimento',
            'data_admissao',
            'rg',
            'cpf',
            'funcao',
            'setor',
            'riscos_ocupacionais',
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
            'descricao_outro_exame',
            'pcmso',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={
                'placeholder': '000.000.000-00',
                'inputmode': 'numeric',
            }),
            'rg': forms.TextInput(attrs={'placeholder': 'RG'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'funcao': forms.TextInput(attrs={'placeholder': 'Função'}),
            'setor': forms.TextInput(attrs={'placeholder': 'Setor'}),
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
            'tipo_exame': forms.Select(),
            'riscos_ocupacionais': forms.Textarea(attrs={
                'placeholder': 'Informe os riscos ocupacionais',
                'rows': 4,
            }),
            'descricao_outro_exame': forms.TextInput(attrs={
                'placeholder': 'Informe o exame personalizado',
            }),
            'pcmso': forms.FileInput(attrs={
                'accept': '.pdf,.jpg,.jpeg,.png',
            }),
        }

        labels = {
            'audiometria': 'Audiometria tonal',
            'hemograma': 'Hemograma completo com plaquetas',
            'glicemia': 'Glicemia em jejum',
            'raio_x_torax': 'Raio X tórax padrão OIT',
            'teste_romberg': 'Teste de equilíbrio/Romberg',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pcmso'].required = False

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf', '').strip()
        cpf_limpo = somente_digitos(cpf)

        if len(cpf_limpo) != 11:
            raise forms.ValidationError('Informe um CPF válido com 11 dígitos.')

        return cpf

    def clean_pcmso(self):
        arquivo = self.cleaned_data.get('pcmso')

        if arquivo:
            validar_assinatura_arquivo(arquivo)

        return arquivo

    def clean_copiar_de_indice(self):
        valor = self.cleaned_data.get('copiar_de_indice', '').strip()

        if not valor:
            return None

        try:
            indice_referencia = int(valor)
            indice_atual = int(self.prefix.rsplit('-', 1)[-1])
        except (TypeError, ValueError):
            return None

        if indice_referencia < 0 or indice_referencia >= indice_atual:
            return None

        return indice_referencia

    def clean(self):
        cleaned_data = super().clean()
        anexar_pcmso = cleaned_data.get('anexar_pcmso')

        if not anexar_pcmso:
            cleaned_data['pcmso'] = None

        return cleaned_data


EncaminhamentoColaboradorFormSet = formset_factory(
    EncaminhamentoColaboradorForm,
    can_delete=True,
    extra=0,
    min_num=1,
    validate_min=True,
)

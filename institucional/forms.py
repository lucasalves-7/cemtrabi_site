from django import forms
from .models import Lead


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

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')

        # Remove máscara para comparar corretamente
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

        if Lead.objects.filter(cnpj__icontains=cnpj_limpo).exists():
            raise forms.ValidationError(
                'Este CNPJ já possui uma solicitação cadastrada. '
                'Por gentileza, aguarde o contato da nossa equipe.'
            )

        return cnpj


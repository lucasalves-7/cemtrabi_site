from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import Encaminhamento


class EncaminhamentoMultiplosColaboradoresTests(TestCase):
    @patch('institucional.views.enviar_email_lote_encaminhamentos', return_value=True)
    @patch('institucional.views.gerar_docx_encaminhamento')
    def test_copia_dados_da_referencia_escolhida(
        self,
        gerar_docx_mock,
        enviar_email_mock,
    ):
        dados = {
            'empresa': 'Empresa Teste',
            'telefone': '(21) 99999-9999',
            'data_encaminhamento': '2026-06-29',
            'aceite_privacidade': 'on',
            'colaboradores-TOTAL_FORMS': '5',
            'colaboradores-INITIAL_FORMS': '0',
            'colaboradores-MIN_NUM_FORMS': '1',
            'colaboradores-MAX_NUM_FORMS': '1000',
        }
        funcoes = [
            'Auxiliar de serviços gerais',
            'Auxiliar de serviços gerais',
            'Auxiliar de serviços gerais',
            'Operador de caixa',
            'Operador de caixa',
        ]
        riscos = ['Ruído', 'ignorar', 'ignorar', 'Ergonômico', 'incorreto']

        for indice in range(5):
            prefixo = f'colaboradores-{indice}-'
            dados.update({
                f'{prefixo}nome': f'Pessoa {indice + 1}',
                f'{prefixo}cpf': f'0000000000{indice}',
                f'{prefixo}rg': f'10000000{indice}',
                f'{prefixo}data_nascimento': '1990-01-01',
                f'{prefixo}funcao': funcoes[indice],
                f'{prefixo}setor': 'Operação',
                f'{prefixo}data_admissao': '2026-01-01',
                f'{prefixo}tipo_exame': 'periodico',
                f'{prefixo}riscos_ocupacionais': riscos[indice],
            })

        dados.update({
            'colaboradores-0-copiar_de_indice': '0',
            'colaboradores-0-exame_clinico': 'on',
            'colaboradores-1-copiar_de_indice': '0',
            'colaboradores-2-copiar_de_indice': '0',
            'colaboradores-3-audiometria': 'on',
            'colaboradores-4-copiar_de_indice': '3',
            'colaboradores-4-anexar_pcmso': 'on',
        })

        resposta = self.client.post(reverse('encaminhamento'), dados)

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Encaminhamento.objects.count(), 5)

        ultimo_colaborador = Encaminhamento.objects.get(nome='Pessoa 5')
        self.assertEqual(ultimo_colaborador.riscos_ocupacionais, 'Ergonômico')
        self.assertTrue(ultimo_colaborador.audiometria)
        self.assertFalse(ultimo_colaborador.exame_clinico)
        self.assertEqual(gerar_docx_mock.call_count, 5)
        enviar_email_mock.assert_called_once()

    @patch('institucional.views.enviar_email_lote_encaminhamentos', return_value=True)
    @patch('institucional.views.gerar_docx_encaminhamento')
    def test_formulario_pode_ser_corrigido_e_enviado_apos_erro(
        self,
        gerar_docx_mock,
        enviar_email_mock,
    ):
        dados = {
            'empresa': 'Empresa Teste',
            'telefone': '(21) 99999-9999',
            'data_encaminhamento': '2026-06-29',
            'aceite_privacidade': 'on',
            'colaboradores-TOTAL_FORMS': '4',
            'colaboradores-INITIAL_FORMS': '0',
            'colaboradores-MIN_NUM_FORMS': '1',
            'colaboradores-MAX_NUM_FORMS': '1000',
            'colaboradores-2-DELETE': 'on',
            'colaboradores-3-DELETE': 'on',
        }

        for indice in range(2):
            prefixo = f'colaboradores-{indice}-'
            dados.update({
                f'{prefixo}nome': f'Pessoa {indice + 1}',
                f'{prefixo}cpf': '123' if indice == 1 else '00000000000',
                f'{prefixo}rg': f'10000000{indice}',
                f'{prefixo}data_nascimento': '1990-01-01',
                f'{prefixo}funcao': 'Operador de caixa',
                f'{prefixo}setor': 'Operação',
                f'{prefixo}data_admissao': '2026-01-01',
                f'{prefixo}tipo_exame': 'periodico',
                f'{prefixo}riscos_ocupacionais': 'Ergonômico',
            })

        resposta = self.client.post(reverse('encaminhamento'), dados)
        html = resposta.content.decode()

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(html.count('data-deleted="true" hidden'), 2)
        self.assertIn('CPF do colaborador 2', html)
        self.assertNotIn('data-add-colaborador-mesma-funcao', html)
        self.assertNotIn('copiar_riscos_primeiro', html)
        self.assertNotIn('copiar_exames_primeiro', html)

        dados['colaboradores-1-cpf'] = '11111111111'
        dados.pop('colaboradores-2-DELETE')
        dados.pop('colaboradores-3-DELETE')
        dados['colaboradores-2-tipo_exame'] = 'admissional'
        dados['colaboradores-3-tipo_exame'] = 'admissional'
        resposta_corrigida = self.client.post(reverse('encaminhamento'), dados)

        self.assertEqual(resposta_corrigida.status_code, 302)
        self.assertEqual(Encaminhamento.objects.count(), 2)
        self.assertEqual(gerar_docx_mock.call_count, 2)
        enviar_email_mock.assert_called_once()

import logging

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


MAX_PCMSO_SIZE = 10 * 1024 * 1024
logger = logging.getLogger(__name__)


def validar_tamanho_pcmso(arquivo):
    if arquivo.size > MAX_PCMSO_SIZE:
        raise ValidationError('Arquivo muito grande. O tamanho máximo permitido é 10MB.')


class Lead(models.Model):
    """
    Model responsável por armazenar os contatos (leads)
    enviados pelo site institucional da CEMTRABI.
    """

    # ===============================
    # CHOICES
    # ===============================
    SERVICOS = [
        ('medicina', 'Medicina Ocupacional'),
        ('seguranca', 'Segurança do Trabalho'),
        ('treinamentos', 'Treinamentos'),
    ]

    STATUS = [
        ('novo', 'Novo'),
        ('contato', 'Em contato'),
        ('orcamento', 'Orçamento enviado'),
        ('fechado', 'Fechado'),
    ]

    # ===============================
    # DADOS DA EMPRESA
    # ===============================
    empresa = models.CharField(
        max_length=150,
        verbose_name='Empresa'
    )

    # ⚠️ CNPJ ÚNICO → TRAVA DEFINITIVA CONTRA DUPLICAÇÃO
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name='CNPJ'
    )

    # ===============================
    # RESPONSÁVEL
    # ===============================
    responsavel = models.CharField(
        max_length=150,
        verbose_name='Responsável'
    )

    email = models.EmailField(
        verbose_name='E-mail'
    )

    telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone'
    )

    # ===============================
    # SERVIÇO
    # ===============================
    servico = models.CharField(
        max_length=20,
        choices=SERVICOS,
        verbose_name='Serviço'
    )

    # ===============================
    # MENSAGEM
    # ===============================
    mensagem = models.TextField(
        blank=True,
        verbose_name='Mensagem'
    )

    # ===============================
    # CONTROLE INTERNO
    # ===============================
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='novo',
        verbose_name='Status'
    )

    origem = models.CharField(
        max_length=50,
        default='site',
        verbose_name='Origem'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de criação'
    )

    # ===============================
    # REPRESENTAÇÃO
    # ===============================
    def __str__(self):
        return f"{self.empresa} - {self.cnpj}"


class Encaminhamento(models.Model):
    TIPO_EXAME_CHOICES = [
        ('admissional', 'Admissional'),
        ('periodico', 'Periódico'),
        ('demissional', 'Demissional'),
        ('retorno_trabalho', 'Retorno ao trabalho'),
        ('mudanca_funcao', 'Mudança de função'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('recebido', 'Recebido'),
        ('agendado', 'Agendado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    nome = models.CharField(max_length=150, verbose_name='Nome')
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    rg = models.CharField(max_length=20, verbose_name='RG')
    data_nascimento = models.DateField(verbose_name='Data de nascimento')
    idade = models.PositiveIntegerField(null=True, blank=True, editable=False, verbose_name='Idade')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    empresa = models.CharField(max_length=150, verbose_name='Empresa')
    cnpj = models.CharField(max_length=18, blank=True, verbose_name='CNPJ')
    nome_emitente = models.CharField(max_length=150, blank=True, verbose_name='Nome do emitente')
    endereco_empresa = models.CharField(max_length=255, blank=True, verbose_name='Endereço da empresa')
    funcao = models.CharField(max_length=120, verbose_name='Função')
    data_encaminhamento = models.DateField(default=timezone.localdate, verbose_name='Data do encaminhamento')
    setor = models.CharField(max_length=120, verbose_name='Setor')
    data_admissao = models.DateField(verbose_name='Data de admissão')
    riscos_ocupacionais = models.TextField(blank=True, verbose_name='Riscos ocupacionais')
    tipo_exame = models.CharField(
        max_length=30,
        choices=TIPO_EXAME_CHOICES,
        verbose_name='Tipo de exame'
    )
    exame_clinico = models.BooleanField(default=False, verbose_name='Exame clínico')
    audiometria = models.BooleanField(default=False, verbose_name='Audiometria tonal')
    hemograma = models.BooleanField(default=False, verbose_name='Hemograma completo com plaquetas')
    glicemia = models.BooleanField(default=False, verbose_name='Glicemia em jejum')
    acuidade_visual = models.BooleanField(default=False, verbose_name='Acuidade visual')
    eletrocardiograma = models.BooleanField(default=False, verbose_name='Eletrocardiograma')
    eletroencefalograma = models.BooleanField(default=False, verbose_name='Eletroencefalograma')
    espirometria = models.BooleanField(default=False, verbose_name='Espirometria')
    avaliacao_psicossocial = models.BooleanField(default=False, verbose_name='Avaliação psicossocial')
    raio_x_torax = models.BooleanField(default=False, verbose_name='Raio X tórax padrão OIT')
    teste_romberg = models.BooleanField(default=False, verbose_name='Teste de equilíbrio/Romberg')
    acido_hipurico = models.BooleanField(default=False, verbose_name='Ácido hipúrico')
    acido_metil_hipurico = models.BooleanField(default=False, verbose_name='Ácido metil hipúrico')
    grupo_sanguineo_fator_rh = models.BooleanField(default=False, verbose_name='Grupo sanguíneo/fator RH')
    outro_exame = models.BooleanField(default=False, verbose_name='Outro exame')
    descricao_outro_exame = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Descrição do outro exame'
    )
    pcmso = models.FileField(
        upload_to='encaminhamentos/pcmso/',
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'],
                message='Arquivo inválido. Envie apenas PDF, JPG, JPEG ou PNG.'
            ),
            validar_tamanho_pcmso,
        ],
        verbose_name='PCMSO'
    )
    docx_gerado = models.FileField(
        upload_to='encaminhamentos/docx/',
        blank=True,
        null=True,
        verbose_name='Documento DOCX gerado'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name='Status'
    )
    email_enviado = models.BooleanField(default=False, verbose_name='E-mail enviado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Encaminhamento'
        verbose_name_plural = 'Encaminhamentos'
        ordering = ['-created_at']

    def calcular_idade(self):
        hoje = timezone.localdate()
        idade = hoje.year - self.data_nascimento.year
        fez_aniversario = (hoje.month, hoje.day) >= (
            self.data_nascimento.month,
            self.data_nascimento.day,
        )
        return idade if fez_aniversario else idade - 1

    def save(self, *args, **kwargs):
        criando = self.pk is None

        if self.data_nascimento:
            self.idade = self.calcular_idade()
        super().save(*args, **kwargs)

        if not getattr(self, '_ignorar_geracao_docx', False):
            from .services import gerar_docx_encaminhamento, enviar_email_encaminhamento

            try:
                gerar_docx_encaminhamento(self)
            except Exception:
                logger.exception(
                    'Erro ao gerar DOCX do encaminhamento %s.',
                    self.pk
                )
                return

            if criando and self.docx_gerado:
                enviar_email_encaminhamento(self)

    def __str__(self):
        return f"{self.nome} - {self.empresa}"
    

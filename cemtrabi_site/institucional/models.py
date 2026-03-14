from django.db import models


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
    

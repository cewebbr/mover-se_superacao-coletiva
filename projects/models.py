import datetime
from datetime import datetime as dt

from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField


class Project(TimeStampedModel, models.Model):
    owner = models.ForeignKey(
        verbose_name="Proprietário",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    image = models.ImageField(verbose_name="Imagem",
                              upload_to='projects/images/%Y/%m/%d/')
    image_description = models.CharField(
        verbose_name="Descrição da Imagem", max_length=255, blank=True)

    title = models.CharField(verbose_name="Título", max_length=255)
    introduction = models.CharField(
        verbose_name="Introdução", max_length=255)
    description = HTMLField(verbose_name="Descrição")
    slug = models.SlugField(unique=True)
    is_flexible = models.BooleanField(
        verbose_name="Aceita doações além da meta?", default=True)
    goal = models.FloatField(verbose_name="Objetivo (R$)", )
    collected = models.FloatField(verbose_name="Valor Arrecadado", default=0)
    deadline = models.DateField(
        verbose_name="Data de Encerramento",
        default=(datetime.datetime.now))

    is_published = models.BooleanField(
        verbose_name="Está publicado?", default=False)

    is_reproved = models.BooleanField(
        verbose_name="Reprovado?", default=False)
    reproval_reason = HTMLField(
        verbose_name="Motivo da reprovação", blank=True)

    def is_withdrawal_available(self):
        now = dt.now().date()
        return (
            now >= (self.deadline +
                    datetime.timedelta(days=settings.DAYS_FOR_WITHDRAWAL_REQUEST))
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"


class Donation(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        verbose_name="Usuário",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    project = models.ForeignKey(
        verbose_name="Projeto", to=Project, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField(verbose_name="Quantia")

    # Pagamento
    id_checkout = models.CharField(
        verbose_name="Id do pagamento (Mercado Pago)",
        max_length=255,
        default="",
    )
    payment_infos = models.JSONField(
        verbose_name="Informações do Pagamento (Mercado Pago)",
        null=True,
        default=None
    )

    class Meta:
        verbose_name = "Doação"
        verbose_name_plural = "Doações"


class WithdrawalRequest(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        verbose_name="Usuário",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    project = models.ForeignKey(
        verbose_name="Projeto", to=Project, on_delete=models.SET_NULL, null=True)

    beneficiary_information = HTMLField(
        verbose_name="Informações do Beneficiário")

    paid = models.BooleanField(
        verbose_name="Pago",
        default=False
    )
    comments = HTMLField(
        verbose_name="Comentários", blank=True)
    payment_proof = models.FileField(
        verbose_name="Comprovante da Transferência",
        upload_to='withdrawals/proofs/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = "Solicitação de Saque"
        verbose_name_plural = "Solicitações de Saque"

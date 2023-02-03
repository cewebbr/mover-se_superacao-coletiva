from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel

from projects.models import Project


class Topic(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        verbose_name="Criador",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    project = models.ForeignKey(
        verbose_name="Projeto",
        to=Project,
        on_delete=models.SET_NULL,
        null=True

    )

    title = models.CharField(verbose_name="Título", max_length=255)
    description = models.TextField(verbose_name="Descrição")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tópico"
        verbose_name_plural = "Tópicos"


class Message(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        verbose_name="Criador",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    topic = models.ForeignKey(
        verbose_name="Tópico",
        to=Topic,
        on_delete=models.CASCADE
    )

    content = models.TextField(verbose_name="Conteúdo")

    def __str__(self):
        return (self.content[:75] + '...') if len(self.content) > 75 else self.content

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"


class MessageVote(TimeStampedModel, models.Model):
    user = models.ForeignKey(
        verbose_name="Usuário",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        verbose_name="Mensagem",
        to=Message,
        on_delete=models.CASCADE
    )

    value = models.BooleanField(
        verbose_name="Gostou", default=True)

    class Meta:
        verbose_name = "Voto Mensagem"
        verbose_name_plural = "Votos Mensagens"

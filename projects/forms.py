import datetime

from crispy_forms.helper import FormHelper
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE

from projects.models import Donation, Project, WithdrawalRequest


class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'is_published', 'is_reproved',
                   'reproval_reason', 'collected', 'slug']
        widgets = {
            'goal': forms.NumberInput(
                attrs={
                    'placeholder': "R$",
                }
            ),
            'deadline': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': datetime.date.today(),
                }
            ),
        }
        help_texts = {
            'introduction': 'Por favor, descreva brevemente seu projeto.',
            'image_description': 'Por favor, descreva a imagem para do projeto. Utilizado para acessibilidade.',
            'deadline': f'Observação: O recebimento do valor coletado só poderá ser solicitado {settings.DAYS_FOR_WITHDRAWAL_REQUEST} dia(s) após a data de encerramento do projeto.',
        }

    def clean_goal(self):
        data = self.cleaned_data.get('goal')

        if data < settings.PROJECT_MINIMUM_GOAL:
            raise ValidationError(
                'O objetivo deve ser no mínimo R$ ' +
                f'{settings.PROJECT_MINIMUM_GOAL:,.2f}'.replace(
                    ',', '').replace('.', ',') + '.',
                code='invalid',
            )

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class ProjectUpdateForm(ProjectCreateForm):
    pass


class ProjectReviewForm(forms.Form):
    approve = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )

    reproval_reason = forms.CharField(
        label="Motivo da reprovação: ",
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30}),
        required=False
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.filter(is_published=False),
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super().clean()

        project = cleaned_data.get('project')

        if project.is_published:
            raise ValidationError({
                'password': "Erro! O projeto selecionado já foi publicado.",
            })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class DonateProjectForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['user', 'project', 'amount']
        widgets = {
            'amount': forms.NumberInput(
                attrs={
                    'placeholder': "R$",
                },
            ),
            'user': forms.HiddenInput(),
            'project': forms.HiddenInput(),
        }

    def clean_amount(self):
        data = self.cleaned_data.get('amount')

        if data < settings.PROJECT_MINIMUM_DONATION:
            raise ValidationError(
                f'O valor da doação deve ser no mínimo R$ ' +
                f'{settings.PROJECT_MINIMUM_GOAL:,.2f}'.replace(
                    ',', '').replace('.', ',') + '.',
                code='invalid',
            )

        project = self.cleaned_data.get('project')
        if data + project.collected > project.goal and not project.is_flexible:
            raise ValidationError(
                f'Este projeto não aceita doações acima da meta! O valor restante para atingir a meta do projeto é R$ ' +
                f'{project.goal-project.collected:,.2f}'.replace(
                    ',', '').replace('.', ',') + '.',
                code='invalid',
            )

        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class WithdrawalRequestCreateForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['user', 'project', 'beneficiary_information']
        widgets = {
            'user': forms.HiddenInput(),
            'project': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class WithdrawalRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['beneficiary_information']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class WithdrawalRequestReplyForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['paid', 'comments', 'payment_proof']

    def clean(self):
        cleaned_data = super().clean()

        paid = cleaned_data.get('paid')
        payment_proof = cleaned_data.get('payment_proof')

        if paid and not payment_proof:
            raise ValidationError(
                "Por favor, insira o comprovante da transferência."
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

import re

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Fieldset, Layout, Row
from django import forms
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError

from .models import User


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'profile_picture', 'about', 'phone_number', 'cell_phone_number', 'country', 'state',
                  'zip', 'city', 'address', ]

        labels = {
            'about': 'Fale um pouco sobre você'
        }
        widgets = {
            'country': forms.Select(attrs={'placeholder': "País"}),
            'state': forms.Select(attrs={'placeholder': "Estado"}),
            'zip': forms.TextInput(attrs={'placeholder': "Cep"}),
            'city': forms.TextInput(attrs={'placeholder': "Cidade"}),
            'address': forms.TextInput(attrs={'placeholder': "Endereço"}),
            'phone_number': forms.TextInput(attrs={'placeholder': "Telefone", 'data-mask': "(00) 0000-0000"}),
            'cell_phone_number': forms.TextInput(attrs={'placeholder': "Celular", 'data-mask': "(00) 0 0000-0000"}),
        }

        help_texts = {
            'phone_number': 'O telefone deve estar no formato (XX) XXXX-XXXX',
            'cell_phone_number': 'O celular deve estar no formato (XX) X XXXX-XXXX.',
            'zip': 'O CEP deve estar no formato XXXXX-XXX',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    HTML(
                        """
                            Informações Públicas
                            <span class="text-muted fw-normal fs-5 text-nowrap">
                                (Visível para todos)
                            </span> 
                            <hr>
                        """,
                    ),
                    css_class="h3"
                ),
                Row(
                    Column(
                        HTML(
                            """
                                {% load static %}
                                <label class="d-flex justify-content-center mb-2 mb-lg-0" for="id_profile_picture">
                                    {% if form.instance.profile_picture %}
                                        <img id="profile_picture-preview" class="img-thumbnail col-6 col-lg-12" thumbnail src="{{ form.instance.profile_picture.url }}" />
                                    {% else %}
                                        <img id="profile_picture-preview" class="img-thumbnail col-6 col-lg-12" thumbnail src="{% static 'global/img/person.svg' %}" />
                                    {% endif %}
                                </label>
                            """,
                        ),
                        css_class='form-group col-lg-2 mb-0'
                    ),
                    Column(
                        'profile_picture',
                        css_class='form-group col-lg-10 mb-0',
                        id="profile_picture_column"
                    ),
                    css_class='form-row mb-4',
                ),
                Row(
                    Column('username', css_class='form-group col-12 mb-0'),
                    css_class='form-row mb-4',
                ),
                Row(
                    Column('about', css_class='form-group col-12 mb-0'),
                    css_class='form-row mb-4',
                ),
                css_class='form-row py-4',
                id="pub-info"
            ),

            Row(
                Column(
                    HTML(
                        """
                            Informações Privadas
                            <span class="text-muted fw-normal fs-5 text-nowrap">
                                (Visível somente para a nossa equipe)
                            </span>  
                            <hr>
                        """,
                    ),
                    css_class="h3 mt-4"
                ),
                Fieldset(
                    "Endereço",
                    Row(
                        Column('country', css_class='form-group col-lg-4 mb-0'),
                        Column('state', css_class='form-group col-lg-8 mb-0'),
                    ),
                    Row(
                        Column('zip', css_class='form-group col-lg-4 mb-0'),
                        Column('city', css_class='form-group col-lg-8 mb-0'),
                        Column('address', css_class='form-group col-lg-12 mb-0'),
                    ),
                    css_class='form-row mb-4',
                    id="address"
                ),

                Fieldset(
                    "Contato",
                    Row(
                        Column('phone_number',
                               css_class='form-group col-lg-6 mb-0'),
                        Column('cell_phone_number',
                               css_class='form-group col-lg-6 mb-0'),
                        css_class='form-row mb-4'
                    ),
                    css_class='form-row mb-4',
                    id="contact"
                ),
                id="priv-info"
            )
        )

    def clean_phone_number(self):
        data = self.cleaned_data.get('phone_number')

        if data and not re.match(r"^\(?[1-9]{2}\)? ?[0-9]{4}-?[0-9]{4}$", data):
            raise ValidationError(
                'O telefone deve estar no formato (XX) XXXX-XXXX.',
                code='invalid',
            )

        return data

    def clean_cell_phone_number(self):
        data = self.cleaned_data.get('cell_phone_number')

        if data and not re.match(r"^\(?[1-9]{2}\)? ?\d ?[0-9]{4}-?[0-9]{4}$", data):
            raise ValidationError(
                'O celular deve estar no formato (XX) X XXXX-XXXX.',
                code='invalid',
            )

        return data

    def clean_zip(self):
        data = self.cleaned_data.get('zip')

        if data and not re.match(r"^[0-9]{5}-[0-9]{3}$", data):
            raise ValidationError(
                'CEP inválido.',
                code='invalid',
            )

        return data


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

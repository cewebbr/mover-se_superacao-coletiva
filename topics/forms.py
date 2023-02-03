from crispy_forms.helper import FormHelper
from django import forms

from topics.models import Message, Topic


class TopicCreateForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['user', 'project', 'title', 'description']

        widgets = {
            'user': forms.HiddenInput(),
            'project': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class MessageCreateForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['user', 'topic', 'content']

        widgets = {
            'user': forms.HiddenInput(),
            'topic': forms.HiddenInput(),
            'content': forms.Textarea(attrs={
                'class': "form-control auto-height-textarea shadow-sm",
                'placeholder': "Escreva uma resposta para o tópico",
                'rows': "3",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.wrapper_class = 'flex-fill me-lg-3'

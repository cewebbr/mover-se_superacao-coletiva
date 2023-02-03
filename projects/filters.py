import django_filters
from django import forms
from django.utils import timezone
from django_filters import ChoiceFilter


class ProjectFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control rounded-0 rounded-start border-end-0 shadow-none',
                'placeholder': 'Pesquisar'
            }),
    )


class ProjectListFilter(ProjectFilter):
    deadline_choices = (
        ('all', 'Todos Projetos'),
        ('active', 'Projetos Ativos'),
        ('finished', 'Projetos Encerrados'),
    )

    status = ChoiceFilter(
        field_name='deadline',
        label='Filtrar por: ',
        choices=deadline_choices,
        method='filter_by_deadline',
        initial='all',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def filter_by_deadline(self, queryset, name, value):
        now = timezone.now()

        if value == 'active':
            return queryset.filter(
                deadline__gte=now,
            )
        elif value == 'finished':
            return queryset.filter(
                deadline__lt=now,
            )

        return queryset


class ProjectsOwnedListFilter(ProjectFilter):
    deadline_choices = (
        ('all', 'Todos'),
        ('active', 'Projetos Ativos'),
        ('finished', 'Projetos Encerrados'),
    )

    status = ChoiceFilter(
        field_name='deadline',
        label='Status: ',
        choices=deadline_choices,
        method='filter_by_deadline',
        initial='all',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    is_published = django_filters.ChoiceFilter(
        field_name='is_published',
        label='Publicados: ',
        choices=[
            ('', 'Todos'),
            (True, 'Sim'),
            (False, 'Não'),
        ],
        initial='',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    is_reproved = django_filters.ChoiceFilter(
        field_name='is_reproved',
        label='Reprovados: ',
        choices=[
            ('', 'Todos'),
            (True, 'Sim'),
            (False, 'Não'),
        ],
        initial='',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select d-flex'}),
    )

    def filter_by_deadline(self, queryset, name, value):
        now = timezone.now()

        if value == 'active':
            return queryset.filter(
                deadline__gte=now,
            )
        elif value == 'finished':
            return queryset.filter(
                deadline__lt=now,
            )

        return queryset


class ProjectReviewListFilter(ProjectFilter):
    filter_by_choices = (
        ('all', 'Projetos não Aprovados'),
        ('review', 'Projetos em Análise'),
        ('reproved', 'Projetos Reprovados'),
    )

    filter_by = django_filters.ChoiceFilter(
        field_name=None,
        label='Filtrar por: ',
        choices=filter_by_choices,
        method='filter_filter_by',
        initial='all',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select d-flex'}),
    )

    def filter_filter_by(self, queryset, name, value):
        if value == 'review':
            return queryset.filter(
                is_reproved=False,
            )
        elif value == 'reproved':
            return queryset.filter(
                is_reproved=True,
            )

        return queryset


class WithdrawalRequestListFilter(ProjectFilter):
    paid = django_filters.ChoiceFilter(
        field_name='paid',
        label='Status: ',
        choices=[
            ('', 'Todas'),
            (True, 'Transferências Realizadas'),
            (False, 'Transferências Pendentes'),
        ],
        initial='',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

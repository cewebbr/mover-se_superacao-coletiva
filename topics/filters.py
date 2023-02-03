import django_filters
from django import forms
from django.db.models import Count, F, Q
from django.forms.widgets import CheckboxInput
from django_filters import BooleanFilter, ChoiceFilter


class MessageOrderByFilter(django_filters.FilterSet):
    order_by_choices = (
        ('created', 'Data de publicação'),
        ('votes', 'Avaliações'),
    )

    order_by = ChoiceFilter(
        field_name=None,
        label='Ordenar por:',
        choices=order_by_choices,
        method='filter_order_by',
        initial='created',
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    ascending = BooleanFilter(
        field_name=None,
        label='Decrescente: ',
        method='filer_order_by_ascending',
        initial=False,
        widget=CheckboxInput(attrs={'class': 'btn-check'}),
    )

    def filter_order_by(self, queryset, name, value):

        if value == 'votes':
            return (
                queryset.annotate(
                    upvotes=Count('messagevote',
                                  filter=Q(messagevote__value=True)),
                    downvotes=Count('messagevote',
                                    filter=Q(messagevote__value=False))
                ).order_by(F('downvotes') - F('upvotes'))
            )
        elif value == 'created':
            return queryset.order_by('-created')

        return queryset

    def filer_order_by_ascending(self, queryset, name, value):
        if value is True:
            return queryset.reverse()

        return queryset

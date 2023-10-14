from django import forms
from django.forms import DateInput
import django_filters
from django_filters import FilterSet
from .models import *


class PostFilter(FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='contains',
        label='Заголовок содержит',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Любое слово'
            }
        )
    )

    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        label='Категория новости',
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-check-input'
            }
        )
    )

    date_joined_after = django_filters.DateFilter(
        field_name='date_joined',
        lookup_expr='gt',
        label='Опубликована после',
        widget=DateInput(
            format='%Y-%m-%dT%H:%M',
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'date_joined_after']

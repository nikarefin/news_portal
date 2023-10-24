from django import forms
from .models import *
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='Заголовок',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    text = forms.CharField(
        label='Описание',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )

    category = forms.ModelChoiceField(
        label='Категория',
        empty_label='Не выбрана',
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    author = forms.ModelChoiceField(
        label='Автор',
        empty_label='Не выбран',
        queryset=Author.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 20:
            raise ValidationError(
                "Описание должно быть больше 20 символов"
            )
        return text

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'author']

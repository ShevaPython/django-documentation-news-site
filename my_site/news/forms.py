import re

from django import forms
from django.core.exceptions import ValidationError

from news.models import News


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'is_publish', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Названия не должно начинаться с цыфры')
        if len(title) <= 2:
            raise ValidationError("Длина должна быть больше 2 символов")
        return title

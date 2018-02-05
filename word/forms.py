from django import forms

from word.models import Word


class WikiForm(forms.ModelForm):

    class Meta:
        model = Word
        fields = (
            'word',
            'description',
        )


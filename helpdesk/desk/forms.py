from django import forms
from.models import *


class QueryFrom(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('status',)


class NewQuery(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('contact', 'description')


class Feedback(forms.ModelForm):
    class Meta:
        model = Query
        fields = ('feedback',)

from dataclasses import fields
from  django import forms
from django.forms import widgets
from .models import Repertoire , MusicTrack , Genre, Hall

class RepertoireForm(forms.ModelForm):
    class Meta:
        model = Repertoire
        fields = ['music_track','hall','host' , 'day','start_time' , 'end_time' , 'date']
        widgets = {
            'date' : forms.DateInput(attrs={'type':'date'}),
            'start_time' : forms.TimeInput(attrs={'type':'time'}),
            'end_time' : forms.TimeInput(attrs={'type' : 'time'}),
        } 


class SearchForm(forms.Form):
    """Форма для поиска в репертуаре"""
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        label="Жанр",
        empty_label="Все жанры"
    )
    date = forms.DateField(
        required=False,
        label="Дата",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hall = forms.ModelChoiceField(
        queryset=Hall.objects.all(),
        required=False,
        label="Зал",
        empty_label="Все залы"
    )

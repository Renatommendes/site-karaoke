from django import forms

class YouTubeForm(forms.Form):
    url = forms.URLField(label='Link do YouTube')
    pitch_shift = forms.IntegerField(label='Alterar tom (semitons)', required=False, initial=0)

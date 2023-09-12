from django import forms

class CreateNewPost(forms.Form):
    titulo = forms.CharField(label="Titulo",  max_length=50, widget=forms.TextInput(attrs={
        'class': 'input'
    }))
    contenido = forms.CharField(label="Detalles", widget=forms.TextInput(attrs={
        'class': 'input'
    }))
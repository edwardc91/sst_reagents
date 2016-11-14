from django import forms
from django.forms import widgets

from django.contrib.auth import authenticate

from reactivos_sst_app.models import Propiedad
from django.db import DatabaseError

from compounds_update_app.models import Existencia, Reactivo

import re


def get_propiedade_choices():
    try:
        propiedades = Propiedad.objects.all()
        choices = []

        for propiedad in propiedades:
            choices.append((propiedad.propiedad, unicode(propiedad.propiedad),))

        return choices
    except DatabaseError:
        return []


class ReactivoForm(forms.ModelForm):
    propiedades = forms.MultipleChoiceField(widget=widgets.CheckboxSelectMultiple(), choices=get_propiedade_choices(),
                                            label="Propiedades")

    class Meta:
        model = Reactivo
        exclude = ['local', ]
        widgets = {'nombre': widgets.TextInput(attrs={'class': 'form-control'}),
                   'nombre_frasco': widgets.TextInput(attrs={'class': 'form-control'}),
                   'r_reglas': widgets.TextInput(attrs={'class': 'form-control'}),
                   's_reglas': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_cas': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_nu': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_icsc': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_rtecs': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_ce': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_einecs': widgets.TextInput(attrs={'class': 'form-control'}),
                   'peso_molecular': widgets.NumberInput(attrs={'class': 'form-control'}),
                   'observaciones': widgets.Textarea(attrs={'class': 'form-control'}),
                   }

    def clean(self):
        cleaned_data = super(ReactivoForm, self).clean()
        n_cas = self.cleaned_data.get('n_cas')
        peso_molecular = self.cleaned_data.get('peso_molecular')
        nombre_frasco = self.cleaned_data.get('nombre_frasco')

        if not nombre_frasco:
            raise forms.ValidationError("Es necesario que introduzca un valor para el nombre del frasco")

        if not re.match("(\d+-\d+-\d+)", n_cas) and n_cas:
            raise forms.ValidationError("El CAS tiene que tener el formato \"numero-numero-numero\".")

        if peso_molecular:
            if int(peso_molecular) <= 0:
                raise forms.ValidationError("El peso molecular debe ser mayor que cero.")

        return self.cleaned_data


class ExistenciaForm(forms.ModelForm):
    class Meta:
        model = Existencia
        exclude = ['reactivo']


class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=20,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        usuario = self.cleaned_data.get('usuario')
        password = self.cleaned_data.get('password')

        if not authenticate(username=usuario, password=password):
            raise forms.ValidationError("Usuario o password incorrecto")

        return self.cleaned_data


class SearchForm(forms.Form):
    termino_busqueda = forms.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reactivo'}))

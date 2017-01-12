from django import forms
from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import widgets

from django.contrib.auth import authenticate

from reactivos_sst_app.models import Propiedad
from django.db import DatabaseError

from compounds_update_app.models import ExistenciaUpdate, ReactivoUpdate, SinonimosUpdate

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
                                            label="Propiedades", required=False)

    check_unique = True
    user_local = None

    class Meta:
        model = ReactivoUpdate
        exclude = ['local', ]
        widgets = {'nombre': widgets.TextInput(attrs={'class': 'form-control'}),
                   'nombre_frasco': widgets.TextInput(attrs={'class': 'form-control'}),
                   'r_reglas': widgets.TextInput(attrs={'class': 'form-control'}),
                   's_reglas': widgets.TextInput(attrs={'class': 'form-control'}),
                   'h_reglas': widgets.TextInput(attrs={'class': 'form-control'}),
                   'p_reglas': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_cas': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_nu': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_icsc': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_rtecs': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_ce': widgets.TextInput(attrs={'class': 'form-control'}),
                   'n_einecs': widgets.TextInput(attrs={'class': 'form-control'}),
                   'peso_molecular': widgets.NumberInput(attrs={'class': 'form-control'}),
                   }

    def clean(self):
        cleaned_data = super(ReactivoForm, self).clean()
        n_cas = self.cleaned_data.get('n_cas')
        n_rtecs = self.cleaned_data.get('n_rtecs')
        n_einecs = self.cleaned_data.get('n_einecs')
        n_ce = self.cleaned_data.get('n_ce')
        n_icsc = self.cleaned_data.get('n_icsc')
        peso_molecular = self.cleaned_data.get('peso_molecular')
        nombre_frasco = self.cleaned_data.get('nombre_frasco')

        if not nombre_frasco:
            raise forms.ValidationError("Es necesario que introduzca un valor para el nombre de la etiqueta del frasco")
        else:
            reactivo_existente = ReactivoUpdate.objects.filter(nombre_frasco__iexact=nombre_frasco,
                                                               local=self.user_local)
            if reactivo_existente.exists() and self.check_unique:
                raise forms.ValidationError(
                    "Ya existe un reactivo con la etiqueta " + nombre_frasco + " en el local " + self.user_local)

        if not re.match("[0-9]+-[0-9]{2}-[0-9]$", n_cas) and n_cas:
            raise forms.ValidationError("El CAS introducido tiene un formato incorrecto.")

        if not re.match("[A-Z][A-Z0-9_]\d+0$", n_rtecs) and n_rtecs:
            raise forms.ValidationError("El RTECS introducido tiene un formato incorrecto.")

        if not re.match("[0-9]{3}-[0-9]{3}-[0-9]$", n_einecs) and n_einecs:
            raise forms.ValidationError("El EINECS introducido tiene un formato incorrecto.")

        if not re.match("[0-9]{2,3}-[0-9]{3}-[0-9]{1,2}(-[0-9]|-X)?$", n_ce) and n_ce:
            raise forms.ValidationError("El CE introducido tiene un formato incorrecto.")

        if not re.match("[0-9]{2,3}-[0-9]{3}-[0-9]{1,2}(-[0-9]|-X)?$", n_ce) and n_ce:
            raise forms.ValidationError("El CE introducido tiene un formato incorrecto.")

        if peso_molecular:
            if float(peso_molecular) <= 0:
                raise forms.ValidationError("El peso molecular debe ser mayor que cero.")

        return self.cleaned_data


class SinonimoForm(forms.ModelForm):
    class Meta:
        model = SinonimosUpdate
        fields = ('sinonimo',)
        widgets = {'sinonimo': widgets.TextInput(attrs={'class': 'form-control'})}


class ExistenciaForm(ModelForm):
    cantidad = forms.CharField(error_messages={'required': "Debe insertar un valor para la cantidad de la existencia"},
                               widget=widgets.NumberInput(attrs={'class': 'form-control'}))
    capacidad = forms.CharField(
        error_messages={'required': "Debe insertar un valor para la capacidad de la existencia"},
        widget=widgets.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = ExistenciaUpdate
        exclude = ['reactivo']
        widgets = {'cantidad': widgets.NumberInput(attrs={'class': 'form-control'}),
                   'capacidad': widgets.NumberInput(attrs={'class': 'form-control'}),
                   'unidad_medida': widgets.Select(attrs={'class': 'form-control'}),
                   'almacenamiento_idoneo': widgets.CheckboxInput(),
                   'tipo_envase': widgets.Select(attrs={'class': 'form-control'}),
                   'material_envase': widgets.Select(attrs={'class': 'form-control'}),
                   'firma': widgets.TextInput(attrs={'class': 'form-control'}),
                   }


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
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'ReactivoUpdate'}))

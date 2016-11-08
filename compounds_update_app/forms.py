from django import forms
from django.forms import widgets

from reactivos_sst_app.models import Propiedad
from django.db import DatabaseError

from compounds_update_app.models import Existencia, Reactivo

import re


class ReactivoForm(forms.ModelForm):

    class Meta:
        model = Reactivo
        exclude = ['local', ]

    def clean(self):
        cleaned_data = super(ReactivoForm, self).clean()
        n_cas = self.cleaned_data.get('n_cas')

        if not re.match("d+-d+-d+", n_cas):
            raise forms.ValidationError("El CAS tiene que tener el formato \"numero-numero-numero\".")

        return self.cleaned_data


def get_propiedade_choices():
    try:
        propiedades = Propiedad.objects.all()
        choices = []

        for propiedad in propiedades:
            choices.append((propiedad.propiedad, propiedad.propiedad,))

        return choices
    except DatabaseError:
        return []


class PropiedadForm(forms.Form):
    propiedad = forms.ChoiceField(choices=get_propiedade_choices(), widget=widgets.CheckboxSelectMultiple)


class ExistenciaForm(forms.ModelForm):
    class Meta:
        model = Existencia
        exclude = ['reactivo']

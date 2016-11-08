from django.shortcuts import render
from django.forms import inlineformset_factory

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.views.generic import ListView
from compounds_update_app.models import Reactivo, PropiedadUp

from reactivos_sst_app.models import Local

from forms import ReactivoForm, PropiedadForm

from django.forms import widgets


# Create your views here.
class ListaReactivosView(ListView):
    template_name = "comps_update_templates/lista_reactivos.html"
    model = Reactivo
    context_object_name = 'lista_reactivos'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListaReactivosView, self).get_context_data(**kwargs)

        lista_locales = Local.objects.all()

        context['lista_locales'] = lista_locales

        return context


def create_reactivo_view(request):
    lista_locales = Local.objects.all()

    if request.POST:
        form_reactivo = ReactivoForm(request.POST)
        form_propiedades = PropiedadForm(request.POST)
    else:
        form_reactivo = ReactivoForm()
        form_propiedades = PropiedadForm()

    context = {'lista_locales': lista_locales, 'form_reactivo': form_reactivo, 'form_propiedades': form_propiedades}
    return render(request, "comps_update_templates/add_reactivo.html", context)


class UpdateReactivoView(UpdateView):
    model = Reactivo
    form_class = ReactivoForm

from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, DeleteView,FormView

from django.views.generic import ListView
from compounds_update_app.models import Reactivo

from reactivos_sst_app.models import Local

from forms import ReactivoForm


# Create your views here.
class ListaReactivosView(ListView):
    template_name = "comps_update_templates/lista_reactivos.html"
    model = Reactivo
    context_object_name = 'lista_reactivos'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(ListaReactivosView,self).get_context_data(**kwargs)

        lista_locales = Local.objects.all()

        context['lista_locales'] = lista_locales

        return context


class CreateReactivoView(FormView):
    form_class = ReactivoForm
    template_name = "comps_update_templates/add_reactivo.html"


class UpdateReactivoView(UpdateView):
    model = Reactivo
    form_class = ReactivoForm

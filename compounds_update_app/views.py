from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.db import DatabaseError

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.views.generic import ListView, View
from compounds_update_app.models import Reactivo, PropiedadUp, UserInfo

from reactivos_sst_app.models import Local, Propiedad

from forms import ReactivoForm, LoginForm, SearchForm
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.contrib import messages
import simplejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from django.views.generic.list import MultipleObjectTemplateResponseMixin

from django.forms import widgets


# Create your views here.
class LoginView(FormView):
    form_class = LoginForm
    template_name = "comps_update_templates/login.html"

    def form_valid(self, form, **kwargs):
        usuario = form.cleaned_data['usuario']
        password = form.cleaned_data['password']

        user = authenticate(username=usuario, password=password)

        local_id = 0

        if user:
            login(self.request, user)

            if not user.is_staff:
                user_local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
                local_id = Local.objects.get(nombre__iexact=user_local).id

            return HttpResponseRedirect(reverse("listado_reactivos", kwargs={'id': str(local_id)}))
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        # here you can add things like:
        return self.render_to_response(context)


def logout_view(request):
    logout(request)
    # form = forms.LoginForm()
    return HttpResponseRedirect(reverse('login'))


class ListaReactivosView(ListView):
    template_name = "comps_update_templates/lista_reactivos.html"
    context_object_name = 'lista_reactivos'
    paginate_by = 10
    query = ""

    def get_context_data(self, **kwargs):
        context = super(ListaReactivosView, self).get_context_data(**kwargs)

        lista_locales = Local.objects.all()

        context['lista_locales'] = lista_locales

        lista_reactivos = context['lista_reactivos']
        cant_reactivos = lista_reactivos.count()

        initial_data = []
        for reactivo in lista_reactivos:
            reactivo_propiedades = PropiedadUp.objects.filter(reactivo=reactivo)

            n_cas = None
            if reactivo.n_cas and reactivo.n_cas != "0-0-0":
                n_cas = reactivo.n_cas

            initial_data.append(
                {'nombre': reactivo.nombre, 'nombre_frasco': reactivo.nombre_frasco, 'n_cas': n_cas,
                 'r_reglas': reactivo.r_reglas, 's_reglas': reactivo.s_reglas, 'n_nu': reactivo.n_nu,
                 'n_icsc': reactivo.n_icsc, 'n_rtecs': reactivo.n_rtecs, 'n_ce': reactivo.n_ce,
                 'n_einecs': reactivo.n_einecs, 'peso_molecular': reactivo.peso_molecular,
                 'observaciones': reactivo.observaciones, 'propiedades': reactivo_propiedades})

        reactivo_formset = formset_factory(ReactivoForm, can_delete=False, extra=cant_reactivos)
        context['formset_reactivos'] = reactivo_formset(initial=initial_data)
        # context['search_form'] = SearchForm()

        user = self.request.user
        if user.is_staff:
            local_id = int(self.kwargs['id'])
            context['local_id'] = local_id
            if local_id == 0:
                text_local = " todos los locales."
            else:
                local = Local.objects.get(pk=local_id).nombre
                text_local = local
        else:
            local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
            text_local = local

        context["nombre_local"] = text_local

        context['termino_busqueda'] = self.request.GET.get('termino_busqueda')

        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            local_id = int(self.kwargs['id'])
            if local_id == 0:
                queryset = Reactivo.objects.all().order_by('nombre_frasco')
            else:
                local = Local.objects.get(pk=local_id).nombre
                queryset = Reactivo.objects.filter(local=local)
        else:
            local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
            queryset = Reactivo.objects.filter(local=local).order_by('nombre_frasco')

        termino = self.request.GET.get('termino_busqueda')
        if termino != "None" and termino:
            termino = self.request.GET.get('termino_busqueda')
            queryset = queryset.filter(
                Q(nombre__icontains=termino) | Q(nombre_frasco__icontains=termino) | Q(
                    n_cas__icontains=termino) | Q(local__icontains=termino))

        return queryset

    def post(self, request, *args, **kwargs):
        if 'nombre_reactivo' in request.POST:
            reactivo_id = request.POST['nombre_reactivo']
            try:
                reactivo = Reactivo.objects.get(pk=reactivo_id)
                reactivo.delete()
                context = {'status': 'True', 'reactivo_id': reactivo_id}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")
            except:
                context = {'status': 'False'}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")


def get_propiedade_choices():
    try:
        propiedades = Propiedad.objects.all()
        choices = []

        for propiedad in propiedades:
            choices.append((propiedad.propiedad, str(propiedad.propiedad),))

        return choices
    except DatabaseError:
        return []


@login_required
def create_reactivo_view(request):
    lista_locales = Local.objects.all()

    if request.POST:
        form_reactivo = ReactivoForm(request.POST)

        if form_reactivo.is_valid():
            nombre = form_reactivo.cleaned_data['nombre']
            nombre_frasco = form_reactivo.cleaned_data['nombre_frasco']
            r_reglas = form_reactivo.cleaned_data['r_reglas']
            s_reglas = form_reactivo.cleaned_data['s_reglas']
            n_cas = form_reactivo.cleaned_data['n_cas']
            n_nu = form_reactivo.cleaned_data['n_nu']
            n_icsc = form_reactivo.cleaned_data['n_icsc']
            n_rtecs = form_reactivo.cleaned_data['n_rtecs']
            n_einecs = form_reactivo.cleaned_data['n_einecs']
            peso_molecular = form_reactivo.cleaned_data['peso_molecular']
            observaciones = form_reactivo.cleaned_data['observaciones']

            propiedades = filter(lambda t: t[0] in form_reactivo.cleaned_data['propiedades'],
                                 form_reactivo.fields['propiedades'].choices)

            if not n_cas:
                n_cas = "0-0-0"

            user = request.user
            user_local = UserInfo.objects.get(user_auth__username__iexact=user.username).local

            reactivo = Reactivo.objects.create(nombre=nombre, nombre_frasco=nombre_frasco, r_reglas=r_reglas,
                                               s_reglas=s_reglas, n_cas=n_cas, n_nu=n_nu, n_icsc=n_icsc,
                                               n_rtecs=n_rtecs,
                                               n_einecs=n_einecs, peso_molecular=peso_molecular,
                                               observaciones=observaciones, local=user_local)

            reactivo.save()

            for propiedad in propiedades:
                propiedad_temp = PropiedadUp.objects.create(reactivo=reactivo, propiedad=propiedad[0])
                propiedad_temp.save()

            local_id = 0
            if not user.is_staff:
                local_id = Local.objects.get(nombre__iexact=user_local).id

            messages.success(request,
                             "Reactivo <strong>" + nombre_frasco + "</strong> ha sido agregado satisfactoriamente.")
            return HttpResponseRedirect(reverse("listado_reactivos", kwargs={'id': local_id}))
        else:
            non_field_errors = form_reactivo.non_field_errors()
            if non_field_errors:
                for error in non_field_errors:
                    messages.error(request, error)

            for field in form_reactivo:
                if field.errors:
                    msn = ""
                    for error in field.errors:
                        msn = error + "\n"
                    messages.error(request, msn, extra_tags=field.label)

            context = {'lista_locales': lista_locales, 'form_reactivo': form_reactivo}
            return render(request, "comps_update_templates/add_reactivo.html", context)
    else:
        form_reactivo = ReactivoForm()

    context = {'lista_locales': lista_locales, 'form_reactivo': form_reactivo}
    return render(request, "comps_update_templates/add_reactivo.html", context)


class UpdateReactivoView(UpdateView):
    model = Reactivo
    form_class = ReactivoForm

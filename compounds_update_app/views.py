# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.forms import formset_factory, inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.db import DatabaseError, IntegrityError

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.views.generic import ListView, View, RedirectView
from compounds_update_app.models import ReactivoUpdate, PropiedadUpdate, UserInfo, SinonimosUpdate, ExistenciaUpdate

from reactivos_sst_app.models import Local, Propiedad

from forms import ReactivoForm, LoginForm, SearchForm, SinonimoForm, ExistenciaForm
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.contrib import messages
import simplejson
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

import re
from django.views.generic.list import MultipleObjectTemplateResponseMixin

from django.forms import widgets


# Create your views here.
def generate_empty_fields_list(reactivo, propiedades, cant_existencias):
    empty_fields = []

    if not reactivo.nombre:
        empty_fields.append("Nombre")
    if not reactivo.nombre_frasco:
        empty_fields.append("Nombre de la etiqueta")
    if not reactivo.s_reglas:
        empty_fields.append("S reglas")
    if not reactivo.r_reglas:
        empty_fields.append("R reglas")
    if not reactivo.h_reglas:
        empty_fields.append("H reglas")
    if not reactivo.p_reglas:
        empty_fields.append("P reglas")
    if not reactivo.n_cas or reactivo.n_cas == "0-0-0":
        empty_fields.append("CAS")
    if not reactivo.n_nu:
        empty_fields.append("NU")
    if not reactivo.n_ce:
        empty_fields.append("CE")
    if not reactivo.n_icsc:
        empty_fields.append("ICSC")
    if not reactivo.n_rtecs:
        empty_fields.append("RTECS")
    if not reactivo.n_einecs:
        empty_fields.append("EINECS")
    if not reactivo.peso_molecular:
        empty_fields.append("peso molecular")
    if not propiedades:
        empty_fields.append("propiedades")
    if cant_existencias == 0:
        empty_fields.append("no tiene existencias registradas")

    return empty_fields


class RedirectToLoginView(RedirectView):
    permanent = False
    pattern_name = "login"


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
    init_reactivo_formset = formset_factory(ReactivoForm, can_delete=False)
    lista_reactivos = None
    cant_cas = 0
    count_queryset = 0

    def get_context_data(self, **kwargs):
        context = super(ListaReactivosView, self).get_context_data(**kwargs)

        lista_locales = Local.objects.all()

        context['lista_locales'] = lista_locales

        lista_reactivos = context['lista_reactivos']
        self.lista_reactivos = lista_reactivos

        initial_data = []
        sinonimos_formsets_init = []
        existencias_formset_init = []
        cantidades_existencias = []
        list_empty_fields = []

        for reactivo in lista_reactivos:
            reactivo_propiedades = PropiedadUpdate.objects.filter(reactivo=reactivo)

            n_cas = None
            if reactivo.n_cas and reactivo.n_cas != "0-0-0":
                n_cas = reactivo.n_cas

            initial_data.append(
                {'nombre': reactivo.nombre, 'nombre_frasco': reactivo.nombre_frasco, 'n_cas': n_cas,
                 'r_reglas': reactivo.r_reglas, 's_reglas': reactivo.s_reglas, 'p_reglas': reactivo.p_reglas,
                 'h_reglas': reactivo.h_reglas, 'n_nu': reactivo.n_nu,
                 'n_icsc': reactivo.n_icsc, 'n_rtecs': reactivo.n_rtecs, 'n_ce': reactivo.n_ce,
                 'n_einecs': reactivo.n_einecs, 'peso_molecular': reactivo.peso_molecular,
                 'propiedades': reactivo_propiedades})

            initial_data_sin = []
            initial_data_existencia = []
            # sinonimos = reactivo.sinonimos.all()

            sinonimos_formset = inlineformset_factory(ReactivoUpdate, SinonimosUpdate, fields=('sinonimo',), extra=0,
                                                      form=SinonimoForm, can_delete=True)

            sinonimos_formsets_init.append(
                sinonimos_formset(initial=initial_data_sin, instance=reactivo, prefix="sinonimos_" + str(reactivo.id)))

            existencias_formset = inlineformset_factory(ReactivoUpdate, ExistenciaUpdate, extra=0,
                                                        form=ExistenciaForm, can_delete=True)

            existencias_formset_init.append(
                existencias_formset(initial=initial_data_existencia, instance=reactivo,
                                    prefix="existencias_" + str(reactivo.id)))

            cant_existencia = ExistenciaUpdate.objects.filter(reactivo=reactivo).count()
            cantidades_existencias.append(cant_existencia)
            list_empty_fields.append(generate_empty_fields_list(reactivo, reactivo_propiedades, cant_existencia))

        reactivo_formset = formset_factory(form=ReactivoForm, can_delete=False, extra=0)
        self.init_reactivo_formset = reactivo_formset
        context['formset_reactivos'] = reactivo_formset(initial=initial_data)
        context['list_sinonimos_formset'] = sinonimos_formsets_init
        context['list_existencia_formset'] = existencias_formset_init
        context['list_cantidades_existencia'] = cantidades_existencias
        context['list_empty_fields'] = list_empty_fields
        context['cantidad_cas'] = self.cant_cas
        context['count_queryset'] = self.count_queryset

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
                queryset = ReactivoUpdate.objects.all().order_by('nombre_frasco')
            else:
                local = Local.objects.get(pk=local_id).nombre
                queryset = ReactivoUpdate.objects.filter(local=local)
        else:
            local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
            queryset = ReactivoUpdate.objects.filter(local=local).order_by('nombre_frasco')

        termino = self.request.GET.get('termino_busqueda')
        if termino != "None" and termino:
            termino = self.request.GET.get('termino_busqueda')
            queryset = queryset.filter(
                Q(nombre__icontains=termino) | Q(nombre_frasco__icontains=termino) | Q(
                    n_cas__icontains=termino) | Q(local__icontains=termino))

        self.lista_reactivos = queryset
        self.count_queryset = queryset.count()
        cant_cas = 0

        for reactivo in queryset:
            if reactivo.n_cas and reactivo.n_cas != "0-0-0":
                cant_cas += 1

        self.cant_cas = cant_cas

        return queryset

    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        if 'nombre_reactivo' in request.POST:
            reactivo_id = request.POST['nombre_reactivo']
            try:
                reactivo = ReactivoUpdate.objects.get(pk=reactivo_id)
                reactivo.delete()
                context = {'status': 'True', 'reactivo_id': reactivo_id}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")
            except:
                context = {'status': 'False'}
                return HttpResponse(simplejson.dumps(context), content_type="application/json")
        else:
            if 'reactivo_current_post_id' in request.POST:
                reactivo_id = request.POST.get("reactivo_current_post_id")

                print "reactivo id " + reactivo_id

                queryset = self.get_queryset()

                init_reactivo_formset = formset_factory(ReactivoForm, can_delete=False, extra=0)
                reactivo_formset = init_reactivo_formset(request.POST)

                paginator = Paginator(queryset, self.paginate_by)
                page = self.request.GET.get('page')

                try:
                    lista_reactivos = paginator.page(page)
                except PageNotAnInteger:
                    lista_reactivos = paginator.page(1)
                except EmptyPage:
                    lista_reactivos = paginator.page(paginator.num_pages)

                index = 0
                lista_reactivos = lista_reactivos.object_list

                for reactivo in lista_reactivos:
                    if reactivo.id == int(reactivo_id):
                        # print "encontro reactivo en " + str(index)
                        break
                    else:
                        index += 1

                # print "index " + str(index)

                # print lista_reactivos

                count = 0
                current_form = None
                for form in reactivo_formset:
                    if count == index:
                        current_form = form
                        break
                    else:
                        count += 1

                # print "count " + str(count)

                current_form.check_unique = False

                if current_form.is_valid():
                    nombre = current_form.cleaned_data.get('nombre')
                    nombre_frasco = current_form.cleaned_data.get('nombre_frasco')
                    # print "Nombre frasco" + nombre_frasco
                    # print "Nombre" + nombre
                    s_reglas = current_form.cleaned_data.get('s_reglas')
                    r_reglas = current_form.cleaned_data.get('r_reglas')
                    p_reglas = current_form.cleaned_data.get('p_reglas')
                    h_reglas = current_form.cleaned_data.get('h_reglas')
                    n_cas = current_form.cleaned_data.get('n_cas')
                    n_nu = current_form.cleaned_data.get('n_nu')
                    n_icsc = current_form.cleaned_data.get('n_icsc')
                    n_rtecs = current_form.cleaned_data.get('n_rtecs')
                    n_einecs = current_form.cleaned_data.get('n_einecs')
                    n_ce = current_form.cleaned_data.get('n_ce')
                    peso_molecular = current_form.cleaned_data.get('peso_molecular')

                    propiedades = filter(lambda t: t[0] in current_form.cleaned_data.get('propiedades'),
                                         current_form.fields['propiedades'].choices)

                    if not n_cas:
                        n_cas = "0-0-0"

                    reactivo = ReactivoUpdate.objects.get(pk=reactivo_id)
                    reactivo.nombre = nombre
                    reactivo.nombre_frasco = nombre_frasco
                    reactivo.r_reglas = r_reglas
                    reactivo.s_reglas = s_reglas
                    reactivo.p_reglas = p_reglas
                    reactivo.h_reglas = h_reglas
                    reactivo.n_cas = n_cas
                    reactivo.n_ce = n_ce
                    reactivo.n_nu = n_nu
                    reactivo.n_rtecs = n_rtecs
                    reactivo.n_icsc = n_icsc
                    reactivo.n_einecs = n_einecs
                    reactivo.peso_molecular = peso_molecular

                    sinonimos_formset = inlineformset_factory(ReactivoUpdate, SinonimosUpdate,
                                                              form=SinonimoForm, can_delete=True)

                    inline_formset = sinonimos_formset(request.POST, instance=reactivo,
                                                       prefix="sinonimos_" + str(reactivo.id))

                    if inline_formset.is_valid():
                        reactivo.save()

                        for sinonimo_form in inline_formset:
                            sinonimo = sinonimo_form.cleaned_data.get('sinonimo')
                            if sinonimo:
                                if not SinonimosUpdate.objects.filter(reactivo=reactivo, sinonimo=sinonimo).exists():
                                    sin_obj = sinonimo_form.save(commit=False)
                                    sin_obj.reactivo = reactivo
                                    sin_obj.save()

                        inline_formset.save()
                    else:
                        # inline_formset = sinonimos_formset(request.POST, request.FILES, instance=reactivo,
                        #                                   prefix="sinonimos_" + str(reactivo.id))

                        error_list = []
                        error_list.append("En el reactivo " + reactivo.nombre_frasco + ":")

                        form_errors = inline_formset.get_unique_error_message(('reactivo', 'sinonimo'))
                        if form_errors:
                            error_list.append(form_errors)

                        user = request.user
                        local_id = 0
                        if not user.is_staff:
                            user_local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
                            local_id = Local.objects.get(nombre__iexact=user_local).id

                        context = {'status': 'False', 'error_list': error_list}
                        return HttpResponse(simplejson.dumps(context), content_type="application/json")

                        # return HttpResponseRedirect(reverse("listado_reactivos", kwargs={'id': str(local_id)}))

                    reactivo_current_prop = PropiedadUpdate.objects.filter(reactivo=reactivo).values_list('propiedad')

                    new_propiedades = []
                    for prop in propiedades:
                        new_propiedades.append(prop[0])

                    for value in reactivo_current_prop:
                        if value[0] not in new_propiedades:
                            prop = PropiedadUpdate.objects.filter(reactivo=reactivo, propiedad=value[0])
                            if prop.exists():
                                prop.delete()

                    for propiedad in propiedades:
                        PropiedadUpdate.objects.get_or_create(reactivo=reactivo, propiedad=propiedad[0])

                    user = request.user
                    local_id = 0
                    if not user.is_staff:
                        user_local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
                        local_id = Local.objects.get(nombre__iexact=user_local).id

                    text = "Reactivo <strong>" + nombre_frasco + "</strong> ha sido actualizado satisfactoriamente."

                    messages.success(request, text)

                    context = {'status': 'True'}
                    return HttpResponse(simplejson.dumps(context), content_type="application/json")
                    # return HttpResponseRedirect(reverse("listado_reactivos", kwargs={'id': str(local_id)}))
                else:
                    non_field_errors = current_form.non_field_errors()
                    error_list = []
                    error_list.append("En el reactivo " + reactivo.nombre_frasco + ":")
                    if non_field_errors:
                        for error in non_field_errors:
                            error_list.append(error)

                    for field in current_form:
                        if field.errors:
                            msn = ""
                            for error in field.errors:
                                msn = error + "\n"
                            error_list.append(error)

                    user = request.user
                    local_id = 0
                    if not user.is_staff:
                        user_local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
                        local_id = Local.objects.get(nombre__iexact=user_local).id

                    context = {'status': 'False', 'error_list': error_list}
                    return HttpResponse(simplejson.dumps(context), content_type="application/json")
            else:
                if "reactivo_existencia_post" in request.POST:
                    reactivo_id = request.POST.get("reactivo_existencia_post")

                    reactivo = ReactivoUpdate.objects.get(pk=reactivo_id)

                    existencia_formset = inlineformset_factory(ReactivoUpdate, ExistenciaUpdate,
                                                               form=ExistenciaForm, can_delete=True)

                    inline_formset = existencia_formset(request.POST, instance=reactivo,
                                                        prefix="existencias_" + str(reactivo.id))

                    if inline_formset.is_valid():
                        try:
                            for existencia_form in inline_formset:
                                sin_obj = existencia_form.save(commit=False)
                                sin_obj.reactivo = reactivo
                                sin_obj.save()

                            inline_formset.save()

                            user = request.user
                            local_id = 0
                            if not user.is_staff:
                                user_local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
                                local_id = Local.objects.get(nombre__iexact=user_local).id

                            messages.success(request,
                                             "Las existencias del reactivo <strong>" + reactivo.nombre_frasco + "</strong> han sido actualizadas satisfactoriamente.")

                            context = {'status': 'True'}
                            return HttpResponse(simplejson.dumps(context), content_type="application/json")
                            # return HttpResponse(simplejson.dumps({'message': "yeah"}))
                            # return HttpResponseRedirect(reverse("listado_reactivos", kwargs={'id': str(local_id)}))
                        except IntegrityError:
                            error_list = []
                            error_list.append(
                                "Existen al menos dos existencias con la misma capacidad, unidad de medida, tipo de envase, material del envase y firma para el reactivo " + reactivo.nombre_frasco + ".")
                            context = {'status': 'False', 'error_list': error_list}
                            return HttpResponse(simplejson.dumps(context), content_type="application/json")
                    else:
                        error_list = []
                        error_list.append("En las existencias del reactivo " + reactivo.nombre_frasco + ":")

                        form_errors = inline_formset.errors
                        print form_errors
                        existencia_num = 0
                        for error_dict in form_errors:
                            if len(error_dict) != 0:
                                if existencia_num == 1:
                                    for field, error in error_dict.items():
                                        error_list.append(error)
                                else:
                                    break
                            existencia_num += 1

                        user = request.user
                        local_id = 0
                        if not user.is_staff:
                            user_local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
                            local_id = Local.objects.get(nombre__iexact=user_local).id

                        context = {'status': 'False', 'error_list': error_list}
                        return HttpResponse(simplejson.dumps(context), content_type="application/json")
                        # return HttpResponseRedirect(reverse("listado_reactivos", kwargs={'id': str(local_id)}))


def get_propiedades_choices():
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
    sinonimos_formset = inlineformset_factory(ReactivoUpdate, SinonimosUpdate, fields=('sinonimo',),
                                              extra=1, form=SinonimoForm)

    if request.POST:
        form_reactivo = ReactivoForm(request.POST)

        user = request.user
        user_local = UserInfo.objects.get(user_auth__username__iexact=user.username).local
        form_reactivo.user_local = user_local

        if form_reactivo.is_valid():
            nombre = form_reactivo.cleaned_data['nombre']
            nombre_frasco = form_reactivo.cleaned_data['nombre_frasco']
            r_reglas = form_reactivo.cleaned_data['r_reglas']
            s_reglas = form_reactivo.cleaned_data['s_reglas']
            h_reglas = form_reactivo.cleaned_data['h_reglas']
            p_reglas = form_reactivo.cleaned_data['p_reglas']
            n_cas = form_reactivo.cleaned_data['n_cas']
            n_nu = form_reactivo.cleaned_data['n_nu']
            n_icsc = form_reactivo.cleaned_data['n_icsc']
            n_rtecs = form_reactivo.cleaned_data['n_rtecs']
            n_einecs = form_reactivo.cleaned_data['n_einecs']
            n_ce = form_reactivo.cleaned_data['n_ce']
            peso_molecular = form_reactivo.cleaned_data['peso_molecular']
            # observaciones = form_reactivo.cleaned_data['observaciones']

            propiedades = filter(lambda t: t[0] in form_reactivo.cleaned_data['propiedades'],
                                 form_reactivo.fields['propiedades'].choices)

            if not n_cas:
                n_cas = "0-0-0"

            reactivo = ReactivoUpdate()
            reactivo.nombre = nombre
            reactivo.nombre_frasco = nombre_frasco
            reactivo.r_reglas = r_reglas
            reactivo.s_reglas = s_reglas
            reactivo.h_reglas = h_reglas
            reactivo.p_reglas = p_reglas
            reactivo.n_cas = n_cas
            reactivo.n_ce = n_ce
            reactivo.n_nu = n_nu
            reactivo.n_rtecs = n_rtecs
            reactivo.n_icsc = n_icsc
            reactivo.n_einecs = n_einecs
            reactivo.peso_molecular = peso_molecular
            reactivo.local = user_local

            inline_formset = sinonimos_formset(request.POST, request.FILES, instance=reactivo)

            if inline_formset.is_valid():
                reactivo.save()
                for sinonimo_form in inline_formset:
                    if sinonimo_form.cleaned_data.get('sinonimo'):
                        sin_obj = sinonimo_form.save(commit=False)
                        sin_obj.reactivo = reactivo
                        sin_obj.save()
            else:
                # inline_formset = sinonimos_formset(request.POST, request.FILES, instance=reactivo)
                #
                # non_form_errors = inline_formset.non_form_errors()
                # if non_form_errors:
                #     for error in non_form_errors:

                error = "Tiene al menos dos sinonimos repetidos."

                messages.error(request, error)

                context = {'lista_locales': lista_locales, 'form_reactivo': form_reactivo,
                           "inline_formset": inline_formset}
                return render(request, "comps_update_templates/add_reactivo.html", context)

            for propiedad in propiedades:
                propiedad_temp = PropiedadUpdate.objects.create(reactivo=reactivo, propiedad=propiedad[0])
                propiedad_temp.save()

            local_id = 0
            if not user.is_staff:
                local_id = Local.objects.get(nombre__iexact=user_local).id

            messages.success(request,
                             "Reactivo <strong>" + nombre_frasco + "</strong> ha sido agregado satisfactoriamente.\nAhora puede agregar sus existencias")
            url_base = reverse("listado_reactivos", kwargs={'id': str(local_id)})
            termino_busqueda = "?termino_busqueda=" + nombre_frasco

            # return HttpResponseRedirect(reverse("listado_reactivos", kwargs={'id': local_id}))
            return HttpResponseRedirect(url_base + termino_busqueda)
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

            inline_formset = sinonimos_formset(request.POST, request.FILES)

            context = {'lista_locales': lista_locales, 'form_reactivo': form_reactivo, "inline_formset": inline_formset}
            return render(request, "comps_update_templates/add_reactivo.html", context)
    else:
        form_reactivo = ReactivoForm()
    inline_formset = sinonimos_formset()
    context = {'lista_locales': lista_locales, 'form_reactivo': form_reactivo, 'inline_formset': inline_formset}
    return render(request, "comps_update_templates/add_reactivo.html", context)


class UpdateReactivoView(UpdateView):
    model = ReactivoUpdate
    form_class = ReactivoForm

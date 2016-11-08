# -*- coding: utf-8 -*-
from django.contrib import admin
import models

from django.db import DatabaseError

from nested_admin import nested


def get_num_estados(model):
    try:
        query_set = model.objects.all()
        if query_set:
            return query_set.count()
        else:
            return 0
    except DatabaseError:
        return 0


# Register your models here.
@admin.register(models.EstadoEnvase)
class EstadosEnvaseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ImagenPropiedad)
class ImagenPropiedadAdmin(admin.ModelAdmin):
    list_per_page = 8


@admin.register(models.Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    filter_horizontal = ['imagenes', ]


@admin.register(models.Local)
class LocalAdmin(admin.ModelAdmin):
    pass


@admin.register(models.EstadoProducto)
class EstadoProductoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MaterialEnvase)
class MaterialEnvaseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TipoEnvase)
class TipoEnvaseAdmin(admin.ModelAdmin):
    ordering = ['tipo']


@admin.register(models.EstadoReactivo)
class EstadoReactivoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PeligroClasificacion)
class PeligroClasificacionAdmin(admin.ModelAdmin):
    filter_horizontal = ['grupo']


@admin.register(models.GrupoPeligrosidad)
class GrupoPeligrosidadAdmin(admin.ModelAdmin):
    pass


class EstadosEnvasesInlines(nested.NestedTabularInline):
    model = models.RelExistenciaEstadoEnvase

    cant_estados = get_num_estados(models.EstadoEnvase)
    extra = cant_estados
    max_num = cant_estados

    verbose_name_plural = "Estados de los envases"


class EstadosExistenciasInlines(nested.NestedTabularInline):
    model = models.RelExistenciaEstadoProducto

    cant_estados = get_num_estados(models.EstadoProducto)

    extra = cant_estados
    max_num = cant_estados

    verbose_name_plural = "Estados de los productos"


class EstadosReactivoInlines(nested.NestedTabularInline):
    model = models.RelExistenciaEstadoReactivo

    cant_estados = get_num_estados(models.EstadoReactivo)

    extra = cant_estados
    max_num = cant_estados

    verbose_name_plural = "Estados de uso del reactivo"


@admin.register(models.Firma)
class FirmaAdmin(admin.ModelAdmin):
    pass


class ExistenciaInline(nested.NestedStackedInline):
    model = models.Existencia
    extra = 0
    inlines = [EstadosEnvasesInlines, EstadosExistenciasInlines, EstadosReactivoInlines, ]


class SinonimosInline(nested.NestedStackedInline):
    model = models.Sinonimo
    extra = 1


@admin.register(models.Reactivo)
class ReactivosAdmin(nested.NestedModelAdmin):
    list_display = ('reactivo', 'cantidad_de_existencias', 'chequeado_minit', 'precursor', 'toxico_arma_quimica',)
    search_fields = ['nombre', 'nombre_frasco', 'n_cas', 'n_nu', 'n_icsc', 'n_rtecs', 'n_ce', 'n_einecs', ]
    inlines = [SinonimosInline, ExistenciaInline, ]
    filter_horizontal = ['propiedades', ]
    list_filter = ('chequeado_minit', 'precursor', 'toxico_arma_quimica', 'propiedades')
    ordering = ['nombre', 'nombre_frasco']

    fieldsets = (
        ('Registro de los nombres', {
            'classes': ('wide',),
            'fields': (('nombre', 'nombre_frasco',),)
        }),
        ('Reglas', {
            'classes': ('collapse',),
            'fields': (('r_reglas', 's_reglas'),)
        }),
        ('Datos', {
            'classes': ('collapse',),
            'fields': (('n_cas', 'n_nu'), ('n_icsc', 'n_rtecs'), ('n_ce', 'n_einecs'),)
        }),
        ('Otros datos', {
            'classes': ('collapse',),
            'fields': (('precursor', 'toxico_arma_quimica', 'chequeado_minit'),
                       'observaciones', 'propiedades',)
        }),
    )

    list_per_page = 10

    def reactivo(self, obj):
        return obj.nombre_reactivo()

    def cantidad_de_existencias(self, obj):
        existencias = models.Existencia.objects.filter(reactivo_id=obj.id)

        suma = 0
        for existencia in existencias:
            suma += existencia.cantidad

        return suma

        # def get_search_results(self, request, queryset, search_term):
        #     queryset, use_distinct = super(ReactivosAdmin, self).get_search_results(request, queryset, search_term)
        #
        #     reactivos_sin_ids = models.Sinonimo.objects.filter(sinonimo__contains=str(search_term)).values_list(
        #         'reactivo_id', flat=True)
        #
        #     if queryset.exists():
        #         queryset |= queryset.filter(pk__in=list(reactivos_sin_ids))
        #     else:
        #         queryset |= models.Reactivo.objects.filter(pk__in=list(reactivos_sin_ids))
        #
        #     return queryset, use_distinct


admin.site.site_header = "Administracion del sitio SST"

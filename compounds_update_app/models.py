# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db import DatabaseError

from reactivos_sst_app.models import Local, EstadoReactivo, EstadoProducto, EstadoEnvase, TipoEnvase, MaterialEnvase, \
    Propiedad

from django.urls import reverse


def get_local_choices():
    try:
        locales = Local.objects.all()
        choices = []

        for local in locales:
            choices.append((local.nombre, local.nombre,))

        return choices
    except DatabaseError:
        return []


def get_generic_choices(model):
    try:
        objetos = model.objects.all()
        choices = []

        for objeto in objetos:
            choices.append((objeto.descripcion, objeto.descripcion,))

        return choices
    except DatabaseError:
        return []


def get_estados_usos():
    try:
        objetos = EstadoReactivo.objects.all()
        choices = []

        for objeto in objetos:
            choices.append((objeto.estado, objeto.estado,))

        return choices
    except DatabaseError:
        return []


def get_propiedade_choices():
    try:
        propiedades = Propiedad.objects.all()
        choices = []

        for propiedad in propiedades:
            choices.append((propiedad.propiedad, propiedad.propiedad,))

        return choices
    except DatabaseError:
        return []


# Create your models here.
class UserInfo(models.Model):
    choices = get_local_choices()

    user_auth = models.OneToOneField(User, related_name='user_info')
    local = models.CharField(max_length=200, choices=choices)

    def __str__(self):
        return self.user_auth.username

    class Meta:
        verbose_name = "Informacion adicional del usuario"
        verbose_name_plural = "Informacion de los usuarios"


class ReactivoUpdate(models.Model):
    nombre_frasco = models.CharField(max_length=200, verbose_name="Nombre de la etiqueta del frasco", null=True,
                                     blank=True)
    nombre = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nombre real")
    r_reglas = models.CharField(max_length=150, blank=True, null=True)
    s_reglas = models.CharField(max_length=150, blank=True, null=True)
    h_reglas = models.CharField(max_length=150, blank=True, null=True)
    p_reglas = models.CharField(max_length=150, blank=True, null=True)
    n_cas = models.CharField(max_length=150, blank=True, null=True, verbose_name="CAS",
                             help_text="Ejemplos: 19010-66-3, 62-38-4, etc")
    n_nu = models.CharField(max_length=150, blank=True, null=True, verbose_name="NU")
    n_icsc = models.CharField(max_length=150, blank=True, null=True, verbose_name="ICSC")
    n_rtecs = models.CharField(max_length=150, blank=True, null=True, verbose_name="RTECS",
                               help_text="Ejemplos: AE1225000, I3325000, etc")
    n_ce = models.CharField(max_length=150, blank=True, null=True, verbose_name="CE",
                            help_text="Ejemplos: 210-817-6, 006-045-00-2, 649-405-00-X etc")
    n_einecs = models.CharField(max_length=150, blank=True, null=True, verbose_name="EINECS",
                                help_text="Ejemplos: 252-104-2, 200-887-6, etc")
    peso_molecular = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso molecular", blank=True,
                                         null=True)

    local = models.CharField(max_length=200, blank=True, null=True, choices=get_local_choices(), default="UMEB")

    class Meta:
        unique_together = ('nombre_frasco', 'local')

    def get_absolute_url(self):
        return reverse('reactivo-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        reactivo_id = unicode(self.id)

        if self.nombre:
            reactivo_id = self.nombre
        elif self.nombre_frasco:
            reactivo_id = self.nombre_frasco

        return "reac. " + reactivo_id + self.local


class SinonimosUpdate(models.Model):
    reactivo = models.ForeignKey(ReactivoUpdate, related_name="sinonimos")
    sinonimo = models.CharField(max_length=150)

    class Meta:
        unique_together = ('reactivo', 'sinonimo')

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('reactivo', 'sinonimo'):
            return 'Unique together in sinonimos violate'
        else:
            return super(SinonimosUpdate, self).unique_error_message(model_class, unique_check)


class PropiedadUpdate(models.Model):
    reactivo = models.ForeignKey(ReactivoUpdate, on_delete=models.CASCADE)
    propiedad = models.CharField(max_length=200, choices=get_propiedade_choices())

    def __unicode__(self):
        return self.propiedad


class ExistenciaUpdate(models.Model):
    unidad_medidas_choices = (('mg', 'mg'),
                              ('cg', 'cg'),
                              ('dg', 'dg'),
                              ('g', 'g'),
                              ('dag', 'dag'),
                              ('hg', 'hg'),
                              ('kg', 'kg'),
                              ('lb', 'lb'),
                              ('ml', 'ml'),
                              ('cl', 'cl'),
                              ('dl', 'dl'),
                              ('litro', 'litro'),
                              ('dal', 'dal'),
                              ('hl', 'hl'),
                              ('kl', 'kl'))

    tipo_envases_choices = (('Pomo', 'Pomo'),
                            ('Caja', 'Caja'),
                            ('Tanque', 'Tanque'),
                            ('Lata', 'Lata'),
                            ('Saco', 'Saco')
                            )

    reactivo = models.ForeignKey(ReactivoUpdate, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField()
    unidad_medida = models.CharField(max_length=2, choices=unidad_medidas_choices, verbose_name="Unidad de medida",
                                     default='g')
    almacenamiento_idoneo = models.NullBooleanField(verbose_name="¿Es idoneo el almacenamiento?", default=True)

    # estados_envases = models.ManyToManyField(EstadoEnvase,
    #                                          through='RelExistenciaEstadoEnvase',
    #                                          through_fields=('existencia', 'estado'))
    # estados_productos = models.ManyToManyField(EstadoProducto,
    #                                            through='RelExistenciaEstadoProducto',
    #                                            through_fields=('existencia', 'estado'))
    # estados_reactivos = models.ManyToManyField(EstadoReactivo, through='RelExistenciaEstadoReactivo',
    #                                            through_fields=('existencia', 'estado'))

    tipo_envase = models.CharField(max_length=100, blank=True, null=True, choices=tipo_envases_choices)
    material_envase = models.CharField(max_length=100,
                                       choices=get_generic_choices(MaterialEnvase))
    firma = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('reactivo', 'capacidad', 'unidad_medida', 'tipo_envase', 'material_envase', 'firma')

    def __unicode__(self):
        reactivo_id = unicode(self.reactivo.id)

        if self.reactivo.nombre:
            reactivo_id = self.reactivo.nombre
        elif self.reactivo.nombre_frasco:
            reactivo_id = self.reactivo.nombre_frasco

        return "reac. " + reactivo_id + " cant. " + unicode(self.cantidad) + " cap. " + unicode(
            self.capacidad) + self.unidad_medida + " " + self.local.nombre + " firma " + self.firma


class EstadoEnvaseUp(models.Model):
    existencia = models.ForeignKey(ExistenciaUpdate)
    cantidad = models.PositiveIntegerField(blank=True, null=True)
    estado = models.CharField(max_length=50, choices=get_generic_choices(EstadoEnvase))

    class Meta:
        unique_together = ('estado', 'existencia')


class EstadoProductoUp(models.Model):
    existencia = models.ForeignKey(ExistenciaUpdate)
    cantidad = models.PositiveIntegerField(blank=True, null=True)
    estado = models.CharField(max_length=50, choices=get_generic_choices(EstadoProducto))

    class Meta:
        unique_together = ('estado', 'existencia')


class EstadoUsoReactivo(models.Model):
    existencia = models.ForeignKey(ExistenciaUpdate)
    cantidad = models.PositiveIntegerField(blank=True, null=True)
    estado = models.CharField(max_length=50, choices=get_estados_usos())

    class Meta:
        unique_together = ('estado', 'existencia')

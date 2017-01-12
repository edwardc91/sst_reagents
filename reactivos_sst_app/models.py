# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save
from django.utils import timezone

import re
import os
from termcolor import colored


# Create your models here.
class EstadoReactivo(models.Model):
    estado = models.CharField(max_length=50,verbose_name="Uso")

    class Meta:
        verbose_name = "Estado de uso de los reactivos"
        verbose_name_plural = "Estados de uso de los reactivos"

    def __unicode__(self):
        return self.uso


class Local(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Locales"

    def __unicode__(self):
        return self.nombre


class EstadoProducto(models.Model):
    estado = models.CharField(max_length=20, unique=True)
    descripcion = models.CharField(max_length=40, unique=True, default="")

    class Meta:
        verbose_name = "Estado de los productos"
        verbose_name_plural = "Estados de los productos"

    def __unicode__(self):
        return self.descripcion


class MaterialEnvase(models.Model):
    material = models.CharField(max_length=2, unique=True)
    descripcion = models.CharField(max_length=40, unique=True)

    class Meta:
        verbose_name = "Material de los envases"
        verbose_name_plural = "Materiales de los envases"

    def __unicode__(self):
        return self.descripcion


class EstadoEnvase(models.Model):
    estado = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Estado de los envases"
        verbose_name_plural = "Estados de los envases"

    def __unicode__(self):
        return self.descripcion


class TipoEnvase(models.Model):
    tipo = models.CharField(max_length=2)
    descripcion = models.CharField(max_length=20)
    material = models.ForeignKey(MaterialEnvase)

    class Meta:
        verbose_name = "Tipo de envases"
        verbose_name_plural = "Tipos de envases"
        unique_together = ('tipo', 'material')

    def __unicode__(self):
        return self.descripcion + "/" + self.material.descripcion


class ImagenPropiedad(models.Model):
    imagen = models.ImageField(upload_to='Images/Propiedades')

    class Meta:
        verbose_name = "Pictograma"
        verbose_name_plural = "Pictogramas"

    def __unicode__(self):
        mo = re.match(".+/(.+).png", self.imagen.name)

        result = mo.group(1)
        if result:
            return unicode(result)
        else:
            return unicode(self.imagen.name)


class Propiedad(models.Model):
    propiedad = models.CharField(max_length=60, unique=True)
    imagenes = models.ManyToManyField(ImagenPropiedad, related_name="propiedades")

    class Meta:
        verbose_name_plural = "Propiedades"

    def __unicode__(self):
        return self.propiedad


class Reactivo(models.Model):
    nombre = models.CharField(max_length=200, blank=True, null=True)
    nombre_frasco = models.CharField(max_length=200, verbose_name="Nombre del frasco", blank=True, null=True)
    r_reglas = models.CharField(max_length=150, blank=True, null=True)
    s_reglas = models.CharField(max_length=150, blank=True, null=True)
    n_cas = models.CharField(max_length=150, blank=True, null=True, unique=True)
    n_nu = models.CharField(max_length=150, blank=True, null=True)
    n_icsc = models.CharField(max_length=150, blank=True, null=True)
    n_rtecs = models.CharField(max_length=150, blank=True, null=True)
    n_ce = models.CharField(max_length=150, blank=True, null=True)
    n_einecs = models.CharField(max_length=150, blank=True, null=True)
    peso_molecular = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Peso molecular", blank=True,
                                         null=True)
    precursor = models.BooleanField(default=False, verbose_name="¿Es precursor?")
    toxico_arma_quimica = models.BooleanField(default=False, verbose_name="¿Quimico toxico para armas quimicas?")
    chequeado_minit = models.BooleanField(default=False,
                                          verbose_name="¿Es chequeado por el minit por su alta peligrosidad?")
    observaciones = models.TextField(blank=True, null=True)
    propiedades = models.ManyToManyField(Propiedad)

    def __unicode__(self):
        reactivo_id = unicode(self.id)

        if self.nombre:
            reactivo_id = self.nombre
        elif self.nombre_frasco:
            reactivo_id = self.nombre_frasco

        return "reac. " + reactivo_id

    def nombre_reactivo(self):
        reactivo_id = "ReactivoUpdate numero " + unicode(self.id)

        if self.nombre:
            reactivo_id = self.nombre
        elif self.nombre_frasco:
            reactivo_id = self.nombre_frasco

        return reactivo_id


class Sinonimo(models.Model):
    sinonimo = models.CharField(max_length=50, blank=True, null=True)
    reactivo = models.ForeignKey(Reactivo, related_name="sinonimos", on_delete=models.CASCADE)

    def __unicode__(self):
        reactivo_id = unicode(self.reactivo.id)

        if self.reactivo.nombre:
            reactivo_id = self.reactivo.nombre
        elif self.reactivo.nombre_frasco:
            reactivo_id = self.reactivo.nombre_frasco

        return reactivo_id + "/" + self.sinonimo


class Firma(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.nombre

class Existencia(models.Model):
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

    reactivo = models.ForeignKey(Reactivo, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    capacidad = models.PositiveIntegerField(default=1)
    unidad_medida = models.CharField(max_length=2, choices=unidad_medidas_choices, verbose_name="Unidad de medida",
                                     default='g')
    almacenamiento_idoneo = models.BooleanField(verbose_name="¿Es idoneo el almacenamiento?", default=True)
    estados_envases = models.ManyToManyField(EstadoEnvase,
                                             through='RelExistenciaEstadoEnvase',
                                             through_fields=('existencia', 'estado'))
    estados_productos = models.ManyToManyField(EstadoProducto,
                                               through='RelExistenciaEstadoProducto',
                                               through_fields=('existencia', 'estado'))
    estados_reactivos = models.ManyToManyField(EstadoReactivo, through='RelExistenciaEstadoReactivo',
                                               through_fields=('existencia', 'estado'))

    envase = models.ForeignKey(TipoEnvase)
    local = models.ForeignKey(Local)
    firma = models.ForeignKey(Firma)

    def __unicode__(self):
        reactivo_id = unicode(self.reactivo.id)

        if self.reactivo.nombre:
            reactivo_id = self.reactivo.nombre
        elif self.reactivo.nombre_frasco:
            reactivo_id = self.reactivo.nombre_frasco

        return "reac. " + reactivo_id + " cant. " + unicode(self.cantidad) + " cap. " + unicode(
            self.capacidad) + self.unidad_medida + " " + self.local.nombre + " firma " + self.firma.nombre


class RelExistenciaEstadoReactivo(models.Model):
    existencia = models.ForeignKey(Existencia, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoReactivo, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, help_text="Cant. de envases en ese estado")

    class Meta:
        unique_together = ('existencia', 'estado')
        verbose_name_plural = "Estados de los envases"
        verbose_name = "Estado de los envases"

    def __unicode__(self):
        return self.existencia.__unicode__() + "/" + self.estado.estado + "/" + unicode(self.cantidad)


class RelExistenciaEstadoEnvase(models.Model):
    existencia = models.ForeignKey(Existencia, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoEnvase, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, help_text="Cant. de envases en ese estado")

    class Meta:
        unique_together = ('existencia', 'estado')
        verbose_name_plural = "Estados de los envases"
        verbose_name = "Estado de los envases"

    def __unicode__(self):
        return self.existencia.__unicode__() + "/" + self.estado.estado + "/" + unicode(self.cantidad)


class RelExistenciaEstadoProducto(models.Model):
    existencia = models.ForeignKey(Existencia, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoProducto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0, help_text="Cant. de existencias en ese estado")

    class Meta:
        unique_together = ('existencia', 'estado')
        verbose_name_plural = "Estados de las existencias"
        verbose_name = "Estado de las existencias"

    def __unicode__(self):
        return self.existencia.__unicode__() + "/" + self.estado.estado + "/" + unicode(self.cantidad)


class GrupoPeligrosidad(models.Model):
    nombre = models.CharField(max_length=1, unique=True)
    descripcion = models.TextField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = "Grupo de Peligrosidad"
        verbose_name_plural = "Grupos de peligrosidad"

    def __unicode__(self):
        return self.nombre


class PeligroClasificacion(models.Model):
    reactivo = models.ForeignKey(Reactivo, null=True, blank=True)
    tipo = models.CharField(max_length=70)
    clasificacion = models.CharField(max_length=100)
    clasificacion_imco = models.CharField(max_length=4)
    no_onu = models.CharField(max_length=4)
    grupo = models.ManyToManyField(GrupoPeligrosidad)

    class Meta:
        verbose_name = "Clasificacion de peligrosidad"
        verbose_name_plural = "Clasificaciones de peligrosidad"

    def __unicode__(self):
        return self.tipo + "/" + self.clasificacion


@receiver(pre_delete, sender=ImagenPropiedad)
def _pictograma_delete(sender, instance, using, **kwargs):
    filedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(filedir, "statics/media/" + str(instance.imagen)).replace("\\", '/')

    # nueva = FicheroBorrar(archivoBorrar = instance.file)
    # nueva.save()

    if os.path.isfile(file_path):
        os.remove(file_path)
        text = colored(text="[" + str(
            timezone.now().strftime(
                '%d/%b/%Y %H:%M:%S')) + "] Pictogram \"" + file_path + "\" DELETED.",
                       color='red')
        print text


@receiver(pre_save, sender=ImagenPropiedad)
def _producto_update(instance, **kwargs):
    old_pictogram = ImagenPropiedad.objects.filter(pk=instance.id)
    filedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if old_pictogram.exists() and old_pictogram[0].foto_inicio != instance.foto_inicio:
        file_path = os.path.join(filedir, "statics/media/" + str(old_pictogram[0].imagen)).replace("\\", '/')

        if os.path.isfile(file_path):
            os.remove(file_path)
            text = colored(text="[" + str(
                timezone.now().strftime(
                    '%d/%b/%Y %H:%M:%S')) + "] Pictogram \"" + file_path + "\" DELETED on update.",
                           color='red')
            print text

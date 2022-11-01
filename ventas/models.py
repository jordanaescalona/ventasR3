from random import choices
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import format_html
#signals
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from django.shortcuts import get_object_or_404
#marca de agua
from PIL import Image,ImageDraw,ImageFont
FONT_PATH = "static/fonts/FiraMono-Bold.ttf"
FONT_SIZE = 25


# Create your models here.
ESTADO_CHOICES =(
    ('DISPONIBLE','Disponible'),
    ('VENDIDO','Vendido'),
    ('ALQUILADO','Alquilado'),
    ('RESERVADO','Reservado')
)

TIPO_CHOICES = (
    ('CASA1','Casa en Venta'),
    ('CASA2','Casa en Alquiler'),
    ('TERRENO1','Terreno en Venta'),
    ('TERRENO2','Terreno en Alquiler'),
    ('CAMPO_GANADERO1','Campo Ganadero en Venta'),
    ('CAMPO_GANADERO2','Campo Ganadero en Alquiler'),
    ('CAMPO_MIXTO1','Campo Mixto en Venta'),
    ('CAMPO_MIXTO2','Campo Mixto en Alquiler'),
    ('CAMPO_AGRICOLA1','Campo Agrícola en Venta'),
    ('CAMPO_AGRICOLA2','Campo Agrícola en Alquiler'),
    ('MAQUINARIA1','Maquinaria en Venta'),
    ('MAQUINARIA2','Maquinaria en Alquiler')
 )

TIPO_VENDEDOR =(
    ('Dueño','Dueño'),
    ('Comisionista','Comisionista')
)
MONEDA =(
    ('Pesos','Pesos'),
    ('Dolares','Dolares')
)
class Vendedor(models.Model):
    tipo = models.CharField(max_length=12,choices=TIPO_VENDEDOR,default="Comisionista")
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)

    def __str__(self):
        return format_html('{} ({}) <br>Contacto: {}',self.nombre,self.tipo,self.telefono)

    class Meta:
        verbose_name_plural = 'Vendedores'

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')
   

    def __str__(self):
        return str(self.imagen)

    class Meta:
        verbose_name_plural = 'Imagenes'
    
    

class Entidad(models.Model):
    estado = models.CharField(max_length=10,choices= ESTADO_CHOICES, default='DISPONIBLE')
    localidad = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50,choices=TIPO_CHOICES)
    moneda = models.CharField(max_length=7,choices=MONEDA,default = 'Dolares')
    precio = models.DecimalField(max_digits=20, decimal_places=2)
    ubicacion = models.TextField('Enlace de Google Maps',null=True,blank=True)
    descripcion = RichTextField(blank=True,null=True)
    vendedor = models.ForeignKey(Vendedor,on_delete=models.CASCADE,related_name="entidad_vendedor") 
    imagen = models.ManyToManyField(Imagen,blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.localidad}"

    class Meta:
        verbose_name_plural = 'Entidades'


    
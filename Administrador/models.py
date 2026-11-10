from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Create your models here.
class Conductor(models.Model):

    TIPO_LICENCIA = [
        ('A2', 'A2'),
        ('A3', 'A3'),
    ]

    rut = models.CharField(
        max_length=12,
        primary_key=True,
        verbose_name='RUT'
    )

    nombre_completo = models.CharField(
        max_length=200,
        verbose_name='Nombre completo'
    )

    direccion = models.CharField(
        max_length=200,
        verbose_name='Dirección'
    )

    fono_celular = models.CharField(
    max_length=9,
    verbose_name='Fono celular'
    )

    fono_domicilio = models.CharField(
        max_length=9,
        verbose_name='Fono domicilio'
    )

    fecha_incorporacion = models.DateField(
        verbose_name='Fecha de incorporación a CONATACOCH'
    )

    tipo_licencia = models.CharField(
        max_length=2,
        choices=TIPO_LICENCIA,
        verbose_name='Tipo de licencia de conducir'
    )

    municipio_licencia = models.CharField(
        max_length=100,
        verbose_name='Municipio que otorgó la licencia'
    )

    fecha_obtencion_licencia = models.DateField(
        verbose_name='Fecha de obtención de licencia'
    )

    duracion_licencia = models.PositiveIntegerField(
        verbose_name='Duración de licencia (años)'
    )

    fecha_vencimiento = models.DateField(
        verbose_name='Fecha de vencimiento'
    )

    def __str__(self):
        return "{} - {}".format(self.nombre_completo, self.rut)

    class Meta:
        db_table = 'conductor'
        verbose_name = 'Conductor'
        verbose_name_plural = 'Conductores'
        ordering = ['nombre_completo']

#--------- MODELO AUTOMOVIL -------------------

class Automovil(models.Model):

    COMBUSTIBLE_CHOICES = [
        ('gasolina', 'Gasolina'),
        ('diesel', 'Diésel'),
        ('gas', 'Gas'),
        ('electrico', 'Eléctrico'),
        ('hibrido', 'Híbrido'),
        ('glp', 'GLP'),
        ('gnc', 'GNC'),
        ('otro', 'Otro'),
    ]

    # Datos generales del automóvil

    marca = models.CharField(
        max_length=60,
        verbose_name='Marca'
    )

    modelo = models.CharField(
        max_length=80,
        verbose_name='Modelo'
    )

    anio = models.PositiveSmallIntegerField(
        verbose_name='Año'
    )

    combustible = models.CharField(
        max_length=20,
        choices=COMBUSTIBLE_CHOICES,
        verbose_name='Combustible'
    )

    patente = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Patente'
    )

    # Permiso de circulación

    permiso_comuna = models.CharField(
        max_length=100,
        verbose_name='Comuna del permiso de circulación'
    )

    permiso_fecha_otorgacion = models.DateField(
        verbose_name='Fecha de otorgación del permiso'
    )

    permiso_vencimiento = models.DateField(
        verbose_name='Vencimiento del permiso de circulación'
    )

    # Revisión técnica

    revision_planta = models.CharField(
        max_length=150,
        verbose_name='Planta de revisión técnica'
    )

    revision_comuna = models.CharField(
        max_length=100,
        verbose_name='Comuna de revisión técnica'
    )

    revision_vencimiento = models.DateField(
        verbose_name='Vencimiento de revisión técnica'
    )

    # Seguro obligatorio

    seguro_compania = models.CharField(
        max_length=150,
        verbose_name='Compañía de seguro'
    )

    seguro_prima = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Prima del seguro obligatorio'
    )

    seguro_vencimiento = models.DateField(
        verbose_name='Vencimiento del seguro obligatorio'
    )

    def clean(self):
        super().clean()

        if (
            self.permiso_fecha_otorgacion
            and self.permiso_vencimiento
            and self.permiso_vencimiento < self.permiso_fecha_otorgacion
        ):
            raise ValidationError({
                'permiso_vencimiento':
                'El vencimiento no puede ser anterior a la fecha de otorgación.'
            })

    def __str__(self):
        return "{} - {} {}".format(
            self.patente,
            self.marca,
            self.modelo
        )

    class Meta:
        db_table = 'automovil'
        verbose_name = 'Automóvil'
        verbose_name_plural = 'Automóviles'
        ordering = ['patente']
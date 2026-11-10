from django import forms
from Administrador.models import Conductor, Automovil


class ConductorForm(forms.ModelForm):

    rut = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 18306487-8'
        })
    )

    nombre_completo = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nombre completo'
        })
    )

    direccion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese dirección'
        })
    )

    fono_celular = forms.CharField(
    max_length=9,
    min_length=9,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ej: 912345678',
        'maxlength': '9',
        'pattern': '[0-9]{9}'
        })
    )

    fono_domicilio = forms.CharField(
    max_length=9,
    min_length=9,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ej: 223456789',
        'maxlength': '9',
        'pattern': '[0-9]{9}'
        })
    )

    fecha_incorporacion = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    tipo_licencia = forms.ChoiceField(
        choices=Conductor.TIPO_LICENCIA,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    municipio_licencia = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese municipio'
        })
    )

    fecha_obtencion_licencia = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    duracion_licencia = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese duración en años'
        })
    )

    fecha_vencimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Conductor
        fields = '__all__'


#--------- FORMULARIO AUTOMOVIL -------------------

class AutomovilForm(forms.ModelForm):

    class Meta:
        model = Automovil
        fields = '__all__'

        widgets = {

            # Datos generales

            'marca': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese marca'
            }),

            'modelo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese modelo'
            }),

            'anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese año',
                'min': '1900'
            }),

            'combustible': forms.Select(attrs={
                'class': 'form-control'
            }),

            'patente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: AB-CD-12',
                'maxlength': '10'
            }),

            # Permiso de circulación

            'permiso_comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese comuna'
            }),

            'permiso_fecha_otorgacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'permiso_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            # Revisión técnica

            'revision_planta': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese planta de revisión'
            }),

            'revision_comuna': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese comuna'
            }),

            'revision_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            # Seguro obligatorio

            'seguro_compania': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese compañía de seguro'
            }),

            'seguro_prima': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese prima',
                'min': '0',
                'step': '0.01'
            }),

            'seguro_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_patente(self):
        patente = self.cleaned_data['patente']
        return patente.strip().upper().replace(' ', '')


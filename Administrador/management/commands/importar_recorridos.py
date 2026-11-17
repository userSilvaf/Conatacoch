from django.core.management.base import BaseCommand, CommandError
from Administrador.models import Recorrido
from openpyxl import load_workbook
from pathlib import Path


class Command(BaseCommand):

    help = 'Importa los recorridos desde el archivo Excel'

    def handle(self, *args, **options):

        # Ubicación del archivo Excel
        archivo = (
            Path(__file__).resolve().parents[3]
            / 'datos'
            / 'Transporte Público - Julio 2026.xlsx'
        )

        if not archivo.exists():
            raise CommandError(
                f'No se encontró el archivo: {archivo}'
            )

        # Evitar importar el mismo catálogo accidentalmente
        if Recorrido.objects.exists():
            raise CommandError(
                'Ya existen recorridos en la base de datos. '
                'Se canceló la importación para evitar duplicados.'
            )

        self.stdout.write('Leyendo archivo Excel...')

        libro = load_workbook(
            archivo,
            read_only=True,
            data_only=True
        )

        nombre_hoja = 'O_D Recorridos'

        if nombre_hoja not in libro.sheetnames:
            raise CommandError(
                f'No existe la hoja {nombre_hoja} en el Excel.'
            )

        hoja = libro[nombre_hoja]

        encabezados = [
            str(celda).strip()
            for celda in next(hoja.iter_rows(values_only=True))
        ]

        campos_requeridos = [
            'REGION',
            'FOLIO',
            'TIPO_SERVICIO',
            'NOMBRE_RECORRIDO',
            'TIPO_TRAZADO',
            'NOMBRE_ORIGEN',
            'COMUNA_ORIGEN',
            'DOMICILIO_ORIGEN',
            'NOMBRE_DESTINO',
            'COMUNA_DESTINO',
            'DOMICILIO_DESTINO'
        ]

        if encabezados != campos_requeridos:
            raise CommandError(
                'Los encabezados del Excel no coinciden '
                'con los esperados.'
            )

        def convertir_texto(valor):
            if valor is None:
                return None

            return str(valor).strip()

        recorridos = []
        errores = []

        for numero_fila, valores in enumerate(
            hoja.iter_rows(min_row=2, values_only=True),
            start=2
        ):

            if all(valor is None for valor in valores):
                continue

            datos = dict(zip(encabezados, valores))

            try:
                recorrido = Recorrido(
                    region=int(datos['REGION']),
                    folio=int(datos['FOLIO']),
                    tipo_servicio=convertir_texto(
                        datos['TIPO_SERVICIO']
                    ),
                    nombre_recorrido=convertir_texto(
                        datos['NOMBRE_RECORRIDO']
                    ),
                    tipo_trazado=convertir_texto(
                        datos['TIPO_TRAZADO']
                    ),
                    nombre_origen=convertir_texto(
                        datos['NOMBRE_ORIGEN']
                    ),
                    comuna_origen=convertir_texto(
                        datos['COMUNA_ORIGEN']
                    ),
                    domicilio_origen=convertir_texto(
                        datos['DOMICILIO_ORIGEN']
                    ),
                    nombre_destino=convertir_texto(
                        datos['NOMBRE_DESTINO']
                    ),
                    comuna_destino=convertir_texto(
                        datos['COMUNA_DESTINO']
                    ),
                    domicilio_destino=convertir_texto(
                        datos['DOMICILIO_DESTINO']
                    )
                )

                recorridos.append(recorrido)

            except (TypeError, ValueError) as error:
                errores.append(
                    f'Fila {numero_fila}: {error}'
                )

        if errores:
            raise CommandError(
                'Se encontraron errores en el Excel:\n'
                + '\n'.join(errores[:20])
            )

        self.stdout.write(
            f'Importando {len(recorridos)} recorridos...'
        )

        Recorrido.objects.bulk_create(
            recorridos,
            batch_size=500
        )

        libro.close()

        self.stdout.write(
            self.style.SUCCESS(
                f'Importación completada: '
                f'{len(recorridos)} recorridos registrados.'
            )
        )

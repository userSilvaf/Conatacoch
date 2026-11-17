from django.shortcuts import render, redirect, get_object_or_404
from Administrador.forms import (
    ConductorForm,
    AutomovilForm,
    RecorridoAsignacionForm,
    AutomovilAsignacionForm
)
from Administrador.models import Conductor, Automovil, Recorrido
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q, CharField
from django.db.models.functions import Cast

#--------- INICIO -------------------

def pagina_principal(request):
    return render(request, 'Template.html')


#--------- CRUD CONDUCTORES -------------------

@login_required
def todos_conductores(request):
    conductores = Conductor.objects.all()

    data = {
        'conductores': conductores
    }

    return render(request, 'conductores.html', data)


@login_required
def crear_conductor(request):
    if request.method == 'POST':
        form = ConductorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('conductores')
    else:
        form = ConductorForm()

    return render(request, 'conductorADD.html', {'form': form})


@login_required
def cargar_editar_conductor(request, conductor_rut):
    conductor = get_object_or_404(Conductor, rut=conductor_rut)

    form = ConductorForm(instance=conductor)

    return render(request, 'conductorEdit.html', {
        'form': form,
        'conductor': conductor
    })


@login_required
def editar_conductor(request, conductor_rut):
    conductor = get_object_or_404(Conductor, rut=conductor_rut)

    if request.method == 'POST':
        form = ConductorForm(request.POST, instance=conductor)

        if form.is_valid():
            form.save()
            return redirect('conductores')
    else:
        form = ConductorForm(instance=conductor)

    return render(request, 'conductorEdit.html', {
        'form': form,
        'conductor': conductor
    })


@login_required
def eliminar_conductor(request, conductor_rut):
    conductor = get_object_or_404(Conductor, rut=conductor_rut)

    if request.method == 'POST':
        conductor.delete()
        return redirect('conductores')

    return render(request, 'conductorDel.html', {
        'conductor': conductor
    })


#--------- CRUD AUTOMOVILES -------------------

@login_required
def todos_automoviles(request):
    automoviles = Automovil.objects.all()

    data = {
        'automoviles': automoviles
    }

    return render(request, 'autos/automoviles.html', data)


@login_required
def crear_automovil(request):
    if request.method == 'POST':
        form = AutomovilForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('automoviles')
    else:
        form = AutomovilForm()

    return render(request, 'autos/automovilADD.html', {'form': form})


@login_required
def cargar_editar_automovil(request, automovil_id):
    automovil = get_object_or_404(Automovil, id=automovil_id)

    form = AutomovilForm(instance=automovil)

    return render(request, 'autos/automovilEdit.html', {
        'form': form,
        'automovil': automovil
    })


@login_required
def editar_automovil(request, automovil_id):
    automovil = get_object_or_404(Automovil, id=automovil_id)

    if request.method == 'POST':
        form = AutomovilForm(request.POST, instance=automovil)

        if form.is_valid():
            form.save()
            return redirect('automoviles')
    else:
        form = AutomovilForm(instance=automovil)

    return render(request, 'autos/automovilEdit.html', {
        'form': form,
        'automovil': automovil
    })


@login_required
def eliminar_automovil(request, automovil_id):
    automovil = get_object_or_404(Automovil, id=automovil_id)

    if request.method == 'POST':
        automovil.delete()
        return redirect('automoviles')

    return render(request, 'autos/automovilDel.html', {
        'automovil': automovil
    })

#--------- ASIGNACION DE RECORRIDOS -------------------

@login_required
def asignar_recorrido(request, automovil_id):

    automovil = get_object_or_404(Automovil, id=automovil_id)

    if request.method == 'POST':

        form = RecorridoAsignacionForm(
            request.POST,
            instance=automovil
        )

        if form.is_valid():
            form.save()
            return redirect('automoviles')

    else:

        form = RecorridoAsignacionForm(
            instance=automovil
        )

    automoviles = Automovil.objects.all()

    return render(request, 'autos/automoviles.html', {
        'automoviles': automoviles,
        'recorrido_form': form,
        'automovil_seleccionado': automovil
    })



#--------- BUSQUEDA DE RECORRIDOS -------------------

@login_required
def buscar_recorridos(request):

    termino = request.GET.get('q', '').strip()

    if not termino:
        return JsonResponse({'recorridos': []})

    recorridos = (
        Recorrido.objects
        .annotate(
            region_texto=Cast('region', CharField()),
            folio_texto=Cast('folio', CharField())
        )
        .filter(
            Q(region_texto__icontains=termino) |
            Q(folio_texto__icontains=termino) |
            Q(nombre_recorrido__icontains=termino) |
            Q(nombre_origen__icontains=termino) |
            Q(comuna_origen__icontains=termino) |
            Q(domicilio_origen__icontains=termino) |
            Q(nombre_destino__icontains=termino) |
            Q(comuna_destino__icontains=termino) |
            Q(domicilio_destino__icontains=termino)
        )
        .order_by('region', 'folio', 'nombre_recorrido')[:25]
    )

    resultados = []

    for recorrido in recorridos:

        origen = recorrido.comuna_origen or recorrido.nombre_origen
        destino = recorrido.comuna_destino or recorrido.nombre_destino

        resultados.append({
            'id': recorrido.id,
            'nombre': (
                f'Región {recorrido.region} | '
                f'Folio {recorrido.folio} | '
                f'{recorrido.nombre_recorrido}'
            ),
            'detalle': f'{origen} → {destino}'
        })

    return JsonResponse({
        'recorridos': resultados
    })



@login_required
@require_POST
def quitar_recorrido(request, automovil_id):

    automovil = get_object_or_404(Automovil, id=automovil_id)

    automovil.recorrido = None
    automovil.save(update_fields=['recorrido'])

    return redirect('automoviles')

#--------- ASIGNACION DE AUTOMOVILES -------------------

@login_required
def asignar_automovil(request, conductor_rut):

    conductor = get_object_or_404(Conductor, rut=conductor_rut)

    automoviles_disponibles = Automovil.objects.filter(
        Q(conductor__isnull=True) |
        Q(conductor=conductor)
    )

    if request.method == 'POST':

        form = AutomovilAsignacionForm(request.POST)

        form.fields['automovil'].queryset = automoviles_disponibles

        if form.is_valid():

            automovil = form.cleaned_data['automovil']

            automovil.conductor = conductor
            automovil.save(update_fields=['conductor'])

            return redirect('conductores')

    else:

        form = AutomovilAsignacionForm()

        form.fields['automovil'].queryset = automoviles_disponibles

    return render(request, 'asignarAutomovil.html', {
        'conductor': conductor,
        'form': form
    })


@login_required
@require_POST
def quitar_automovil(request, conductor_rut):

    conductor = get_object_or_404(Conductor, rut=conductor_rut)

    automovil = get_object_or_404(
        Automovil,
        conductor=conductor
    )

    automovil.conductor = None
    automovil.save(update_fields=['conductor'])

    return redirect('conductores')

from django.shortcuts import render, redirect, get_object_or_404
from Administrador.forms import ConductorForm, AutomovilForm
from Administrador.models import Conductor, Automovil
from django.contrib.auth.decorators import login_required


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

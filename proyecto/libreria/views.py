from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ProductoTemporada, Receta
from .forms import ProductoTemporadaForm, RecetaForm
from datetime import datetime

# Decorador para verificar si es superusuario
def is_admin(user):
    return user.is_superuser

# Diccionario para traducir meses
MESES_EN_ESPANOL = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre',
}

# Mapear meses a estaciones
MES_A_ESTACION = {
    'Enero': 'Verano',
    'Febrero': 'Verano',
    'Marzo': 'Otoño',
    'Abril': 'Otoño',
    'Mayo': 'Otoño',
    'Junio': 'Invierno',
    'Julio': 'Invierno',
    'Agosto': 'Invierno',
    'Septiembre': 'Primavera',
    'Octubre': 'Primavera',
    'Noviembre': 'Primavera',
    'Diciembre': 'Verano',
}

# Estructura de estaciones para el calendario
ESTACIONES = {
    'Primavera': ['Septiembre', 'Octubre', 'Noviembre'],
    'Verano': ['Diciembre', 'Enero', 'Febrero'],
    'Otoño': ['Marzo', 'Abril', 'Mayo'],
    'Invierno': ['Junio', 'Julio', 'Agosto'],
}

def inicio(request):
    # Obtener el mes actual
    mes_actual_ingles = datetime.now().strftime('%B')
    mes_actual = MESES_EN_ESPANOL.get(mes_actual_ingles, 'Abril')  # Fallback a Abril si falla
    
    # Obtener el mes seleccionado desde la URL, o usar el mes actual
    mes_seleccionado = request.GET.get('mes', mes_actual)
    
    # Validar que el mes seleccionado sea válido, si no, usar el actual
    if mes_seleccionado not in MESES_EN_ESPANOL.values():
        mes_seleccionado = mes_actual
    
    # Mapear el mes a estación
    estacion_seleccionada = MES_A_ESTACION.get(mes_seleccionado, 'Otoño')
    
    # Filtrar productos por estación
    productos = ProductoTemporada.objects.filter(estación__contains=estacion_seleccionada)
    
    return render(request, 'paginas/inicio.html', {
        'productos': productos,
        'estacion': estacion_seleccionada,
        'estaciones': ESTACIONES,
        'mes_seleccionado': mes_seleccionado,
        'mes_actual': mes_actual,
    })

# Resto de las vistas sin cambios...
def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def productos_temporada(request):
    mes_seleccionado = request.GET.get('mes', datetime.now().strftime('%B'))
    mes_actual_ingles = datetime.now().strftime('%B')
    mes_seleccionado_es = MESES_EN_ESPANOL.get(mes_seleccionado, MESES_EN_ESPANOL[mes_actual_ingles])
    estacion_seleccionada = MES_A_ESTACION.get(mes_seleccionado_es, 'Primavera')
    productos = ProductoTemporada.objects.filter(estación__contains=estacion_seleccionada)
    
    return render(request, 'productos/index.html', {
        'productos': productos,
        'estacion': estacion_seleccionada
    })

def detalle_producto(request, id):
    producto = get_object_or_404(ProductoTemporada, id=id)
    recetas = Receta.objects.filter(producto=producto)
    return render(request, 'productos/detalle.html', {'producto': producto, 'recetas': recetas})

@login_required
@user_passes_test(is_admin)
def crear_producto(request):
    formulario = ProductoTemporadaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('productos_temporada')
    return render(request, 'productos/crear.html', {'formulario': formulario})

@login_required
@user_passes_test(is_admin)
def editar_producto(request, id):
    producto = get_object_or_404(ProductoTemporada, id=id)
    formulario = ProductoTemporadaForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('productos_temporada')
    return render(request, 'productos/editar.html', {'formulario': formulario})

@login_required
@user_passes_test(is_admin)
def eliminar_producto(request, id):
    producto = get_object_or_404(ProductoTemporada, id=id)
    producto.delete()
    return redirect('productos_temporada')



@login_required
@user_passes_test(is_admin)
def crear_receta(request, producto_id):
    producto = get_object_or_404(ProductoTemporada, id=producto_id)
    formulario = RecetaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        receta = formulario.save(commit=False)
        receta.producto = producto
        receta.save()
        return redirect('detalle_producto', id=producto.id)  # Cambiado
    return render(request, 'recetas/crear.html', {'formulario': formulario, 'producto': producto})

@login_required
@user_passes_test(is_admin)
def editar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    formulario = RecetaForm(request.POST or None, request.FILES or None, instance=receta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('detalle_producto', id=receta.producto.id)  # Cambiado
    return render(request, 'recetas/editar.html', {'formulario': formulario, 'receta': receta})

@login_required
@user_passes_test(is_admin)
def eliminar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    producto_id = receta.producto.id
    receta.delete()
    return redirect('detalle_producto', id=producto_id)  # Cambiado

def detalle_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    return render(request, 'recetas/detalle.html', {'receta': receta})
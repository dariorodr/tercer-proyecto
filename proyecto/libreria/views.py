from django.shortcuts import render, get_object_or_404, redirect
from .models import ProductoTemporada, Receta
from .forms import ProductoTemporadaForm, RecetaForm
from datetime import datetime

def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def productos_temporada(request):
    mes_actual = datetime.now().strftime('%B').capitalize()
    productos = ProductoTemporada.objects.filter(meses_temporada__contains=mes_actual)
    return render(request, 'productos/index.html', {'productos': productos, 'mes': mes_actual})

def crear_producto(request):
    formulario = ProductoTemporadaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('productos_temporada')
    return render(request, 'productos/crear.html', {'formulario': formulario})

def editar_producto(request, id):
    producto = get_object_or_404(ProductoTemporada, id=id)
    formulario = ProductoTemporadaForm(request.POST or None, request.FILES or None, instance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('productos_temporada')
    return render(request, 'productos/editar.html', {'formulario': formulario})

def eliminar_producto(request, id):
    producto = get_object_or_404(ProductoTemporada, id=id)
    producto.delete()
    return redirect('productos_temporada')

def recetas_por_producto(request, producto_id):
    producto = get_object_or_404(ProductoTemporada, id=producto_id)
    recetas = Receta.objects.filter(producto=producto)
    return render(request, 'recetas/index.html', {'producto': producto, 'recetas': recetas})

def crear_receta(request, producto_id):
    producto = get_object_or_404(ProductoTemporada, id=producto_id)
    formulario = RecetaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        receta = formulario.save(commit=False)
        receta.producto = producto
        receta.save()
        return redirect('recetas_por_producto', producto_id=producto.id)
    return render(request, 'recetas/crear.html', {'formulario': formulario, 'producto': producto})

def editar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    formulario = RecetaForm(request.POST or None, request.FILES or None, instance=receta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('recetas_por_producto', producto_id=receta.producto.id)
    return render(request, 'recetas/editar.html', {'formulario': formulario, 'receta': receta})

def eliminar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    producto_id = receta.producto.id
    receta.delete()
    return redirect('recetas_por_producto', producto_id=producto_id)

def detalle_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    return render(request, 'recetas/detalle.html', {'receta': receta})
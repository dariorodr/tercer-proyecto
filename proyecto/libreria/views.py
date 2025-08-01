from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages  
from django.http import JsonResponse
from .models import ProductoTemporada, Receta
from .forms import ProductoTemporadaForm, RecetaForm
from datetime import datetime
import requests
import json
import base64
from django.conf import settings

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
    mes_actual_ingles = datetime.now().strftime('%B')
    mes_actual = MESES_EN_ESPANOL.get(mes_actual_ingles, 'Mayo')
    mes_seleccionado = request.GET.get('mes', mes_actual).capitalize()
    query = request.GET.get('q', '').strip()

    # Validar mes_seleccionado
    if mes_seleccionado not in MESES_EN_ESPANOL.values():
        mes_seleccionado = mes_actual

    estacion_seleccionada = MES_A_ESTACION.get(mes_seleccionado, 'Otoño')
    productos = ProductoTemporada.objects.filter(estación__contains=estacion_seleccionada)

    if query:
        if len(query) < 3:
            productos = ProductoTemporada.objects.none()
        else:
            productos = productos.filter(nombre__icontains=query)

    return render(request, 'paginas/inicio.html', {
        'productos': productos,
        'estacion': estacion_seleccionada,
        'estaciones': ESTACIONES,
        'mes_seleccionado': mes_seleccionado,
        'mes_actual': mes_actual,
        'query': query,
    })


def buscar_productos(request):
    query = request.GET.get('q', '').strip()
    
    productos = ProductoTemporada.objects.all()
    if query:
        # Obtener productos que comienzan con la consulta
        starts_with = productos.filter(nombre__istartswith=query).order_by('nombre')
        # Obtener productos que contienen la consulta, excluyendo los que ya comienzan con ella
        contains = productos.filter(nombre__icontains=query).exclude(nombre__istartswith=query).order_by('nombre')
        # Combinar, priorizando starts_with
        productos = list(starts_with) + list(contains)
    else:
        productos = productos.order_by('nombre')

    resultados = [{'id': p.id, 'nombre': p.nombre} for p in productos]
    return JsonResponse({'resultados': resultados})

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def detalle_producto(request, id):
    producto = get_object_or_404(ProductoTemporada, id=id)
    recetas = Receta.objects.filter(producto=producto)
    receta_temporal = request.session.get(f'receta_temporal_{id}', None)
    if not recetas.exists() and not receta_temporal:
        messages.info(request, f'No hay recetas disponibles para {producto.nombre}. ¡Prueba generar una con IA!')
    context = {
        'producto': producto,
        'recetas': recetas,
        'receta_temporal': receta_temporal,
    }
    return render(request, 'productos/detalle.html', context)

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
        return redirect('detalle_producto', id=producto.id)
    return render(request, 'recetas/crear.html', {'formulario': formulario, 'producto': producto})

@login_required
@user_passes_test(is_admin)
def editar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    formulario = RecetaForm(request.POST or None, request.FILES or None, instance=receta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('detalle_producto', id=receta.producto.id)
    return render(request, 'recetas/editar.html', {'formulario': formulario, 'receta': receta})

@login_required
@user_passes_test(is_admin)
def eliminar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    producto_id = receta.producto.id
    receta.delete()
    return redirect('detalle_producto', id=producto_id)

def detalle_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    if not receta.titulo or not receta.ingredientes or not receta.preparacion:
        messages.warning(request, 'Esta receta está incompleta. Algunos datos no están disponibles.')
    context = {
        'receta': receta,
    }
    return render(request, 'recetas/detalle.html', context)
    
def generar_receta_ia(request, producto_id):
    producto = get_object_or_404(ProductoTemporada, id=producto_id)
    recetas_persistentes = producto.recetas.all()
    receta_temporal = request.session.get(f'receta_temporal_{producto_id}')

    if request.method == 'POST':
        prompt_texto = f"Generá una receta usando {producto.nombre} como ingrediente principal. Devuelve la respuesta en formato JSON con los campos: titulo (string), ingredientes (string), preparacion (string), tiempo_preparacion (integer, en minutos), dificultad (string, 'Fácil', 'Media' o 'Difícil')."
        headers = {
            'Authorization': f'Bearer {settings.HF_API_KEY}',
            'Content-Type': 'application/json',
        }
        data_texto = {
            'inputs': prompt_texto,
            'parameters': {'max_length': 500},
        }

        try:
            # Llamada a la API para texto
            response_texto = requests.post(
                'https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1',
                json=data_texto,
                headers=headers,
                timeout=10
            )
            response_texto.raise_for_status()
            response_json = response_texto.json()

            # Extraer el JSON de la receta
            generated_text = response_json[0]['generated_text']
            json_start = generated_text.find('{')
            if json_start == -1:
                raise ValueError("No se encontró un JSON válido en la respuesta.")
            json_str = generated_text[json_start:]
            receta_data = json.loads(json_str)

            # Generar imagen con Stable Diffusion XL
            prompt_imagen = f"Plato de comida con {producto.nombre}, estilo apetitoso, iluminación suave, fondo limpio"
            data_imagen = {'inputs': prompt_imagen}
            response_imagen = requests.post(
                'https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0',
                json=data_imagen,
                headers=headers,
                timeout=10
            )
            response_imagen.raise_for_status()

            # Codificar imagen en base64
            imagen_base64 = base64.b64encode(response_imagen.content).decode('utf-8')
            receta_data['imagen_base64'] = f"data:image/png;base64,{imagen_base64}"
            receta_data['es_temporal'] = True

            # Guardar en sesión
            request.session[f'receta_temporal_{producto_id}'] = receta_data
            request.session.modified = True

            messages.success(request, f'Receta generada exitosamente para {producto.nombre}.')
            return redirect('generar_receta_ia', producto_id=producto_id)

        except requests.RequestException as e:
            messages.error(request, f'Error de conexión con la API: {str(e)}')
        except json.JSONDecodeError:
            messages.error(request, 'Error al procesar la respuesta de la API: formato JSON inválido.')
        except ValueError as e:
            messages.error(request, f'Error en los datos generados: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error inesperado al generar la receta: {str(e)}')
        return redirect('generar_receta_ia', producto_id=producto_id)

    return render(request, 'productos/detalle.html', {
        'producto': producto,
        'recetas': recetas_persistentes,
        'receta_temporal': receta_temporal,
    })
    
def custom_404(request, exception):
    return render(request, 'paginas/404.html', status=404)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('productos/', views.productos_temporada, name='productos_temporada'),
    path('productos/<int:id>/', views.detalle_producto, name='detalle_producto'),  # Nueva ruta
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/<int:producto_id>/', views.recetas_por_producto, name='recetas_por_producto'),
    path('producto/<int:producto_id>/crear/', views.crear_receta, name='crear_receta'),
    path('receta/editar/<int:id>/', views.editar_receta, name='editar_receta'),
    path('receta/eliminar/<int:id>/', views.eliminar_receta, name='eliminar_receta'),
    path('receta/<int:id>/', views.detalle_receta, name='detalle_receta'),
]
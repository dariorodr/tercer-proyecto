from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError('La imagen no debe superar los 5MB.')

class ProductoTemporada(models.Model):
    nombre = models.CharField(max_length=100)
    estación = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, validators=[validate_image_size])

    def __str__(self):
        return self.nombre

class Receta(models.Model):
    titulo = models.CharField(max_length=100)
    producto = models.ForeignKey(ProductoTemporada, on_delete=models.CASCADE, related_name='recetas')
    ingredientes = models.TextField()
    preparacion = models.TextField()
    tiempo_preparacion = models.IntegerField()
    dificultad = models.CharField(max_length=20, choices=[
        ('Fácil', 'Fácil'),
        ('Media', 'Media'),
        ('Difícil', 'Difícil')
    ])
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True, validators=[validate_image_size])
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validar límite de 5 recetas por producto
        if self.producto and self.producto.recetas.count() >= 5 and not self.id:
            raise ValidationError(f'No se pueden agregar más de 5 recetas para {self.producto.nombre}.')


    def __str__(self):
        return self.titulo
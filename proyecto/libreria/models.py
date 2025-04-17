from django.db import models
from django.contrib.auth.models import User

class ProductoTemporada(models.Model):
    nombre = models.CharField(max_length=100)
    estación = models.CharField(max_length=100)  # Ej. "Enero, Febrero"
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Receta(models.Model):
    titulo = models.CharField(max_length=100)
    producto = models.ForeignKey(ProductoTemporada, on_delete=models.CASCADE)
    ingredientes = models.TextField()
    preparacion = models.TextField()
    tiempo_preparacion = models.IntegerField()
    dificultad = models.CharField(
        max_length=20,
        choices=[('Fácil', 'Fácil'), ('Media', 'Media'), ('Difícil', 'Difícil')]
    )
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
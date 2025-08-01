# Generated by Django 5.0.7 on 2025-03-30 03:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0004_tumodelo_descripcion_alter_tumodelo_nombre'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoTemporada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('meses_temporada', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='productos/')),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('ingredientes', models.TextField()),
                ('preparacion', models.TextField()),
                ('tiempo_preparacion', models.IntegerField()),
                ('dificultad', models.CharField(choices=[('Fácil', 'Fácil'), ('Media', 'Media'), ('Difícil', 'Difícil')], max_length=20)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='recetas/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('autor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.productotemporada')),
            ],
        ),
        migrations.DeleteModel(
            name='Libro',
        ),
        migrations.DeleteModel(
            name='TuModelo',
        ),
    ]

from django.db import models #Librería para crear modelos
from django.contrib.auth.models import AbstractUser #Librería para crear usuarios

class Carrera(models.Model):
    nombre_carrera = models.CharField("Nombre de la Carrera", max_length=100)

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"

    #Personaliza la representación de los objetos en la interfaz de administración
    def __str__(self):
        return self.nombre_carrera

class Seccion(models.Model):
    codigo_seccion = models.CharField("Código de la Sección", max_length=20, unique=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, verbose_name="Carrera")
    
    class Meta:
        verbose_name = "Sección"
        verbose_name_plural = "Secciones"

    def __str__(self):
        return f"{self.codigo_seccion} - {self.carrera}"

class Usuario(AbstractUser): #Los demás atributos vienen de AbstractUser
    cedula = models.IntegerField("Cédula de Identidad", unique=True, null=True, blank=True)
    seccion_base = models.ForeignKey(Seccion, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sección Base")

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    REQUIRED_FIELDS = ['cedula'] #Requerido para cuando se crea un usuario desde la terminal

    #username es requerido por Django, por lo que se debe personalizar para que use la cédula como username
    def save(self, *args, **kwargs):
        if self.cedula:
            self.username = str(self.cedula)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cedula})"

#models.Model es una clase base que proporciona funcionalidades comunes para todos los modelos en Django
#Esta clase hace posible que Django genere la tabla correspondiente en la base de datos
#La clase Meta, define de manera personalizada lo que realmente verá el usuario en la interfaz de administración respecto a su modelo

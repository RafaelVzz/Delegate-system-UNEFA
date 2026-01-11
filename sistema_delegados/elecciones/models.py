from django.db import models
from django.conf import settings

class Materia(models.Model):
    nombre_materia = models.CharField("Nombre de la Materia", max_length=100)
    codigo_materia = models.CharField("Código", max_length=20)
    seccion = models.ForeignKey('core.Seccion', on_delete=models.CASCADE, verbose_name="Sección")
    delegado_actual = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='delegado_de',
        verbose_name="Delegado Actual"
    )

    class Meta:
        verbose_name = "Materia"
        verbose_name_plural = "Materias"

    def __str__(self):
        return f"{self.nombre_materia} ({self.seccion})"

class Eleccion(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, verbose_name="Materia")
    token_acceso = models.CharField("Token de Acceso", max_length=20)
    candidatos = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='postulaciones', blank=True, verbose_name="Candidatos")
    fecha_creacion = models.DateTimeField("Fecha de Creación", auto_now_add=True)
    esta_activa = models.BooleanField("Estado (Activa)", default=True)

    class Meta:
        verbose_name = "Elección"
        verbose_name_plural = "Elecciones"

    def __str__(self):
        return f"Elección {self.materia} - {'Activa' if self.esta_activa else 'Cerrada'}"

class Voto(models.Model):
    eleccion = models.ForeignKey(Eleccion, on_delete=models.CASCADE, verbose_name="Elección")
    usuario_votante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votos_emitidos', verbose_name="Estudiante que votó")
    usuario_candidato = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votos_recibidos', verbose_name="Candidato votado")

    class Meta:
        unique_together = ('eleccion', 'usuario_votante')
        verbose_name = "Voto"
        verbose_name_plural = "Votos"

    def __str__(self):
        return f"Voto de {self.usuario_votante} en {self.eleccion}"

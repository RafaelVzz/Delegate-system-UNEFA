from django.shortcuts import render, get_object_or_404, redirect
from django.utils.crypto import get_random_string #Cadena ramdom para generar el token de acceso
from django.contrib.auth.decorators import login_required #Decorador para verificar que el usuario esté autenticado
from django.db.models import Count #Contar votos
from django.contrib import messages #Mensajes para el usuario
from .models import Materia, Eleccion, Voto #Modelos de elecciones
from core.models import Usuario, Seccion, Carrera #Modelos de usuarios, secciones y carreras
from django.http.request import HttpRequest #Solicitud HTTP

@login_required
def dashboard(request):
    carreras = Carrera.objects.all() #Obtener todas las carreras
    
    seccion_id = request.GET.get('seccion')
    carrera_id = request.GET.get('carrera')
    
    selected_seccion = None
    selected_carrera = None

    if carrera_id: #Si en la URL se pide (GET) una carrera en espeífico (id de carrera)
        selected_carrera = get_object_or_404(Carrera, id=carrera_id)
        secciones = Seccion.objects.filter(carrera=selected_carrera)
    else:
        secciones = Seccion.objects.all()

    materias = []
    
    if seccion_id: #Si en la URL se pide (GET) una sección en espeífico (id de sección)
        selected_seccion = get_object_or_404(Seccion, id=seccion_id)
        # Verify the section belongs to the selected career if both are present
        if selected_carrera and selected_seccion.carrera != selected_carrera:
            selected_seccion = None
            materias = []
            messages.warning(request, "La sección no pertenece a la carrera seleccionada.")
        else:
            materias = Materia.objects.filter(seccion=selected_seccion)

    #El tecer argumento que se la pasa a la función render, es el contexto para la plantilla html que corresponda a este método (en este caso dashboard.html)

    return render(request, 'elecciones/dashboard.html', {
        'carreras': carreras,
        'secciones': secciones,
        'materias': materias,
        'selected_seccion': selected_seccion,
        'selected_carrera': selected_carrera
    })

@login_required
def materia_detalle(request: HttpRequest, materia_id):
    materia = get_object_or_404(Materia, id=materia_id) #Obtener la materia
    eleccion_activa = Eleccion.objects.filter(materia=materia, esta_activa=True).first() #Obtener la elección activa
    
    if request.method == 'POST':
        if 'convocar' in request.POST:
            user_carrera = None
            if request.user.seccion_base and request.user.seccion_base.carrera: #Si existe una sección base para el usuario
                user_carrera = request.user.seccion_base.carrera
            
            materia_carrera = materia.seccion.carrera
            
            if user_carrera != materia_carrera:
                 messages.error(request, "Solo estudiantes de la misma carrera pueden convocar la elección.")
                 return redirect('materia_detalle', materia_id=materia_id)

            if not eleccion_activa:
                token = get_random_string(5, allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                Eleccion.objects.create(materia=materia, token_acceso=token) #INSERT INTO Eleccion (materia_id, token_acceso) VALUES (materia_id, token)
                messages.success(request, f"Elección convocada. Token: {token}")
            return redirect('materia_detalle', materia_id=materia_id)
            
        elif 'verificar_token' in request.POST:
            token_ingresado = request.POST.get('token')
            if eleccion_activa and token_ingresado.upper() == eleccion_activa.token_acceso:
                # token correcto
                request.session[f'can_vote_{eleccion_activa.id}'] = True
                return redirect('votar_eleccion', eleccion_id=eleccion_activa.id)
            else:
                messages.error(request, "Token incorrecto.")
        
        elif 'cerrar_eleccion' in request.POST:
            if eleccion_activa:
                return cerrar_eleccion_logic(request, eleccion_activa)

    user_carrera = None
    if request.user.seccion_base and request.user.seccion_base.carrera: 
        user_carrera = request.user.seccion_base.carrera
        
    materia_carrera = materia.seccion.carrera
    puede_convocar = (user_carrera == materia_carrera)

    # Lógica de asignacón automática para el usuario que ganó la elección
    mostrar_modal_asignacion = False
    materias_vacias = []

    if materia.delegado_actual is not None: #Si el delegado de la materia que se está viendo no es nulo
        if materia.delegado_actual == request.user: #Si el usuario que ganó la elección es el que esta haciendo la solicitud http
            if request.user.seccion_base == materia.seccion: #Si el usuario que ganó la elección pertenece a la misma sección que la materia
                materias_vacias = Materia.objects.filter(seccion=materia.seccion, delegado_actual__isnull=True).exclude(id=materia.id) #SELECT * FROM Materia WHERE seccion_id = materia.seccion_id AND delegado_actual IS NULL AND id != materia.id
                if materias_vacias.exists():
                    mostrar_modal_asignacion = True

    return render(request, 'elecciones/materia_detalle.html', {
        'materia': materia,
        'eleccion': eleccion_activa,
        'puede_convocar': puede_convocar,
        'mostrar_modal_asignacion': mostrar_modal_asignacion,
        'materias_vacias': materias_vacias
    })

@login_required
def votar_eleccion(request, eleccion_id):
    eleccion = get_object_or_404(Eleccion, id=eleccion_id)
    if not eleccion.esta_activa:
        messages.error(request, "La elección ha finalizado.")
        return redirect('materia_detalle', materia_id=eleccion.materia.id)

    if not request.session.get(f'can_vote_{eleccion.id}'):
        return redirect('materia_detalle', materia_id=eleccion.materia.id)

    # Verificar si ya votó
    if Voto.objects.filter(eleccion=eleccion, usuario_votante=request.user).exists():
        messages.warning(request, "Ya has votado en esta elección.")
        return redirect('materia_detalle', materia_id=eleccion.materia.id)
        
    candidatos = eleccion.candidatos.all()
    es_candidato = eleccion.candidatos.filter(id=request.user.id).exists() #SELECT * FROM Usuario WHERE id = request.user.id AND id IN (SELECT candidato_id FROM Eleccion WHERE id = eleccion_id)

    if request.method == 'POST':
        if 'postularse' in request.POST:
            if not es_candidato:
                eleccion.candidatos.add(request.user)
                messages.success(request, "Te has postulado exitosamente.")
            return redirect('votar_eleccion', eleccion_id=eleccion.id)
            
        candidato_id = request.POST.get('candidato')
        if candidato_id:
            candidato = get_object_or_404(Usuario, id=candidato_id)
            
            # Verificar si el candidato es válido (está en la lista de candidatos)
            if not eleccion.candidatos.filter(id=candidato.id).exists():
                messages.error(request, "El candidato seleccionado no es válido.")
                return redirect('votar_eleccion', eleccion_id=eleccion.id)

            Voto.objects.create(
                eleccion=eleccion,
                usuario_votante=request.user,
                usuario_candidato=candidato
            ) #INSERT INTO Voto (eleccion_id, usuario_votante_id, usuario_candidato_id) VALUES (eleccion_id, usuario_votante_id, usuario_candidato_id)
            messages.success(request, "Voto registrado.")
            return redirect ('materia_detalle', materia_id=eleccion.materia.id)

    return render(request, 'elecciones/votar.html', {
        'eleccion': eleccion,
        'estudiantes': candidatos,
        'es_candidato': es_candidato
    })

def cerrar_eleccion_logic(request, eleccion):
    eleccion.esta_activa = False
    eleccion.save()
    
    # Contar votos
    resultados = Voto.objects.filter(eleccion=eleccion).values('usuario_candidato').annotate(total=Count('id')).order_by('-total') #SELECT usuario_candidato_id, COUNT(*) FROM Voto WHERE eleccion_id = eleccion_id GROUP BY usuario_candidato_id ORDER BY COUNT(*) DESC
    
    if resultados:
        ganador_id = resultados[0]['usuario_candidato'] #Accede al primer resultado (id del ganador)    
        ganador = Usuario.objects.get(id=ganador_id) #SELECT * FROM Usuario WHERE id = ganador_id
        
        materia = eleccion.materia
        materia.delegado_actual = ganador
        materia.save() #UPDATE Materia SET delegado_actual_id = ganador_id WHERE id = eleccion.materia_id
        
        messages.success(request, f"Elección cerrada. Ganador: {ganador}")
        
    return redirect('materia_detalle', materia_id=eleccion.materia.id)  

@login_required
def confirmar_auto_asignacion(request):
    if request.method == 'POST':
        ganador_id = request.POST.get('ganador_id')
        ganador = get_object_or_404(Usuario, id=ganador_id)
        materias_ids = request.POST.getlist('materias')
        
        for mid in materias_ids:
            mat = Materia.objects.get(id=mid)
            mat.delegado_actual = ganador
            mat.save()
        
        messages.success(request, "Delegado asignado a materias adicionales.")
        return redirect('dashboard')
    return redirect('dashboard')

import os
import sys
import django

# 1. Configurar Entorno de Django
# Agregamos la carpeta 'sistema_delegados' al path para que Python encuentre los módulos
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'sistema_delegados'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_delegados.settings')
django.setup()

# 2. Importaciones (Una vez configurado Django)
from core.models import Carrera, Seccion, Usuario
from elecciones.models import Materia

def main():
    print('--- INICIANDO CARGA MASIVA DE DATOS UNIVERSITARIOS ---')

    # ==========================================
    # DICCIONARIO MAESTRO DE DATOS
    # Estructura: "Carrera": { "CODIGO_CARRERA": { Semestre (int): [ ("Materia", "Código"), ... ] } }
    # ==========================================
    
    UNIVERSIDAD_DATA = {
        # 1. INGENIERÍA DE SISTEMAS (2603)
        "Ingeniería de Sistemas": {
            "CODIGO": "2603",
            "MATERIAS": {
                1: [
                    ("Educación Ambiental", "ADG-25132"),
                    ("Hombre, Sociedad, Ciencia y Tec.", "ADG-25123"),
                    ("Inglés I", "IDM-24113"),
                    ("Dibujo", "MAT-21212"),
                    ("Matemática I", "MAT-21215"),
                    ("Geometría Analítica", "MAT-21524"),
                    ("Seminario I", "ADG-25131"),
                    ("Defensa Integral de la Nación I", "DIN-21113"),
                ],
                2: [
                    ("Inglés II", "IDM-24123"),
                    ("Química General", "QUF-22014"),
                    ("Física I", "QUF-23015"),
                    ("Matemática II", "MAT-21225"),
                    ("Álgebra Lineal", "MAT-21114"),
                    ("Seminario II", "ADG-25141"),
                    ("Defensa Integral de la Nación II", "DIN-21123"),
                ],
                3: [
                    ("Física II", "QUF-23025"),
                    ("Matemática III", "MAT-21235"),
                    ("Probabilidades y Estadística", "MAT-21414"),
                    ("Programación", "SYC-22113"),
                    ("Sistemas Administrativos", "AGG-22313"),
                    ("Defensa Integral de la Nación III", "DIN-21133"),
                ],
                4: [
                    ("Teoría de los Sistemas", "SYC-32114"),
                    ("Cálculo Numérico", "MAT-31714"),
                    ("Lógica Matemática", "MAT-31214"),
                    ("Lenguajes de Programación I", "SYC-32225"),
                    ("Procesamiento de Datos", "SYC-32414"),
                    ("Sistemas de Producción", "AGL-30214"),
                    ("Defensa Integral de la Nación IV", "DIN-31143"),
                ],
                5: [
                    ("Teoría de Grafos", "MAT-31114"),
                    ("Lenguajes de Programación II", "SYC-32235"),
                    ("Investigación de Operaciones", "MAT-30925"),
                    ("Circuitos Lógicos", "ELN-30514"),
                    ("Análisis de Sistemas", "SYC-32514"),
                    ("Bases de Datos", "SYC-32614"),
                    ("Defensa Integral de la Nación V", "DIN-31153"),
                ],
                6: [
                    ("Optimización No Lineal", "MAT-30935"),
                    ("Lenguajes de Programación III", "SYC-32245"),
                    ("Procesos Estocásticos", "MAT-31414"),
                    ("Arquitectura del Computador", "SYC-30525"),
                    ("Diseño de Sistemas", "SYC-32524"),
                    ("Sistemas Operativos", "SYC-30834"),
                    ("Defensa Integral de la Nación VI", "DIN-31163"),
                ],
                7: [
                    ("Implantación de Sistemas", "SYC-32714"),
                    ("Metodología de la Investigación", "ADG-30214"),
                    ("Simulación y Modelos", "MAT-30945"),
                    ("Redes", "SYC-31644"),
                    ("Gerencia de la Informática", "ADG-30224"),
                    ("Electiva Técnica", "ELEC-TEC-SIS-07"),
                    ("Electiva No Técnica", "ELEC-NOT-SIS-07"),
                    ("Defensa Integral de la Nación VII", "DIN-31173"),
                ],
                8: [
                    ("Teoría de Decisiones", "MAT-31314"),
                    ("Auditoría de Sistemas", "SYC-32814"),
                    ("Marco Legal Para el Ejercicio de la Ing.", "CJU-37314"),
                    ("Teleprocesos", "TTC-31154"),
                    ("Electiva Técnica", "ELEC-TEC-SIS-08"),
                    ("Electiva No Técnica", "ELEC-NOT-SIS-08"),
                    ("Defensa Integral de la Nación VIII", "DIN-31183"),
                ]
            }
        },

        # 2. INGENIERÍA MECÁNICA (2403)
        "Ingeniería Mecánica": {
            "CODIGO": "2403",
            "MATERIAS": {
                1: [
                    ("Educación Ambiental", "ADG-25132"),
                    ("Hombre, Sociedad, Ciencia y Tec.", "ADG-25123"),
                    ("Inglés I", "IDM-24113"),
                    ("Dibujo", "MAT-21212"),
                    ("Matemática I", "MAT-21215"),
                    ("Geometría Analítica", "MAT-21524"),
                    ("Seminario I", "ADG-25131"),
                    ("Defensa Integral de la Nación I", "DIN-21113"),
                ],
                2: [
                    ("Inglés II", "IDM-24123"),
                    ("Química General", "QUF-22014"),
                    ("Física I", "QUF-23015"),
                    ("Matemática II", "MAT-21225"),
                    ("Álgebra Lineal", "MAT-21114"),
                    ("Seminario II", "ADG-25141"),
                    ("Defensa Integral de la Nación II", "DIN-21123"),
                ],
                3: [
                    ("Física II", "QUF-23025"),
                    ("Matemática III", "MAT-21235"),
                    ("Probabilidades y Estadística", "MAT-21414"),
                    ("Programación", "SYC-22113"),
                    ("Cálculo Numérico", "MAT-20814"), # Código distinto a Sistemas
                    ("Defensa Integral de la Nación III", "DIN-21133"),
                ],
                4: [
                    ("Matemáticas Aplic. a la Ingeniería", "MAT-30265"),
                    ("Mecánica", "MEC-30115"),
                    ("Termodinámica I", "QUF-30315"),
                    ("Geometría Descriptiva", "MAT-30123"),
                    ("Informática", "SYC-30114"),
                    ("Elem. de Ciencias de Materiales y Metalurgia", "MEC-30314"),
                    ("Defensa Integral de la Nación IV", "DIN-31143"),
                ],
                5: [
                    ("Termodinámica II", "QUF-30325"),
                    ("Electrotecnia", "ELC-30315"),
                    ("Resistencia de los Materiales", "MEC-30215"),
                    ("Mecánica de los Fluidos", "MEC-30414"),
                    ("Dibujo Mecánico", "MEC-30124"),
                    ("Procesos de Fabricación I", "MEC-30614"),
                    ("Defensa Integral de la Nación V", "DIN-31153"),
                ],
                6: [
                    ("Mecanismos", "MEC-30134"),
                    ("Transferencia de Calor", "QUF-30514"),
                    ("Sistemas", "SYC-30814"),
                    ("Dinámica de Gases", "MEC-30714"),
                    ("Procesos de Fabricación II", "MEC-30625"),
                    ("Metodología de la Investigación", "ADG-30214"),
                    ("Defensa Integral de la Nación VI", "DIN-31163"),
                ],
                7: [
                    ("Vibraciones Mecánicas", "MEC-30915"),
                    ("Diseño de Elementos de Máquinas I", "MEC-30815"),
                    ("Higiene y Seguridad Industrial", "AGP-30213"),
                    ("Mantenimiento General", "AGM-30315"),
                    ("Electiva Técnica", "ELEC-TEC-MEC-07"),
                    ("Electiva No Técnica", "ELEC-NOT-MEC-07"),
                    ("Defensa Integral de la Nación VII", "DIN-31173"),
                ],
                8: [
                    ("Diseño de Elementos de Máquinas II", "MEC-30825"),
                    ("Turbomáquinas", "MEC-31015"),
                    ("Generación de Potencia", "MEC-31115"),
                    ("Marco Legal Para el Ejercicio de la Ing.", "CJU-37314"),
                    ("Electiva Técnica", "ELEC-TEC-MEC-08"),
                    ("Electiva No Técnica", "ELEC-NOT-MEC-08"),
                    ("Defensa Integral de la Nación VIII", "DIN-31183"),
                ]
            }
        },

        # 3. INGENIERÍA CIVIL (1303)
        "Ingeniería Civil": {
            "CODIGO": "1303",
            "MATERIAS": {
                1: [
                    ("Educación Ambiental", "ADG-25132"),
                    ("Hombre, Sociedad, Ciencia y Tec.", "ADG-25123"),
                    ("Inglés I", "IDM-24113"),
                    ("Dibujo", "MAT-21212"),
                    ("Matemática I", "MAT-21215"),
                    ("Geometría Analítica", "MAT-21524"),
                    ("Seminario I", "ADG-25131"),
                    ("Defensa Integral de la Nación I", "DIN-21113"),
                ],
                2: [
                    ("Inglés II", "IDM-24123"),
                    ("Química General", "QUF-22014"),
                    ("Física I", "QUF-23015"),
                    ("Matemática II", "MAT-21225"),
                    ("Álgebra Lineal", "MAT-21114"),
                    ("Seminario II", "ADG-25141"),
                    ("Defensa Integral de la Nación II", "DIN-21123"),
                ],
                3: [
                    ("Física II", "QUF-23025"),
                    ("Matemática III", "MAT-21235"),
                    ("Probabilidades y Estadística", "MAT-21414"),
                    ("Programación", "SYC-22113"),
                    ("Cálculo Numérico", "MAT-20714"), # Código diferente a Mecánica/Sistemas
                    ("Defensa Integral de la Nación III", "DIN-21133"),
                ],
                4: [
                    ("Geometría Descriptiva", "MAT-30123"),
                    ("Topografía", "CIV-30115"),
                    ("Geología Aplicada", "CIV-30123"),
                    ("Mecánica de los Fluidos", "MEC-30414"),
                    ("Estática", "MEC-31615"),
                    ("Resistencia de Materiales", "MEC-31814"),
                    ("Electiva No Técnica", "ELEC-NOT-CIV-04"),
                    ("Defensa Integral de la Nación IV", "DIN-31143"),
                ],
                5: [
                    ("Materiales y Ensayos", "CIV-30314"),
                    ("Dinámica", "MEC-31714"),
                    ("Hidrología", "CIV-30213"),
                    ("Mecánica de los Suelos", "CIV-30144"),
                    ("Vías de Comunicación", "CIV-30615"),
                    ("Instalaciones Eléctricas", "CIV-31024"),
                    ("Dibujo de Proyectos", "CIV-31713"),
                    ("Defensa Integral de la Nación V", "DIN-31153"),
                ],
                6: [
                    ("Administración de Obras", "AGG-31113"),
                    ("Acueductos y Cloacas", "CIV-31115"),
                    ("Teoría de Estructuras I", "CIV-30415"),
                    ("Ingeniería de Tránsito", "CIV-30623"),
                    ("Mantenimiento Gral. de Obras Civiles", "AGM-31013"),
                    ("Arquitectura y Urbanismo", "CIV-30713"),
                    ("Proyectos de Acero", "CIV-30514"),
                    ("Electiva No Técnica", "ELEC-NOT-CIV-06"),
                    ("Defensa Integral de la Nación VI", "DIN-31163"),
                ],
                7: [
                    ("Concreto Armado", "CIV-30915"),
                    ("Teoría de Estructuras II", "CIV-30425"),
                    ("Diseño de Obras Hidráulicas", "CIV-31214"),
                    ("Metodología de la Investigación", "ADG-30214"),
                    ("Ferrocarriles", "CIV-30653"),
                    ("Pavimentos", "CIV-30813"),
                    ("Planificación y Eval. de Proyectos", "AGG-31513"),
                    ("Defensa Integral de la Nación VII", "DIN-31173"),
                ],
                8: [
                    ("Fundaciones y Muros", "CIV-31314"),
                    ("Marco Legal Para el Ejercicio de la Ing.", "CJU-37314"),
                    ("Ingeniería Sísmica", "CIV-31514"),
                    ("Puentes", "CIV-31614"),
                    ("Concreto Precomprimido", "CIV-31414"),
                    ("Electiva Técnica I", "ELEC-TEC1-CIV-08"),
                    ("Electiva Técnica II", "ELEC-TEC2-CIV-08"),
                    ("Defensa Integral de la Nación VIII", "DIN-31183"),
                ]
            }
        },

        # 4. INGENIERÍA AGROINDUSTRIAL (1903)
        "Ingeniería Agroindustrial": {
            "CODIGO": "1903",
            "MATERIAS": {
                1: [
                    ("Educación Ambiental", "ADG-25132"),
                    ("Hombre, Sociedad, Ciencia y Tec.", "ADG-25123"),
                    ("Inglés I", "IDM-24113"),
                    ("Dibujo", "MAT-21212"),
                    ("Matemática I", "MAT-21215"),
                    ("Geometría Analítica", "MAT-21524"),
                    ("Seminario I", "ADG-25131"),
                    ("Defensa Integral de la Nación I", "DIN-21113"),
                ],
                2: [
                    ("Inglés II", "IDM-24123"),
                    ("Química General", "QUF-22014"),
                    ("Física I", "QUF-23015"),
                    ("Matemática II", "MAT-21225"),
                    ("Álgebra Lineal", "MAT-21114"),
                    ("Seminario II", "ADG-25141"),
                    ("Defensa Integral de la Nación II", "DIN-21123"),
                ],
                3: [
                    ("Física II", "QUF-23025"),
                    ("Matemática III", "MAT-21235"),
                    ("Probabilidades y Estadística", "MAT-21414"),
                    ("Programación", "SYC-22113"),
                    ("Química Orgánica", "QUF-21114"),
                    ("Defensa Integral de la Nación III", "DIN-21133"),
                ],
                4: [
                    ("Introducción a la Ing. Agroindustrial", "AGI-35113"),
                    ("Biología", "BIO-34114"),
                    ("Ecología", "AGI-35122"),
                    ("Fisicoquímica", "QUI-33214"),
                    ("Bioquímica", "QUI-33223"),
                    ("Iniciativa Empresarial", "ADG-36112"),
                    ("Defensa Integral de la Nación IV", "DIN-31143"),
                ],
                5: [
                    ("Estadística Aplicada a la Agroindustrial", "MAT-31113"),
                    ("Alimentación y Nutrición", "AGI-35412"),
                    ("Balance de Materia y Energía", "QUI-33233"),
                    ("Microbiología de Alimentos", "BIO-34214"),
                    ("Materias Primas Agropecuarias", "AGI-35213"),
                    ("Conservación y Transformación de Alimentos", "AGI-35244"),
                    ("Economía y Mercadeo Agroindustrial", "ECN-32214"),
                    ("Defensa Integral de la Nación V", "DIN-31153"),
                ],
                6: [
                    ("Operaciones Unitarias", "AGI-35144"),
                    ("Tecnología Agrícola", "AGI-35314"),
                    ("Administración Financiera y de la Prod.", "AGG-32113"),
                    ("Diagnóstico y Control de Plagas", "AGI-35233"),
                    ("Tecnología de Alimentos de Origen Animal", "AGI-35344"),
                    ("Metodología de la Investigación", "ADG-30214"),
                    ("Electiva Técnica", "ELEC-TEC-AGR-06"),
                    ("Defensa Integral de la Nación VI", "DIN-31163"),
                ],
                7: [
                    ("Control de Calidad", "AGG-36143"),
                    ("Planificación y Gestión de Proyectos", "ADG-36134"),
                    ("Higiene y Seguridad Industrial", "AGI-35264"),
                    ("Seminario de Investigación Social", "ADG-30914"),
                    ("Electiva No Técnica", "ELEC-NOT-AGR-07"),
                    ("Defensa Integral de la Nación VII", "DIN-31173"),
                ],
                8: [
                    ("Sanidad Animal", "ADG-35253"),
                    ("Marco Legal Para el Ejercicio de la Ing.", "CJU-37314"),
                    ("Normas Ambientales para la Agroindustria", "CJU-37142"),
                    ("Electiva Técnica", "ELEC-TEC-AGR-08"),
                    ("Electiva No Técnica", "ELEC-NOT-AGR-08"),
                    ("Defensa Integral de la Nación VIII", "DIN-31183"),
                ]
            }
        },

        # 5. T.S.U EN TURISMO (0603)
        "T.S.U en Turismo": {
            "CODIGO": "0603",
            "MATERIAS": {
                1: [
                    ("Educación Ambiental", "ADG-15112"),
                    ("Inglés I", "IDM-12113"),
                    ("Matemática", "MAT-11113"),
                    ("Historia Económica y Social de Venezuela", "SOC-13112"),
                    ("Administración", "AYE-17113"),
                    ("Fundamentos del Turismo", "HYT-14213"),
                    ("Electiva de Idioma I", "ELEC-IDI1-TUR-01"),
                    ("Defensa Integral de la Nación I", "DIN-11113"),
                ],
                2: [
                    ("Informática", "SYC-16124"),
                    ("Inglés II", "IDM-12124"),
                    ("Estadística", "MAT-11214"),
                    ("Geografía Turística", "SOC-13214"),
                    ("Administración Turística", "AYE-17124"),
                    ("Electiva de Idioma II", "ELEC-IDI2-TUR-02"),
                    ("Defensa Integral de la Nación II", "DIN-11123"),
                ],
                3: [
                    ("Contabilidad General", "MAT-11224"),
                    ("Inglés III", "IDM-12134"),
                    ("Economía", "AYE-17213"),
                    ("Mercadeo y Promoción Turística", "HYT-14233"),
                    ("Técnicas Turísticas", "HYT-14224"),
                    ("Gerencia", "ADG-15163"),
                    ("Electiva de Idioma III", "ELEC-IDI3-TUR-03"),
                    ("Defensa Integral de la Nación III", "DIN-11133"),
                ],
                4: [
                    ("Tráfico Aéreo", "HYT-14243"),
                    ("Inglés IV", "IDM-12144"),
                    ("Legislación y Ética Profesional", "HYT-14114"),
                    ("Eventos y Recreación", "ADG-15133"),
                    ("Relaciones Públicas, Protocolo y Etiqueta", "ADG-15174"),
                    ("Finanzas y Presupuesto", "AYE-17224"),
                    ("Redacción de Informes Técnicos", "ADG-10243"),
                    ("Defensa Integral de la Nación IV", "DIN-11143"),
                ]
            }
        }
    }

    # ==========================================
    # EJECUCIÓN DE CARGA
    # ==========================================

    for nombre_carrera, datos in UNIVERSIDAD_DATA.items():
        cod_carrera = datos["CODIGO"]
        
        # 1. Crear Carrera
        carrera, created = Carrera.objects.get_or_create(nombre_carrera=nombre_carrera) 
        if created:
            print(f"--> CREANDO CARRERA: {nombre_carrera}")
        else:
            print(f"--> PROCESANDO: {nombre_carrera}")

        # 2. Iterar por semestres
        for semestre_num, lista_materias in datos["MATERIAS"].items():
            
            # Construir Código Sección (Ej: 05S-2603-D1)
            # Formato: 01S, 02S... 05S
            semestre_str = str(semestre_num).zfill(2)
            codigo_seccion = f"{semestre_str}S-{cod_carrera}-D1"

            # 3. Crear Sección
            # Nota: Asumimos 'D1' como sección fija por defecto en este script
            seccion, created = Seccion.objects.get_or_create(
                codigo_seccion=codigo_seccion,
                defaults={'carrera': carrera}
            )

            # 4. Crear Materias
            for nombre_materia, codigo_materia in lista_materias:
                materia, m_created = Materia.objects.get_or_create(
                    codigo_materia=codigo_materia,
                    seccion=seccion,
                    defaults={'nombre_materia': nombre_materia}
                )
                
                if m_created:
                    pass 
                    # print(f"   + Agregada: {nombre_materia}")
    
    # IMPORTANTE: Los bloques comentados de creación de usuarios permanecen comentados
    # pero han sido adaptados al nuevo contexto si se descomentan.

    # CREACIÓN DE USUARIOS BASE (ADMIN y PRUEBA)
    # if not Usuario.objects.filter(username='admin').exists():
    #     Usuario.objects.create_superuser('admin', 'admin@email.com', 'admin')
    #     print('--> Superusuario "admin" creado.')

    # # Usuario de Prueba: Pedro (Sistemas 5to Semestre)
    # try:
    #     seccion_pedro = Seccion.objects.get(codigo_seccion="05S-2603-D1")
    #     if not Usuario.objects.filter(cedula=1001).exists():
    #         Usuario.objects.create_user(
    #             username='1001', 
    #             cedula=1001, 
    #             password='1234', 
    #             first_name='Pedro', 
    #             last_name='Pérez', 
    #             seccion_base=seccion_pedro
    #         )
    #         print('--> Usuario de prueba "Pedro" (Sistemas 5to) creado.')
    # except Seccion.DoesNotExist:
    #     print("Error: No se encontró la sección de Pedro.")
    
    # # Otros usuarios (compañeros, arrastre) seguirían la misma lógica...

    print('\n¡CARGA COMPLETA! TODA LA UNIVERSIDAD ESTÁ EN LA BASE DE DATOS.')

if __name__ == '__main__':
    main()

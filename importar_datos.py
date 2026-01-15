import os
import sys
import django

# Configurar Django
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'sistema_delegados'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_delegados.settings')
django.setup()

from django.core.management import call_command

print('Importando datos desde datos_backup.json...')
print('IMPORTANTE: Asegurate de haber ejecutado las migraciones primero!')
print('')

try:
    # Importar los datos
    call_command('loaddata', 'datos_backup.json')
    print('')
    print('Datos importados exitosamente!')
    print('Tu base de datos ahora tiene todos los datos de SQLite.')
except Exception as e:
    print(f'Error al importar datos: {e}')
    print('')
    print('Asegurate de:')
    print('1. Haber ejecutado: python sistema_delegados/manage.py migrate')
    print('2. Que el archivo datos_backup.json exista')

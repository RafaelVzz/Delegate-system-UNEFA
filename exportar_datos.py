import os
import sys
import django

# Configurar Django
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, 'sistema_delegados'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_delegados.settings')
django.setup()

from django.core.management import call_command

print('Exportando datos de la base de datos SQLite...')

# Exportar todos los datos a un archivo JSON
with open('datos_backup.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', 
                 '--natural-foreign', 
                 '--natural-primary',
                 '--indent', '2',
                 '--exclude', 'contenttypes',
                 '--exclude', 'auth.permission',
                 stdout=f)

print('Datos exportados exitosamente a: datos_backup.json')
print('Este archivo contiene todos tus datos y se puede importar en cualquier base de datos.')

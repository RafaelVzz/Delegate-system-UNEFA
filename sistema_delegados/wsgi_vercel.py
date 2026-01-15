import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_delegados.settings')

application = get_wsgi_application()

# Vercel necesita que la variable se llame 'app'
app = application

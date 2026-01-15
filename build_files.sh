#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python sistema_delegados/manage.py collectstatic --noinput --clear

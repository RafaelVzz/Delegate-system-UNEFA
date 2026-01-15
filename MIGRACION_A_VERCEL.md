# Guía de Migración de SQLite a PostgreSQL en Vercel

## ✅ Paso 1: Datos Exportados (YA HECHO)

Tus datos de SQLite han sido exportados exitosamente a: **`datos_backup.json`**

Este archivo contiene:
- Todas las carreras (Ingeniería de Sistemas, Mecánica, Civil, Agroindustrial, T.S.U en Turismo)
- Todas las secciones
- Todas las materias
- Todos los usuarios (si los tienes)
- Todas las elecciones y votos

---

## 🚀 Paso 2: Crear Base de Datos PostgreSQL en Vercel

### Opción A: Vercel Postgres (Recomendado - Gratis)

1. Ve a tu proyecto en Vercel Dashboard
2. Click en la pestaña **Storage**
3. Click en **Create Database**
4. Selecciona **Postgres**
5. Elige el plan **Free** (Hobby)
6. Click en **Create**

Vercel automáticamente creará estas variables de entorno:
```
POSTGRES_URL
POSTGRES_PRISMA_URL
POSTGRES_URL_NON_POOLING
POSTGRES_USER
POSTGRES_HOST
POSTGRES_PASSWORD
POSTGRES_DATABASE
```

### Opción B: Supabase (Alternativa Gratis)

1. Ve a [supabase.com](https://supabase.com)
2. Crea un nuevo proyecto
3. Copia las credenciales de conexión
4. Configura manualmente las variables en Vercel

---

## 🔧 Paso 3: Configurar Variables de Entorno en Vercel

Ve a tu proyecto en Vercel → **Settings** → **Environment Variables**

### Variables Obligatorias:

```bash
# Django
SECRET_KEY=django-insecure-y4f23#=pk3!h@m9tsy3%*!41-abp_wd%+(iv(orca@tt10k+(5
DEBUG=False
ALLOWED_HOSTS=.vercel.app

# Base de Datos PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=verceldb
DB_USER=default
DB_PASSWORD=[tu_password_de_vercel]
DB_HOST=[tu_host_de_vercel].postgres.vercel-storage.com
DB_PORT=5432

# Email (Opcional)
EMAIL_HOST_USER=rafa1234.univ@gmail.com
EMAIL_HOST_PASSWORD=xfbr cpnr ggro bxea
```

**IMPORTANTE**: Si usas Vercel Postgres, las variables ya estarán configuradas automáticamente. Solo necesitas agregar:
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `EMAIL_HOST_USER` (opcional)
- `EMAIL_HOST_PASSWORD` (opcional)

---

## 📤 Paso 4: Desplegar en Vercel

```bash
# Instalar Vercel CLI (si no lo tienes)
npm install -g vercel

# Iniciar sesión
vercel login

# Desplegar
vercel

# Cuando te pregunte, confirma:
# - Link to existing project? No
# - Project name: delegate-system-unefa (o el que prefieras)
# - Directory: ./ (raíz del proyecto)

# Desplegar a producción
vercel --prod
```

---

## 🗄️ Paso 5: Ejecutar Migraciones en PostgreSQL

Después del despliegue, necesitas crear las tablas en PostgreSQL.

### Método 1: Usando Vercel CLI (Recomendado)

```bash
# Conectarse a la base de datos de Vercel
vercel env pull .env.production

# Ejecutar migraciones
python sistema_delegados/manage.py migrate
```

### Método 2: Localmente con credenciales de producción

1. Copia las credenciales de PostgreSQL de Vercel
2. Crea un archivo `.env.production`:

```bash
SECRET_KEY=django-insecure-y4f23#=pk3!h@m9tsy3%*!41-abp_wd%+(iv(orca@tt10k+(5
DEBUG=False
DB_ENGINE=django.db.backends.postgresql
DB_NAME=verceldb
DB_USER=default
DB_PASSWORD=[password_de_vercel]
DB_HOST=[host].postgres.vercel-storage.com
DB_PORT=5432
```

3. Ejecuta las migraciones:

```bash
# Cargar variables de producción
$env:DJANGO_SETTINGS_MODULE="sistema_delegados.settings"

# Ejecutar migraciones
python sistema_delegados/manage.py migrate
```

---

## 📥 Paso 6: Importar Datos a PostgreSQL

Una vez que las migraciones estén completas:

```bash
# Importar los datos desde el backup
python importar_datos.py
```

Este comando cargará todos tus datos de SQLite a PostgreSQL.

---

## ✅ Verificación

Después de importar, verifica que todo funcione:

1. Ve a tu URL de Vercel (ej: `https://tu-proyecto.vercel.app`)
2. Intenta iniciar sesión
3. Verifica que las carreras, materias y secciones estén disponibles

---

## 🔄 Alternativa: Usar PostgreSQL Localmente También

Si quieres usar PostgreSQL tanto en local como en producción:

### 1. Instalar PostgreSQL localmente

- Windows: Descarga desde [postgresql.org](https://www.postgresql.org/download/windows/)
- Instala y configura con contraseña

### 2. Crear base de datos local

```bash
# Abrir psql
psql -U postgres

# Crear base de datos
CREATE DATABASE delegate_system_unefa;

# Salir
\q
```

### 3. Actualizar tu .env local

```bash
SECRET_KEY=django-insecure-y4f23#=pk3!h@m9tsy3%*!41-abp_wd%+(iv(orca@tt10k+(5
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=delegate_system_unefa
DB_USER=postgres
DB_PASSWORD=tu_password_local
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=rafa1234.univ@gmail.com
EMAIL_HOST_PASSWORD=xfbr cpnr ggro bxea
```

### 4. Migrar e importar datos

```bash
# Ejecutar migraciones
python sistema_delegados/manage.py migrate

# Importar datos
python importar_datos.py
```

---

## 🆘 Solución de Problemas

### Error: "relation does not exist"
- Ejecuta las migraciones primero: `python sistema_delegados/manage.py migrate`

### Error: "password authentication failed"
- Verifica las credenciales en las variables de entorno
- Asegúrate de copiar el password correcto de Vercel

### Error: "could not connect to server"
- Verifica que el HOST y PORT sean correctos
- Asegúrate de tener conexión a internet
- Verifica que Vercel Postgres esté activo

### Los datos no aparecen después de importar
- Verifica que `datos_backup.json` exista
- Ejecuta: `python importar_datos.py` nuevamente
- Revisa los logs para ver si hay errores

---

## 📋 Resumen de Archivos Creados

- ✅ `datos_backup.json` - Backup completo de tus datos SQLite
- ✅ `exportar_datos.py` - Script para exportar datos de SQLite
- ✅ `importar_datos.py` - Script para importar datos a PostgreSQL
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `build_files.sh` - Script de build para Vercel
- ✅ `.vercelignore` - Archivos a ignorar en el despliegue

---

## 🎯 Próximos Pasos

1. ✅ Datos exportados
2. ⏳ Crear base de datos PostgreSQL en Vercel
3. ⏳ Configurar variables de entorno
4. ⏳ Desplegar en Vercel
5. ⏳ Ejecutar migraciones
6. ⏳ Importar datos
7. ⏳ Verificar que todo funcione

¡Estás listo para desplegar! 🚀

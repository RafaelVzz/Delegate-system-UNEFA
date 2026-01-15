# RESUMEN: Migración de SQLite a PostgreSQL para Vercel

## ✅ LO QUE YA ESTÁ HECHO

### 1. Datos Exportados
- ✅ Archivo: `datos_backup.json` (60 KB)
- ✅ Contiene TODAS tus carreras, secciones, materias y usuarios
- ✅ Listo para importar a PostgreSQL

### 2. Archivos de Configuración Creados
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `build_files.sh` - Script de construcción
- ✅ `.vercelignore` - Archivos a ignorar
- ✅ `sistema_delegados/wsgi_vercel.py` - Punto de entrada WSGI
- ✅ `exportar_datos.py` - Script de exportación
- ✅ `importar_datos.py` - Script de importación

### 3. Dependencias Actualizadas
- ✅ `whitenoise==6.8.2` - Para archivos estáticos
- ✅ `psycopg2-binary==2.9.9` - Para PostgreSQL

### 4. Settings.py Configurado
- ✅ DEBUG dinámico (usa variable de entorno)
- ✅ ALLOWED_HOSTS configurado
- ✅ WhiteNoise middleware agregado
- ✅ STATIC_ROOT configurado
- ✅ Soporte para PostgreSQL cuando DB_ENGINE está definido

---

## 🚀 PRÓXIMOS PASOS (LO QUE DEBES HACER)

### Paso 1: Crear Base de Datos en Vercel (5 minutos)

1. Ve a [vercel.com](https://vercel.com) e inicia sesión
2. Crea un nuevo proyecto o selecciona uno existente
3. Ve a la pestaña **Storage**
4. Click en **Create Database** → **Postgres** → **Continue**
5. Selecciona el plan **Hobby (Free)**
6. Click en **Create**

Vercel creará automáticamente las variables de entorno de PostgreSQL.

### Paso 2: Configurar Variables de Entorno Adicionales (2 minutos)

En tu proyecto de Vercel → **Settings** → **Environment Variables**, agrega:

```
SECRET_KEY = django-insecure-y4f23#=pk3!h@m9tsy3%*!41-abp_wd%+(iv(orca@tt10k+(5
DEBUG = False
ALLOWED_HOSTS = .vercel.app
EMAIL_HOST_USER = rafa1234.univ@gmail.com
EMAIL_HOST_PASSWORD = xfbr cpnr ggro bxea
```

### Paso 3: Conectar tu Repositorio y Desplegar (3 minutos)

**Opción A: Desde GitHub (Recomendado)**

1. Sube tu código a GitHub:
   ```bash
   git add .
   git commit -m "Configuración para Vercel con PostgreSQL"
   git push origin main
   ```

2. En Vercel:
   - Click en **Add New** → **Project**
   - Importa tu repositorio de GitHub
   - Vercel detectará automáticamente Django
   - Click en **Deploy**

**Opción B: Desde Vercel CLI**

```bash
# Instalar Vercel CLI
npm install -g vercel

# Iniciar sesión
vercel login

# Desplegar
vercel

# Desplegar a producción
vercel --prod
```

### Paso 4: Ejecutar Migraciones en PostgreSQL (2 minutos)

Después del despliegue, necesitas crear las tablas:

```bash
# Descargar las variables de entorno de Vercel
vercel env pull .env.production

# Ejecutar migraciones (esto creará las tablas en PostgreSQL)
python sistema_delegados/manage.py migrate
```

### Paso 5: Importar tus Datos (1 minuto)

```bash
# Importar todos los datos desde SQLite a PostgreSQL
python importar_datos.py
```

¡Listo! Tu aplicación estará en línea con todos tus datos.

---

## 📝 COMANDOS RÁPIDOS

```bash
# 1. Desplegar en Vercel
vercel --prod

# 2. Descargar variables de entorno
vercel env pull .env.production

# 3. Ejecutar migraciones
python sistema_delegados/manage.py migrate

# 4. Importar datos
python importar_datos.py

# 5. Verificar
# Ve a: https://tu-proyecto.vercel.app
```

---

## ⚠️ IMPORTANTE

- **NO subas** el archivo `.env` a Git (ya está en `.gitignore`)
- **NO subas** `datos_backup.json` a Git (ya está en `.vercelignore`)
- **Guarda** el archivo `datos_backup.json` en un lugar seguro como respaldo
- **Verifica** que todas las variables de entorno estén configuradas en Vercel

---

## 🆘 ¿Problemas?

Lee la guía completa en: **`MIGRACION_A_VERCEL.md`**

---

## 📊 Estado Actual

- ✅ Datos exportados: **datos_backup.json** (60 KB)
- ✅ Configuración de Vercel: Completa
- ✅ Dependencias: Actualizadas
- ⏳ Base de datos PostgreSQL: Pendiente de crear
- ⏳ Despliegue: Pendiente
- ⏳ Migraciones: Pendiente
- ⏳ Importación de datos: Pendiente

**Tiempo estimado total: 15-20 minutos**

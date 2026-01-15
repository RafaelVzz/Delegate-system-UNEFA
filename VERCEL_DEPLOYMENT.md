# Configuración de Vercel para Sistema de Delegados UNEFA

## 📋 Variables de Entorno Requeridas en Vercel

Antes de desplegar, debes configurar las siguientes variables de entorno en el Dashboard de Vercel:

### Variables Obligatorias:

1. **SECRET_KEY**: Clave secreta de Django
   ```
   Ejemplo: django-insecure-tu-clave-secreta-aqui-123456
   ```

2. **DEBUG**: Modo debug (usar False en producción)
   ```
   False
   ```

3. **ALLOWED_HOSTS**: Dominios permitidos
   ```
   .vercel.app,tu-dominio-personalizado.com
   ```

### Variables Opcionales (Base de Datos MySQL):

Si vas a usar MySQL en producción, configura estas variables:

4. **DB_ENGINE**:
   ```
   django.db.backends.mysql
   ```

5. **DB_NAME**: Nombre de tu base de datos
6. **DB_USER**: Usuario de la base de datos
7. **DB_PASSWORD**: Contraseña de la base de datos
8. **DB_HOST**: Host de la base de datos
9. **DB_PORT**: Puerto (por defecto 3306)

### Variables de Email (Opcional):

10. **EMAIL_HOST_USER**: Tu correo de Gmail
11. **EMAIL_HOST_PASSWORD**: Contraseña de aplicación de Gmail

## 🚀 Pasos para Desplegar en Vercel

### 1. Instalar Vercel CLI (si no lo tienes)
```bash
npm install -g vercel
```

### 2. Iniciar sesión en Vercel
```bash
vercel login
```

### 3. Desplegar el proyecto
Desde la raíz del proyecto, ejecuta:
```bash
vercel
```

### 4. Configurar Variables de Entorno
En el Dashboard de Vercel:
1. Ve a tu proyecto
2. Settings → Environment Variables
3. Agrega cada variable mencionada arriba

### 5. Redesplegar con las variables
```bash
vercel --prod
```

## ⚠️ Limitaciones Importantes de Django en Vercel

1. **Base de datos SQLite no funciona** en producción en Vercel (es serverless)
   - Debes usar una base de datos externa como:
     - **PostgreSQL** (recomendado): Vercel Postgres, Supabase, Railway
     - **MySQL**: PlanetScale, Railway
     - **MongoDB**: MongoDB Atlas

2. **Archivos estáticos**: Se sirven mediante WhiteNoise

3. **Migraciones**: Debes ejecutarlas manualmente o usar un servicio externo

## 🔧 Configuración de Base de Datos PostgreSQL (Recomendado)

Si quieres usar PostgreSQL en lugar de MySQL:

1. Instala el adaptador:
```bash
pip install psycopg2-binary
```

2. Agrega a `requirements.txt`:
```
psycopg2-binary==2.9.9
```

3. Configura las variables de entorno en Vercel:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=tu_host.postgres.database.azure.com
DB_PORT=5432
```

## 📝 Notas Adicionales

- El archivo `db.sqlite3` NO se subirá a Vercel (está en `.vercelignore`)
- Los archivos estáticos se recolectan automáticamente durante el build
- Las migraciones deben ejecutarse en tu base de datos de producción antes del despliegue

## 🆘 Solución de Problemas

### Error 404
- Verifica que `vercel.json` esté en la raíz del proyecto
- Asegúrate de que todas las rutas en `vercel.json` sean correctas

### Error 500
- Revisa los logs en Vercel Dashboard
- Verifica que todas las variables de entorno estén configuradas
- Asegúrate de que DEBUG=False en producción

### Error de Base de Datos
- Verifica que la base de datos externa esté configurada
- Ejecuta las migraciones en la base de datos de producción
- Verifica las credenciales de conexión

## 📚 Recursos Útiles

- [Documentación de Vercel](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

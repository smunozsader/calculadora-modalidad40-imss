# Railway Deploy Configuration

## Configuración de Deployment

### 1. Archivos de Configuración Requeridos

**Procfile** (en la raíz del proyecto):
```
web: cd webapp && gunicorn app:app
```

**railway.json** (en la raíz del proyecto):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "cd webapp && gunicorn app:app",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**requirements.txt** (en la raíz del proyecto):
```
Flask==3.0.0
gunicorn==21.2.0
reportlab==4.0.8
```

### 2. Estructura del Proyecto
```
2025. SEMANAS COTIZADAS SERGIO/
├── Procfile
├── railway.json
├── requirements.txt
├── webapp/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
└── calculadoras-python/
    └── Calculadora_Modalidad_40_CORREGIDA.py
```

### 3. Pasos para Deploy en Railway

1. **Conectar Repositorio GitHub**
   - Ve a [railway.app](https://railway.app)
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio `calculadora-modalidad40-imss`

2. **Configuración Automática**
   - Railway detectará automáticamente el `railway.json`
   - El build se ejecutará usando los comandos configurados
   - La aplicación se iniciará desde el directorio `webapp/`

3. **Variables de Entorno** (opcional)
   ```
   FLASK_ENV=production
   PORT=8080
   PYTHONPATH=/app
   ```

4. **Dominio Personalizado** (opcional)
   - Railway proporciona un dominio automático: `https://tu-app.up.railway.app`
   - Puedes configurar un dominio personalizado en la configuración

### 4. Build y Deploy Process

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
cd webapp && gunicorn app:app
```

### 5. Monitoreo y Logs

- **Logs en tiempo real:** Disponibles en el dashboard de Railway
- **Métricas:** CPU, memoria y tráfico de red
- **Health checks:** Configurados para verificar `/` cada 100 segundos

### 6. Auto-Deploy

- **Deploy automático:** En cada push a la rama `main`
- **Preview deploys:** Para pull requests (opcional)
- **Rollback:** Disponible desde el dashboard

### 7. URL de la Aplicación

Tu calculadora estará disponible en:
`https://calculadora-modalidad40-imss.up.railway.app`

### 8. Troubleshooting

**Problemas comunes:**
- Verificar que `Procfile` esté en la raíz
- Asegurar que las rutas en `railway.json` sean correctas
- Revisar logs de build en el dashboard de Railway
- Verificar que `requirements.txt` contenga todas las dependencias

**Debug en producción:**
```bash
railway logs --tail
```
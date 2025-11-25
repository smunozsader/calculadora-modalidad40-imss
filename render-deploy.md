# Render Deploy Configuration

## Build Settings
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Environment:** Python 3
- **Python Version:** 3.12.0

## Environment Variables (opcional)
```
FLASK_ENV=production
PORT=10000
```

## Auto-Deploy
- Conecta tu repositorio GitHub
- Render detectará automáticamente la configuración
- Se desplegará automáticamente en cada push

## URL esperada
Tu app estará disponible en:
`https://tu-app-name.onrender.com`
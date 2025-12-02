# 🚀 Deployment Configuration

This directory contains all deployment-related configuration files for the Calculadora Modalidad 40 IMSS.

## 📁 Files Overview

### Railway Deployment
- `main.py` - Entry point for Railway deployment
- `railway.json` - Railway service configuration  
- `railway.toml` - Railway build configuration
- `nixpacks.toml` - Nixpacks build system config

### Docker Deployment  
- `Dockerfile` - Docker container configuration
- `Procfile` - Process definition for various platforms

## 🔧 Railway Deployment

The main production deployment runs on Railway:

**Live URL**: https://calculadora-modalidad40-imss-production.up.railway.app/

### Auto-Deploy Process
1. Push to `main` branch triggers automatic deployment
2. Railway builds using Nixpacks configuration
3. `main.py` serves as entry point
4. Flask app runs on assigned PORT

### Environment Variables
- `PORT` - Automatically set by Railway
- `PYTHON_VERSION` - Defined in `../runtime.txt`

## 🐳 Local Docker Development

```bash
# Build image
docker build -f deployment/Dockerfile -t calculadora-modalidad40 .

# Run container  
docker run -p 5000:5000 calculadora-modalidad40
```

## 📝 Deployment Notes

- All paths in `main.py` are relative to project root
- Dependencies defined in `../requirements.txt`
- Static files served from `webapp/templates/`
- Calculator engine imported from `calculadoras-python/`

## 🔄 Updates

Any changes to deployment configuration should be tested locally before pushing to production.
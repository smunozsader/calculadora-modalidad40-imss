# 🧮 Calculadora Modalidad 40 IMSS - Proyecto Completo

Calculadora web completa para estimar pensiones bajo la Modalidad 40 del IMSS según la Ley 73 del Seguro Social mexicano.

## ✨ Características Principales

- ✅ **Validación de Elegibilidad**: Verifica automáticamente acceso a Modalidad 40 (Ley 73 vs Ley 97)  
- 📊 **Cálculo Dinámico**: Múltiples escenarios y proyecciones de pensión
- 💰 **Timeline de Pagos**: Pagos mensuales detallados por año hasta retiro
- 📄 **Reportes PDF**: Generación de reportes personalizados
- 🔒 **Cumplimiento Legal**: Implementa restricciones y requisitos IMSS

## 📁 Estructura del Proyecto (Reorganizada)

```
CALCULADORA-MODALIDAD40-IMSS/
├── 📄 main.py                          # Entry point para desarrollo local
├── 📄 requirements.txt                 # Dependencias Python
├── 📄 runtime.txt                      # Versión Python
├── 📄 .gitignore                       # Exclusiones Git
├── 📄 README.md                        # Este archivo
│
├── 📱 webapp/                          # Aplicación Web Flask  
│   ├── app.py                         # Backend Flask principal
│   ├── templates/                     # Templates HTML
│   │   └── index.html                 # Calculadora principal + validación Ley 97
│   └── README.md                      # Documentación webapp
│
├── 🐍 calculadoras-python/            # Motor de Cálculo
│   └── Calculadora_Modalidad_40_CORREGIDA.py    # ✅ Lógica principal pensiones
│
├── 📚 documentos/                     # Documentación Técnica y Legal
│   ├── ley_77.md                     # 🚨 Requisitos legales Ley 97 (crítico)
│   ├── Requisitos Modalidad 40.md    # Requisitos completos IMSS
│   └── Analisis *.md                 # Análisis técnicos diversos
│
├── 📊 calculadoras excel/             # Referencias Excel
│   └── *.csv, *.xlsm                 # Hojas cálculo referencia
│
├── 🔧 tests/                          # Tests y Utilidades 
│   ├── test_*.py                     # Tests funcionalidad
│   └── fix_js_scope.py               # Utilidades desarrollo
│
├── 🚀 deployment/                      # Configuración Despliegue
│   ├── main.py                       # Entry point Railway
│   ├── railway.json                  # Config Railway
│   ├── Dockerfile                    # Config Docker  
│   └── *.toml, Procfile             # Configs deployment
│
├── 📁 logs/                           # Logs deployment
├── 📁 normativa/                      # Normativa IMSS
│   └── tablas_referencia_UMA_CORREGIDAS.csv
│
├── 📄 latex/                          # Documentos LaTeX y PDFs
│   ├── *.tex                         # Códigos fuente LaTeX
│   ├── *.pdf                         # Documentos generados
│   └── *.aux, *.log, etc.            # Archivos auxiliares LaTeX
│
├── ⚖️ normativa/                      # Base Legal y Normativa
│   └── [Documentos legales IMSS]
│
└── 🔧 Archivos de Configuración       # Configuración del Proyecto
    ├── Procfile                      # Configuración Railway/Heroku
    ├── requirements.txt              # Dependencias Python
    ├── railway.json                  # Configuración Railway
    ├── .gitignore                    # Archivos excluidos de Git
    └── 2025. SEMANAS COTIZADAS SERGIO.code-workspace
```

## 🚀 Despliegue

### Aplicación Web (Railway)
```bash
# La aplicación web está configurada para desplegarse desde la carpeta webapp/
# Railway ejecuta: cd webapp && gunicorn app:app
```

**URL de Producción:** [Tu URL de Railway aquí]

## 🎯 Características Principales

### ✅ **Calculadora Web Completa**
- Captura de datos personales completos (Nombre, RFC, CURP, NSS)
- Cálculos Modalidad 40 con tablas variables Ley 73
- Generación de reportes PDF profesionales
- Interfaz responsive y moderna

### ✅ **Motores de Cálculo Validados**
- Fórmulas Ley 73 con tablas variables (80% - 13%)
- Validación matemática exhaustiva
- ROI y análisis actuarial completo

### ✅ **Documentación Completa**
- Análisis actuariales profesionales
- Base normativa legal completa
- Comparativas de estrategias de pago

## 🔧 Tecnologías

- **Backend:** Python Flask
- **Frontend:** Bootstrap 5, JavaScript
- **PDF:** ReportLab
- **Deploy:** Railway
- **Cálculos:** NumPy, tablas IMSS oficiales

## 📞 Contacto

Proyecto desarrollado para análisis personal de Modalidad 40 IMSS.
**Disclaimer:** No constituye asesoría oficial. Consulte directamente con IMSS.
# 🧮 Calculadora Modalidad 40 IMSS - Proyecto Completo

## 📁 Estructura del Proyecto

```
2025. SEMANAS COTIZADAS SERGIO/
├── 📱 webapp/                          # Aplicación Web Flask
│   ├── app.py                         # Aplicación principal
│   ├── templates/                     # Templates HTML
│   │   ├── index.html                 # Calculadora principal
│   │   └── info.html                  # Información educativa
│   ├── README.md                      # Documentación del webapp
│   └── render-deploy.md               # Guías de despliegue
│
├── 🐍 calculadoras-python/            # Motores de Cálculo
│   ├── Calculadora_Modalidad_40_CORREGIDA.py    # ✅ Motor principal (tablas variables)
│   ├── Calculadora_Modalidad_40_Universal.py    # Versión universal
│   ├── Calculo_Pension_Ley73_COMPLETO.py       # Cálculos Ley 73 completos
│   ├── Interfaz_Calculadora_Modalidad40.py     # Interfaz standalone
│   └── Verificacion_Calculos_REALES.py         # Validaciones matemáticas
│
├── 📚 documentos/                     # Análisis y Documentación
│   ├── Analisis*.md                  # Análisis actuariales y matemáticos
│   ├── Comparativa*.md               # Comparativas de estrategias
│   ├── Requisitos*.md                # Requisitos legales y normativos
│   └── RESUMEN*.md                   # Resúmenes ejecutivos
│
├── 📊 calculadoras excel/             # Hojas de Cálculo Excel
│   ├── 2025. saldo afore al mes de oct.csv
│   ├── Calculador de Pensiones ley 73 (2018) Sergio de Alba(1).xlsm
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
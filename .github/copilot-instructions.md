# Copilot Instructions - IMSS Semanas Cotizadas Project

## Project Overview

This is a personal documentation and tracking project for IMSS (Instituto Mexicano del Seguro Social) Modalidad 40 requirements and contribution weeks analysis. The project includes:
- Documentation of eligibility requirements and contribution history
- Python calculators for pension projections under Ley 73
- Flask web application for interactive Modalidad 40 calculations
- **Live deployment**: https://web-production-9372ec.up.railway.app/

## Deployment Configuration

### Railway Platform
- **Production URL**: https://web-production-9372ec.up.railway.app/
- **Platform**: Railway.app
- **Deployment method**: Dockerfile-based build
- **Repository**: smunozsader/calculadora-modalidad40-imss
- **Branch**: main (auto-deploys on push)

### File Structure for Deployment
```
/deployment/
  ├── Dockerfile          # Build configuration
  ├── main.py            # Railway entry point (imports webapp.app)
  ├── Procfile           # Process definition: gunicorn main:app
  └── railway.json       # Railway-specific config
  
/webapp/
  ├── app.py            # Main Flask application
  ├── templates/        # HTML templates
  └── static/           # CSS, JS, images
  
/calculadoras-python/   # Core calculation logic
  └── Calculadora_Modalidad_40_CORREGIDA.py
```

### Key Technical Details
- **Web framework**: Flask 3.1.2
- **WSGI server**: Gunicorn 21.2.0
- **PDF generation**: ReportLab 4.0.7
- **Entry point**: `deployment/main.py` exposes Flask app for gunicorn
- **Health check**: Configured on `/` with 120s timeout
- **Restart policy**: ON_FAILURE with max 10 retries

## Key Context & Domain Knowledge

### IMSS Terminology
- **Modalidad 40**: Voluntary Continuation in the Mandatory Regime - allows inactive workers to continue contributing
- **Semanas Cotizadas**: Contribution weeks - the fundamental unit for pension calculations
- **Ley 73**: 1973 Social Security Law - determines pension calculation method
- **CURP**: Unique Population Registry Code (Mexican national ID)
- **NSS**: Social Security Number (IMSS-specific identifier)
- **UMA**: Unit of Measure and Update (used for salary caps and calculations)

### Critical Requirements Pattern
When documenting IMSS requirements, always structure as:
1. **Eligibility criteria** (with specific time limits and thresholds)
2. **Required documentation** (originals vs copies, validity periods)
3. **Additional considerations** (payment options, consequences of interruption)

## File Patterns & Conventions

### Documentation Structure
- Use `.md` files for requirements and procedures
- Include both Spanish terms and English explanations in parentheses
- Bold key requirements and thresholds (e.g., **52 semanas cotizadas**, **5 años**)
- Use bullet points for requirement lists, numbered lists for procedures

### PDF Handling
- Contribution reports are typically named: `[CURP] reporteSemanasCotizadas.pdf`
- These contain official IMSS contribution history data
- Always preserve original filenames for traceability

## Project-Specific Patterns

### Time Sensitivity
- All IMSS procedures have strict time limits (typically 5 years from last employment)
- When documenting timelines, always specify the reference date clearly
- Current context: Analysis performed in 2025 for historical contribution periods

### Bilingual Documentation
- Primary language: Spanish (official IMSS language)
- Include English clarifications for technical terms
- Maintain official IMSS terminology even when translating

## Common Tasks

### Web Application Development
When working on the Flask app (`webapp/app.py`):
- Test locally before deploying: `cd webapp && python app.py`
- Changes to `main` branch auto-deploy to Railway
- Check deployment logs for debugging
- Ensure imports work from both local and deployment contexts

### Deployment Tasks
When updating deployment configuration:
- **Dockerfile changes**: Edit `deployment/Dockerfile`
  - Include locale installation for Spanish support (es_ES.UTF-8, es_MX.UTF-8)
  - Required for proper month names in PDFs
- **Dependencies**: Update root `requirements.txt` (not `deployment/requirements.txt`)
- **Entry point**: Root `main.py` imports and exposes `webapp.app`
- **Environment variables**: Configure in Railway dashboard, not in code

**CRITICAL - Module Import Structure:**
- **Root cause of ModuleNotFoundError**: `webapp/app.py` MUST configure sys.path BEFORE importing calculadora
- Each module must handle its own imports - don't rely on parent to configure paths
- Pattern to follow in `webapp/app.py`:
  ```python
  # ✅ CORRECT - Configure path BEFORE import:
  calculator_path = os.path.join(os.path.dirname(__file__), '..', 'calculadoras-python')
  calculator_path_abs = os.path.abspath(calculator_path)
  sys.path.insert(0, calculator_path_abs)  # CRITICAL: Do this BEFORE importing
  
  from Calculadora_Modalidad_40_CORREGIDA import CalculadoraModalidad40Corregida
  
  # ❌ WRONG - Path added too late or not at all:
  from Calculadora_Modalidad_40_CORREGIDA import ...  # FAILS - path not configured
  sys.path.append(calculator_path)  # Too late!
  ```

**Deployment Entry Point Structure:**
- `main.py` (root level) imports webapp.app and exposes `app` variable for gunicorn
- `deployment/Dockerfile` runs: `gunicorn main:app`
- When gunicorn imports `main`, it executes `from webapp.app import app`
- At that moment, `webapp/app.py` executes and MUST have paths configured internally

When updating requirements documentation:
1. Verify current IMSS regulations (they change frequently)
2. Include specific threshold numbers (weeks, years, salary multiples)
3. Cross-reference with actual contribution reports when available
4. Maintain clear distinction between requirements vs. recommendations

When working with contribution data:
- Preserve exact dates and periods from official reports
- Calculate gaps in coverage periods
- Track eligibility windows for different modalities

## Key Files

### Deployment & Application
- `main.py`: Railway entry point that imports Flask app
- `deployment/Dockerfile`: Container build configuration (includes Spanish locale installation)
- `deployment/Procfile`: Process definition for gunicorn
- `deployment/railway.json`: Railway platform configuration
- `webapp/app.py`: Main Flask application (configures sys.path internally for calculator imports)
- `calculadoras-python/Calculadora_Modalidad_40_CORREGIDA.py`: Core calculation engine
- `requirements.txt`: Python dependencies (root level)

### Documentation
- `Requisitos Modalidad 40.md`: Core eligibility requirements for voluntary contributions
- `MUMS640728UQ0 reporteSemanasCotizadas.pdf`: Official contribution history report
- Directory structure follows year-based organization for pension planning periods
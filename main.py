#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CALCULADORA MODALIDAD 40 IMSS - Main Entry Point
Calculadora de pensiones Modalidad 40 del IMSS bajo Ley 73

Para desarrollo local:
    python main.py

Para producción ver: deployment/main.py (Railway entry point)
"""

import sys
import os

def main():
    """Main entry point for local development"""
    # Add paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    webapp_path = os.path.join(current_dir, 'webapp')
    calculadora_path = os.path.join(current_dir, 'calculadoras-python')
    
    sys.path.insert(0, webapp_path)
    sys.path.insert(0, calculadora_path)
    
    # Import and run Flask app
    try:
        from webapp.app import app
        print("🚀 Iniciando Calculadora Modalidad 40 IMSS...")
        print("📋 Accede en: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error importando webapp: {e}")
        return 1

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAILWAY ENTRY POINT - Simplified entry for Railway deployment
This file starts the Flask app from the root directory
"""

import sys
import os

# Add paths to ensure imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
webapp_path = os.path.join(current_dir, 'webapp')
calculadora_path = os.path.join(current_dir, 'calculadoras-python')

sys.path.insert(0, webapp_path)
sys.path.insert(0, calculadora_path)

# Import and expose the Flask app
try:
    from webapp.app import app as flask_app
    app = flask_app  # Expose for gunicorn
    
    if __name__ == "__main__":
        # Get port from environment or use default
        port = int(os.environ.get('PORT', 8080))
        host = os.environ.get('HOST', '0.0.0.0')
        
        print(f"🚀 Starting Flask app on {host}:{port}")
        print(f"📂 Current directory: {current_dir}")
        print(f"📂 Webapp path: {webapp_path}")
        print(f"📂 Calculadora path: {calculadora_path}")
        
        flask_app.run(host=host, port=port, debug=False)
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Startup Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LOCAL FLASK APP TEST - Direct test of Flask endpoints
"""

import sys
import os
import json
from datetime import datetime

# Add the webapp directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'webapp'))

try:
    from app import app
    print("✅ Flask app imported successfully")
except ImportError as e:
    print(f"❌ Error importing Flask app: {e}")
    sys.exit(1)

def test_flask_endpoints_direct():
    """Test Flask endpoints directly without running server"""
    print("\n🧪 DIRECT FLASK ENDPOINT TEST")
    print("=" * 50)
    
    # Create a test client
    with app.test_client() as client:
        
        # Test simple endpoints first
        print("\n📋 Testing simple endpoints:")
        
        simple_tests = [
            ('/', 'GET', 'Main page'),
            ('/test', 'GET', 'Test endpoint'),
            ('/test-calculator', 'GET', 'Calculator test'),
            ('/api/topes', 'GET', 'API topes')
        ]
        
        for endpoint, method, description in simple_tests:
            try:
                if method == 'GET':
                    response = client.get(endpoint)
                else:
                    response = client.post(endpoint)
                    
                print(f"  {endpoint}: Status {response.status_code}")
                
                if response.status_code == 200:
                    if 'application/json' in response.content_type:
                        data = response.get_json()
                        print(f"    ✅ JSON response with keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                    else:
                        print(f"    ✅ HTML response ({len(response.data)} bytes)")
                else:
                    print(f"    ❌ Error: {response.status_code}")
                    
            except Exception as e:
                print(f"    ❌ Exception: {e}")
        
        # Test the calculation endpoint with Sergio's data
        print("\n🧮 Testing /calcular endpoint:")
        
        sergio_data = {
            # Personal data
            "nombre": "Sergio",
            "apellido_paterno": "Muñoz",
            "apellido_materno": "Sader",
            "rfc": "MUSS640728UQ0",
            "curp": "MUSS640728HDFNDR09",
            "nss": "12345678901",
            "dia_nacimiento": "28",
            "mes_nacimiento": "7",
            "año_nacimiento": "1964",
            
            # IMSS calculation data
            "semanas_cotizadas": "758",
            "sdp_actual": "222.02",
            "sbc_modalidad40": "2828.50",
            "edad_actual": "60",
            "edad_pension": "65",
            
            # Family situation
            "tiene_esposa": False,
            "num_hijos": "0",
            "tiene_padres": False,
            "año_inicio": "2025"
        }
        
        try:
            print("  📤 Sending calculation request...")
            response = client.post('/calcular', 
                                 json=sergio_data,
                                 content_type='application/json')
            
            print(f"  Status: {response.status_code}")
            print(f"  Content-Type: {response.content_type}")
            
            if response.status_code == 200:
                try:
                    data = response.get_json()
                    print(f"  ✅ JSON Response received")
                    print(f"  Response type: {type(data)}")
                    print(f"  Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
                    
                    if isinstance(data, dict):
                        if 'error' in data:
                            print(f"  ❌ Server Error: {data['error']}")
                        elif 'success' in data:
                            print(f"  ✅ Success: {data['success']}")
                            if data.get('success') and 'sin_modalidad40' in data:
                                print(f"  🎯 Pension without Mod40: ${data['sin_modalidad40']['pension_total']:,.0f}")
                                print(f"  🎯 Pension with Mod40: ${data['con_modalidad40']['pension_total']:,.0f}")
                        elif 'sin_modalidad40' in data:
                            print(f"  ✅ Calculation data found (no success flag)")
                            print(f"  🎯 Pension without Mod40: ${data['sin_modalidad40']['pension_total']:,.0f}")
                            print(f"  🎯 Pension with Mod40: ${data['con_modalidad40']['pension_total']:,.0f}")
                        else:
                            print(f"  ⚠️ Unexpected response structure")
                            print(f"  First few keys: {list(data.keys())[:5]}")
                    
                except Exception as e:
                    print(f"  ❌ JSON parsing error: {e}")
                    print(f"  Raw response: {response.data.decode()[:300]}...")
                    
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
                print(f"  Response: {response.data.decode()[:200]}...")
                
        except Exception as e:
            print(f"  ❌ Exception in calculation test: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("🚀 DIRECT FLASK APP TEST")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_flask_endpoints_direct()
#!/usr/bin/env python3
"""
Quick test to debug the exact response format from Railway
"""

import requests
import json
from datetime import datetime

def test_sergio_scenario():
    """Test Sergio's exact scenario from the console logs"""
    
    url = "https://web-production-9372ec.up.railway.app/calcular"
    
    # Sergio's data from console logs
    data = {
        'nombre': 'Sergio',
        'apellido_paterno': 'Muñoz de Alba', 
        'apellido_materno': 'Medrano',
        'rfc': 'MUMS640728UQ0',
        'curp': 'MUMS640728HDFXDR02',
        'fecha_nacimiento': '1964-07-28',
        'edad_actual': '61',
        'edad_jubilacion': '65',
        'edad_pension': '65',
        'semanas_cotizadas': '978',
        'salario_promedio': '9779',
        'salario_deseado': '2500',  # Valid SBC under UMA limit
        'sdp_actual': '2000',
        'sbc_modalidad40': '2500',
        'incluir_alternativo': 'false',
        'tiene_esposa': 'false',
        'num_hijos': '0',
        'tiene_padres': 'false'
    }
    
    print("🧪 Testing Sergio's scenario on Railway...")
    print(f"📅 Current time: {datetime.now()}")
    print(f"🌐 URL: {url}")
    
    try:
        response = requests.post(url, json=data, timeout=30)
        
        print(f"\n📡 Response Status: {response.status_code}")
        print(f"📋 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"\n✅ JSON Response:")
                print(f"   Type: {type(result)}")
                print(f"   Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                print(f"   Full content: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
                # Check what we expect vs what we got
                expected_keys = ['success', 'sin_modalidad40', 'con_modalidad40', 'inversion', 'analisis_roi']
                missing_keys = [key for key in expected_keys if key not in result]
                unexpected_keys = [key for key in result.keys() if key not in expected_keys + ['warning', 'edad_info', 'fecha_calculo', 'tope_maximo', 'uma_2025']]
                
                if missing_keys:
                    print(f"\n❌ Missing expected keys: {missing_keys}")
                if unexpected_keys:
                    print(f"\n⚠️ Unexpected keys: {unexpected_keys}")
                    
                # Check if this is the old format
                if 'continuar' in result:
                    print(f"\n🔍 OLD FORMAT DETECTED!")
                    print(f"   This suggests Railway is running an old version of the code.")
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ JSON Decode Error: {e}")
                print(f"Raw response: {response.text[:500]}...")
                
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network Error: {e}")

if __name__ == '__main__':
    test_sergio_scenario()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FLASK WEB APP TEST SUITE - Simulating exact web requests
Testing the Flask /calcular endpoint with Sergio's data
"""

import sys
import os
import json
import requests
from datetime import datetime

# Test the Flask app directly
def test_flask_app_local():
    """Test Flask app running locally"""
    print("🧪 TESTING FLASK APP - LOCAL")
    print("=" * 50)
    
    # Sergio's exact form data as sent by JavaScript
    form_data = {
        # Personal data
        "nombre": "Sergio",
        "apellido_paterno": "Muñoz",
        "apellido_materno": "Sader",
        "rfc": "MUSS640728UQ0",  # Example RFC
        "curp": "MUSS640728HDFNDR09",  # Example CURP
        "nss": "12345678901",  # Example NSS
        "dia_nacimiento": "28",
        "mes_nacimiento": "7",
        "año_nacimiento": "1964",
        
        # IMSS calculation data
        "semanas_cotizadas": "758",
        "sdp_actual": "222.02",
        "sbc_modalidad40": "2828.50",
        "edad_actual": "60",  # Current age based on birth date
        "edad_pension": "65",
        
        # Family situation
        "tiene_esposa": False,
        "num_hijos": "0",
        "tiene_padres": False,
        "año_inicio": "2025"
    }
    
    print("📤 Form data to send:")
    print(json.dumps(form_data, indent=2))
    
    # Try local Flask app first
    local_urls = [
        "http://localhost:5000/calcular",
        "http://127.0.0.1:5000/calcular"
    ]
    
    for url in local_urls:
        try:
            print(f"\n🌐 Testing URL: {url}")
            response = requests.post(
                url, 
                json=form_data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"   ✅ JSON Response received")
                    print(f"   Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                    
                    if 'error' in result:
                        print(f"   ❌ Server Error: {result['error']}")
                    elif 'sin_modalidad40' in result:
                        print(f"   ✅ Success! Pension calculation completed")
                        print(f"   Sin Mod40: ${result['sin_modalidad40']['pension_total']:,.0f}")
                        print(f"   Con Mod40: ${result['con_modalidad40']['pension_total']:,.0f}")
                    else:
                        print(f"   ⚠️ Unexpected response structure")
                        print(f"   Full response: {json.dumps(result, indent=2)}")
                        
                except json.JSONDecodeError as e:
                    print(f"   ❌ JSON Decode Error: {e}")
                    print(f"   Raw response: {response.text[:500]}...")
                    
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection failed - Flask app not running locally")
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Request timed out")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_flask_app_railway():
    """Test Flask app on Railway deployment"""
    print("\n🧪 TESTING FLASK APP - RAILWAY DEPLOYMENT")
    print("=" * 50)
    
    # Railway URL (replace with actual URL)
    railway_url = "https://calculadora-modalidad40-imss-production.up.railway.app/calcular"
    
    # Sergio's exact form data
    form_data = {
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
        print(f"🌐 Testing Railway URL: {railway_url}")
        response = requests.post(
            railway_url, 
            json=form_data,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Python-Test-Suite/1.0'
            },
            timeout=45
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Status Text: {response.reason}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ JSON Response received")
                print(f"   Response Type: {type(result)}")
                print(f"   Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
                
                # Check for different response patterns
                if isinstance(result, dict):
                    if 'error' in result:
                        print(f"   ❌ Server Error: {result['error']}")
                    elif 'success' in result and result['success']:
                        print(f"   ✅ Success flag found!")
                        if 'sin_modalidad40' in result:
                            print(f"   Sin Mod40: ${result['sin_modalidad40']['pension_total']:,.0f}")
                            print(f"   Con Mod40: ${result['con_modalidad40']['pension_total']:,.0f}")
                    elif 'sin_modalidad40' in result:
                        print(f"   ✅ Calculation data found (no success flag)")
                        print(f"   Sin Mod40: ${result['sin_modalidad40']['pension_total']:,.0f}")
                        print(f"   Con Mod40: ${result['con_modalidad40']['pension_total']:,.0f}")
                    else:
                        print(f"   ⚠️ Unexpected response structure")
                        print(f"   Full response preview:")
                        print(json.dumps(result, indent=2)[:1000] + "..." if len(str(result)) > 1000 else json.dumps(result, indent=2))
                        
                else:
                    print(f"   ❌ Response is not a dictionary: {type(result)}")
                    print(f"   Content: {str(result)[:500]}...")
                    
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON Decode Error: {e}")
                print(f"   Raw response preview: {response.text[:500]}...")
                
        else:
            print(f"   ❌ HTTP Error: {response.status_code} {response.reason}")
            print(f"   Response preview: {response.text[:300]}...")
            
    except requests.exceptions.ConnectionError as e:
        print(f"   🔌 Connection Error: {e}")
    except requests.exceptions.Timeout:
        print(f"   ⏱️ Request timed out after 45 seconds")
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")

def test_simple_endpoints():
    """Test simple endpoints first"""
    print("\n🧪 TESTING SIMPLE ENDPOINTS")
    print("=" * 50)
    
    # Test Railway endpoints
    base_url = "https://calculadora-modalidad40-imss-production.up.railway.app"
    
    endpoints_to_test = [
        ("/", "GET", "Main page"),
        ("/test", "GET", "Test endpoint"),
        ("/test-calculator", "GET", "Calculator test endpoint"),
        ("/api/topes", "GET", "API topes endpoint")
    ]
    
    for endpoint, method, description in endpoints_to_test:
        try:
            url = f"{base_url}{endpoint}"
            print(f"\n🔗 Testing {description}: {method} {url}")
            
            if method == "GET":
                response = requests.get(url, timeout=30)
            else:
                response = requests.post(url, timeout=30)
                
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                if 'application/json' in response.headers.get('content-type', ''):
                    try:
                        result = response.json()
                        print(f"   ✅ JSON Response: {list(result.keys()) if isinstance(result, dict) else type(result)}")
                    except:
                        print(f"   ⚠️ Non-JSON response")
                else:
                    print(f"   ✅ HTML/Text response ({len(response.text)} chars)")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def run_web_tests():
    """Run all web-specific tests"""
    print("🚀 FLASK WEB APPLICATION TEST SUITE")
    print("=" * 60)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test simple endpoints first
    test_simple_endpoints()
    
    # Test calculation endpoint on Railway
    test_flask_app_railway()
    
    # Test local if available
    test_flask_app_local()
    
    print("\n" + "=" * 60)
    print("🎯 WEB TEST SUMMARY")
    print("=" * 60)
    print("✅ If Railway /test-calculator works, the core calculator is fine")
    print("❌ If /calcular fails, the issue is in the web endpoint handling")
    print("🔍 Check server logs for detailed error information")

if __name__ == "__main__":
    run_web_tests()
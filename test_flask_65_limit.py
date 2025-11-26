#!/usr/bin/env python3
"""
Test Flask endpoint with 65-year legal limit enforcement
"""

import requests
import json

def test_flask_65_limit():
    """Test Flask app with 65-year legal limit scenarios"""
    
    base_url = "https://calculadora-modalidad40-imss-production.up.railway.app"
    
    test_cases = [
        {
            "name": "Age 64 → 65 (Legal, 1 year)",
            "data": {
                "nombre": "Test",
                "apellido_paterno": "User", 
                "fecha_nacimiento": "1960-12-01",  # Age 64
                "edad_jubilacion": "65",
                "semanas_cotizadas": "990",
                "salario_promedio": "15000",
                "salario_deseado": "75000",
                "incluir_alternativo": "false"
            },
            "should_work": True
        },
        {
            "name": "Age 64 → 66 (ILLEGAL, over 65)",
            "data": {
                "nombre": "Test",
                "apellido_paterno": "User",
                "fecha_nacimiento": "1960-12-01",  # Age 64
                "edad_jubilacion": "66",  # ILLEGAL - over 65
                "semanas_cotizadas": "990", 
                "salario_promedio": "15000",
                "salario_deseado": "75000",
                "incluir_alternativo": "false"
            },
            "should_work": False
        }
    ]
    
    print("🌐 Testing Flask App with 65-Year Legal Limit")
    
    results = []
    
    for case in test_cases:
        print(f"\n📋 Testing: {case['name']}")
        
        try:
            response = requests.post(
                f"{base_url}/calcular",
                data=case['data'],
                timeout=30
            )
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    
                    if case['should_work']:
                        if 'error' in result:
                            print(f"❌ FAIL: Legal scenario blocked - {result['error']}")
                            results.append(False)
                        else:
                            print("✅ PASS: Legal scenario worked")
                            if 'con_modalidad40' in result:
                                pension = result['con_modalidad40'].get('pension_total', 'N/A')
                                print(f"   Pension: ${pension:,.0f}/month" if isinstance(pension, (int, float)) else f"   Pension: {pension}")
                            results.append(True)
                    else:
                        if 'error' in result and '65 años' in result['error']:
                            print(f"✅ PASS: Illegal scenario blocked - {result['error']}")
                            results.append(True)
                        else:
                            print("❌ FAIL: Illegal scenario should have been blocked")
                            results.append(False)
                            
                except json.JSONDecodeError:
                    print(f"❌ FAIL: Invalid JSON response")
                    results.append(False)
            else:
                print(f"❌ FAIL: HTTP {response.status_code}")
                results.append(False)
                
        except requests.RequestException as e:
            print(f"❌ FAIL: Network error - {e}")
            results.append(False)
    
    return all(results)

if __name__ == '__main__':
    success = test_flask_65_limit()
    
    print(f"\n📋 Flask 65-Year Limit Test: {'✅ PASS' if success else '❌ FAIL'}")
    
    if success:
        print("\n🎉 All Flask tests passed! The 65-year legal limit is properly enforced in production.")
    else:
        print("\n💥 Some Flask tests failed. Check the deployment.")
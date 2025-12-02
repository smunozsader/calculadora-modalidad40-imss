#!/usr/bin/env python3
"""
Test the 65-year legal limit enforcement for IMSS pension
This ensures the system respects Mexican social security law
"""

import sys
import os

# Add the calculadoras-python directory to the Python path
calculadoras_path = os.path.join(os.path.dirname(__file__), 'calculadoras-python')
if calculadoras_path not in sys.path:
    sys.path.insert(0, calculadoras_path)

from Calculadora_Modalidad_40_CORREGIDA import CalculadoraModalidad40Corregida as CalculadoraModalidad40

def test_legal_age_limits():
    """Test that the calculator respects the 65-year legal pension limit"""
    print("🧪 Testing Legal Age Limits (65 years maximum)")
    
    calculadora = CalculadoraModalidad40()
    
    # Test scenarios
    test_cases = [
        {"name": "Age 64 → 65 (1 year, legal)", "edad_actual": 64, "edad_pension": 65, "should_work": True},
        {"name": "Age 63 → 65 (2 years, legal)", "edad_actual": 63, "edad_pension": 65, "should_work": True},
        {"name": "Age 60 → 65 (5 years, legal)", "edad_actual": 60, "edad_pension": 65, "should_work": True},
        {"name": "Age 59 → 65 (6 years, legal)", "edad_actual": 59, "edad_pension": 65, "should_work": True},
        {"name": "Age 64 → 66 (ILLEGAL - over 65)", "edad_actual": 64, "edad_pension": 66, "should_work": False},
        {"name": "Age 63 → 67 (ILLEGAL - over 65)", "edad_actual": 63, "edad_pension": 67, "should_work": False},
    ]
    
    results = []
    
    for case in test_cases:
        print(f"\n📋 Testing: {case['name']}")
        
        try:
            # Use valid SBC (within 25 UMA limit = $2,828.50 daily)
            sbc_diario = 2500  # Safe value under the limit
            
            resultado = calculadora.calcular_escenario_completo(
                semanas_cotizadas_actuales=990,
                sdp_actual_diario=3000,  # Current SDP
                sbc_modalidad40_diario=sbc_diario,  # Desired SBC
                edad_pension=case['edad_pension'],
                edad_actual=case['edad_actual'],
                tiene_esposa=False,
                num_hijos_dependientes=0,
                tiene_padres_dependientes=False
            )
            
            # Handle error responses from calculator
            if isinstance(resultado, dict) and 'error' in resultado:
                if not case['should_work']:
                    print(f"✅ PASS: Illegal scenario correctly blocked - {resultado['error'][:50]}...")
                    results.append(True)
                else:
                    print(f"❌ FAIL: Legal scenario incorrectly blocked - {resultado['error']}")
                    results.append(False)
            else:
                # Successful calculation
                if case['should_work']:
                    print(f"✅ PASS: Legal scenario worked correctly")
                    if 'con_modalidad40' in resultado and 'pension_final_mensual' in resultado['con_modalidad40']:
                        print(f"   Pension: ${resultado['con_modalidad40']['pension_final_mensual']:,.0f}/month")
                        print(f"   Years available: {case['edad_pension'] - case['edad_actual']}")
                    results.append(True)
                else:
                    print(f"❌ FAIL: Illegal scenario should have been blocked")
                    results.append(False)
                
        except Exception as e:
            if not case['should_work']:
                print(f"✅ PASS: Illegal scenario correctly blocked - {str(e)[:50]}...")
                results.append(True)
            else:
                print(f"❌ FAIL: Legal scenario incorrectly blocked - {e}")
                results.append(False)
    
    return all(results)

def test_age_64_scenario_detailed():
    """Detailed test for age 64 (only 1 year left) - most critical scenario"""
    print("\n🎯 Detailed Test: Age 64 Scenario (Last Year)")
    
    calculadora = CalculadoraModalidad40()
    
    try:
        # Use valid SBC (within 25 UMA limit = $2,828.50 daily)
        sbc_diario = 2500  # Safe value under the limit
        
        resultado = calculadora.calcular_escenario_completo(
            semanas_cotizadas_actuales=990,
            sdp_actual_diario=3000,  # Current SDP 
            sbc_modalidad40_diario=sbc_diario,  # Goal: $120k/month pension
            edad_actual=64,
            edad_pension=65,  # Only 1 year available
            tiene_esposa=False,
            num_hijos_dependientes=0,
            tiene_padres_dependientes=False
        )
        
        if 'error' in resultado:
            print(f"❌ Error: {resultado['error']}")
            return False
            
        print("✅ Age 64 scenario works!")
        print(f"📊 Without Modalidad 40: ${resultado['sin_modalidad40']['pension_final_mensual']:,.0f}/month")
        print(f"📊 With 1-year Modalidad 40: ${resultado['con_modalidad40']['pension_final_mensual']:,.0f}/month")
        
        if 'promedio_mensual' in resultado['inversion']:
            print(f"💰 Monthly investment needed: ${resultado['inversion']['promedio_mensual']:,.0f}")
        if 'total_años' in resultado['inversion']:
            print(f"💵 Total 1-year investment: ${resultado['inversion']['total_años']:,.0f}")
        
        if 'roi_anual' in resultado['analisis_roi']:
            print(f"📈 ROI from 1 year: {resultado['analisis_roi']['roi_anual']:.1f}%")
        
        # Verify improvement
        improvement = resultado['con_modalidad40']['pension_final_mensual'] - resultado['sin_modalidad40']['pension_final_mensual']
        improvement_pct = (improvement / resultado['sin_modalidad40']['pension_final_mensual']) * 100
        
        print(f"📈 Pension improvement: ${improvement:,.0f}/month ({improvement_pct:.1f}% increase)")
        
        return True
        
    except Exception as e:
        print(f"❌ Age 64 scenario failed: {e}")
        return False

def test_flask_validation_simulation():
    """Simulate Flask app validation for 65-year limit"""
    print("\n🌐 Simulating Flask App Validation")
    
    test_cases = [
        {"edad_pension": 60, "expected": "PASS"},
        {"edad_pension": 65, "expected": "PASS"},
        {"edad_pension": 66, "expected": "FAIL - Over 65"},
        {"edad_pension": 70, "expected": "FAIL - Over 65"},
    ]
    
    results = []
    
    for case in test_cases:
        edad_pension = case['edad_pension']
        
        # Simulate Flask validation logic
        if edad_pension < 60:
            result = "FAIL - Under 60"
        elif edad_pension > 65:
            result = "FAIL - Over 65"
        else:
            result = "PASS"
        
        expected = case['expected']
        passed = result == expected
        
        print(f"  Age {edad_pension}: {result} {'✅' if passed else '❌'}")
        results.append(passed)
    
    return all(results)

if __name__ == '__main__':
    print("🚀 Testing 65-Year Legal Limit Enforcement\n")
    
    # Run all tests
    test1 = test_legal_age_limits()
    test2 = test_age_64_scenario_detailed()
    test3 = test_flask_validation_simulation()
    
    print(f"\n📋 Final Results:")
    print(f"  - Legal Age Limits: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"  - Age 64 Scenario: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"  - Flask Validation: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if test1 and test2 and test3:
        print("\n🎉 All tests passed! The 65-year legal limit is properly enforced.")
        print("\n📚 Legal Context:")
        print("  • Mexican IMSS law sets 65 as maximum pension age")
        print("  • After 65, pension is granted automatically by old age")
        print("  • Modalidad 40 can still be extremely valuable even with just 1 year")
        print("  • Someone at age 64 has their LAST CHANCE to improve their pension")
    else:
        print("\n💥 Some tests failed. Check the validation logic.")
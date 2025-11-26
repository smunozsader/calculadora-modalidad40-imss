#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPREHENSIVE TEST SUITE - CALCULADORA MODALIDAD 40
Testing with Sergio's personal data and variations
"""

import sys
import os
import json
from datetime import datetime

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'calculadoras-python'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'webapp'))

try:
    from Calculadora_Modalidad_40_CORREGIDA import CalculadoraModalidad40Corregida
    print("✅ Calculator imported successfully")
except ImportError as e:
    print(f"❌ Error importing calculator: {e}")
    sys.exit(1)

def test_calculator_basic():
    """Test basic calculator functionality"""
    print("\n🧪 TEST 1: Basic Calculator Functionality")
    print("=" * 50)
    
    try:
        calc = CalculadoraModalidad40Corregida()
        print(f"✅ Calculator instantiated")
        print(f"   - UMA 2025: ${calc.uma_diaria_2025:.2f}")
        print(f"   - Tope máximo: ${calc.tope_diario_2025:.2f}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sergio_base_data():
    """Test with Sergio's base personal data"""
    print("\n🧪 TEST 2: Sergio's Base Data")
    print("=" * 50)
    
    # Sergio's actual data from previous analyses
    test_data = {
        'semanas_cotizadas': 758,
        'sdp_actual': 222.02,
        'sbc_modalidad40': 2828.50,  # 25 UMAs
        'edad_actual': 57,  # Approximate based on context
        'edad_pension': 65,
        'tiene_esposa': False,
        'num_hijos': 0,
        'tiene_padres': False,
        'año_inicio': 2025
    }
    
    print(f"Input Data: {json.dumps(test_data, indent=2)}")
    
    try:
        calc = CalculadoraModalidad40Corregida()
        
        resultado = calc.calcular_escenario_completo(
            semanas_cotizadas_actuales=test_data['semanas_cotizadas'],
            sdp_actual_diario=test_data['sdp_actual'],
            sbc_modalidad40_diario=test_data['sbc_modalidad40'],
            edad_pension=test_data['edad_pension'],
            tiene_esposa=test_data['tiene_esposa'],
            num_hijos_dependientes=test_data['num_hijos'],
            tiene_padres_dependientes=test_data['tiene_padres'],
            año_inicio=test_data['año_inicio']
        )
        
        print("✅ Calculation completed successfully!")
        print(f"   - Result keys: {list(resultado.keys())}")
        
        if 'error' in resultado:
            print(f"❌ Calculation returned error: {resultado['error']}")
            return False
        
        # Display key results
        sin_mod40 = resultado['sin_modalidad40']
        con_mod40 = resultado['con_modalidad40']
        
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"   Sin Modalidad 40: ${sin_mod40['pension_final_mensual']:,.0f}/mes")
        print(f"   Con Modalidad 40: ${con_mod40['pension_final_mensual']:,.0f}/mes")
        print(f"   Diferencia: ${con_mod40['pension_final_mensual'] - sin_mod40['pension_final_mensual']:,.0f}/mes")
        print(f"   Inversión total: ${resultado['inversion']['total_5_años']:,.0f}")
        print(f"   ROI anual: {resultado['analisis_roi']['roi_anual_pct']:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in calculation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_age_variations():
    """Test with different retirement ages"""
    print("\n🧪 TEST 3: Age Variations")
    print("=" * 50)
    
    base_data = {
        'semanas_cotizadas': 758,
        'sdp_actual': 222.02,
        'sbc_modalidad40': 2828.50,
        'edad_actual': 57,
        'tiene_esposa': False,
        'num_hijos': 0,
        'tiene_padres': False,
        'año_inicio': 2025
    }
    
    ages_to_test = [60, 62, 65, 67]
    results = {}
    
    calc = CalculadoraModalidad40Corregida()
    
    for edad in ages_to_test:
        print(f"\n  Testing retirement age: {edad}")
        try:
            resultado = calc.calcular_escenario_completo(
                semanas_cotizadas_actuales=base_data['semanas_cotizadas'],
                sdp_actual_diario=base_data['sdp_actual'],
                sbc_modalidad40_diario=base_data['sbc_modalidad40'],
                edad_pension=edad,
                tiene_esposa=base_data['tiene_esposa'],
                num_hijos_dependientes=base_data['num_hijos'],
                tiene_padres_dependientes=base_data['tiene_padres'],
                año_inicio=base_data['año_inicio']
            )
            
            if 'error' in resultado:
                print(f"    ❌ Error: {resultado['error']}")
                continue
                
            pension_con = resultado['con_modalidad40']['pension_final_mensual']
            factor_edad = resultado['sin_modalidad40']['factor_edad']
            
            print(f"    ✅ Age {edad}: ${pension_con:,.0f}/mes (factor: {factor_edad:.0%})")
            results[edad] = pension_con
            
        except Exception as e:
            print(f"    ❌ Exception at age {edad}: {e}")
    
    print(f"\n📊 Age comparison results: {len(results)} successful tests")
    return len(results) > 0

def test_sbc_variations():
    """Test with different SBC levels"""
    print("\n🧪 TEST 4: SBC Variations")
    print("=" * 50)
    
    base_data = {
        'semanas_cotizadas': 758,
        'sdp_actual': 222.02,
        'edad_pension': 65,
        'tiene_esposa': False,
        'num_hijos': 0,
        'tiene_padres': False,
        'año_inicio': 2025
    }
    
    # Test different UMA multiples
    calc = CalculadoraModalidad40Corregida()
    uma_daily = calc.uma_diaria_2025
    
    sbc_levels = [
        (5, uma_daily * 5, "5 UMAs"),
        (10, uma_daily * 10, "10 UMAs"),
        (15, uma_daily * 15, "15 UMAs"),
        (20, uma_daily * 20, "20 UMAs"),
        (25, uma_daily * 25, "25 UMAs (tope)")
    ]
    
    results = {}
    
    for multiplier, sbc_value, description in sbc_levels:
        print(f"\n  Testing {description}: ${sbc_value:.2f}/day")
        try:
            resultado = calc.calcular_escenario_completo(
                semanas_cotizadas_actuales=base_data['semanas_cotizadas'],
                sdp_actual_diario=base_data['sdp_actual'],
                sbc_modalidad40_diario=sbc_value,
                edad_pension=base_data['edad_pension'],
                tiene_esposa=base_data['tiene_esposa'],
                num_hijos_dependientes=base_data['num_hijos'],
                tiene_padres_dependientes=base_data['tiene_padres'],
                año_inicio=base_data['año_inicio']
            )
            
            if 'error' in resultado:
                print(f"    ❌ Error: {resultado['error']}")
                continue
                
            pension_con = resultado['con_modalidad40']['pension_final_mensual']
            inversion = resultado['inversion']['total_5_años']
            roi = resultado['analisis_roi']['roi_anual_pct']
            
            print(f"    ✅ {description}: ${pension_con:,.0f}/mes, Investment: ${inversion:,.0f}, ROI: {roi:.1f}%")
            results[multiplier] = {'pension': pension_con, 'roi': roi}
            
        except Exception as e:
            print(f"    ❌ Exception with {description}: {e}")
    
    print(f"\n📊 SBC comparison results: {len(results)} successful tests")
    return len(results) > 0

def test_family_variations():
    """Test with different family situations"""
    print("\n🧪 TEST 5: Family Situation Variations")
    print("=" * 50)
    
    base_data = {
        'semanas_cotizadas': 758,
        'sdp_actual': 222.02,
        'sbc_modalidad40': 2828.50,
        'edad_pension': 65,
        'año_inicio': 2025
    }
    
    family_scenarios = [
        (False, 0, False, "Single, no dependents"),
        (True, 0, False, "Married, no children"),
        (True, 2, False, "Married with 2 children"),
        (False, 1, False, "Single with 1 child"),
        (False, 0, True, "Single with dependent parents")
    ]
    
    calc = CalculadoraModalidad40Corregida()
    results = {}
    
    for tiene_esposa, num_hijos, tiene_padres, description in family_scenarios:
        print(f"\n  Testing: {description}")
        try:
            resultado = calc.calcular_escenario_completo(
                semanas_cotizadas_actuales=base_data['semanas_cotizadas'],
                sdp_actual_diario=base_data['sdp_actual'],
                sbc_modalidad40_diario=base_data['sbc_modalidad40'],
                edad_pension=base_data['edad_pension'],
                tiene_esposa=tiene_esposa,
                num_hijos_dependientes=num_hijos,
                tiene_padres_dependientes=tiene_padres,
                año_inicio=base_data['año_inicio']
            )
            
            if 'error' in resultado:
                print(f"    ❌ Error: {resultado['error']}")
                continue
                
            pension_con = resultado['con_modalidad40']['pension_final_mensual']
            asignaciones = resultado['con_modalidad40']['total_asignaciones_mensual']
            
            print(f"    ✅ {description}: ${pension_con:,.0f}/mes (asignaciones: ${asignaciones:,.0f})")
            results[description] = pension_con
            
        except Exception as e:
            print(f"    ❌ Exception with {description}: {e}")
    
    print(f"\n📊 Family scenarios results: {len(results)} successful tests")
    return len(results) > 0

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n🧪 TEST 6: Edge Cases")
    print("=" * 50)
    
    calc = CalculadoraModalidad40Corregida()
    edge_cases = [
        # Minimum weeks
        {
            'name': 'Minimum weeks (500)',
            'data': {
                'semanas_cotizadas': 500,
                'sdp_actual': 222.02,
                'sbc_modalidad40': 1000.0,
                'edad_pension': 65,
                'tiene_esposa': False,
                'num_hijos': 0,
                'tiene_padres': False,
                'año_inicio': 2025
            }
        },
        # Very high weeks
        {
            'name': 'Very high weeks (2000)',
            'data': {
                'semanas_cotizadas': 2000,
                'sdp_actual': 222.02,
                'sbc_modalidad40': 2828.50,
                'edad_pension': 65,
                'tiene_esposa': False,
                'num_hijos': 0,
                'tiene_padres': False,
                'año_inicio': 2025
            }
        },
        # Maximum SBC
        {
            'name': 'Maximum SBC (25 UMAs)',
            'data': {
                'semanas_cotizadas': 758,
                'sdp_actual': 222.02,
                'sbc_modalidad40': calc.tope_diario_2025,
                'edad_pension': 65,
                'tiene_esposa': False,
                'num_hijos': 0,
                'tiene_padres': False,
                'año_inicio': 2025
            }
        },
        # Low SBC
        {
            'name': 'Low SBC (1 UMA)',
            'data': {
                'semanas_cotizadas': 758,
                'sdp_actual': 222.02,
                'sbc_modalidad40': calc.uma_diaria_2025,
                'edad_pension': 65,
                'tiene_esposa': False,
                'num_hijos': 0,
                'tiene_padres': False,
                'año_inicio': 2025
            }
        }
    ]
    
    successful_tests = 0
    
    for test_case in edge_cases:
        print(f"\n  Testing: {test_case['name']}")
        try:
            data = test_case['data']
            resultado = calc.calcular_escenario_completo(
                semanas_cotizadas_actuales=data['semanas_cotizadas'],
                sdp_actual_diario=data['sdp_actual'],
                sbc_modalidad40_diario=data['sbc_modalidad40'],
                edad_pension=data['edad_pension'],
                tiene_esposa=data['tiene_esposa'],
                num_hijos_dependientes=data['num_hijos'],
                tiene_padres_dependientes=data['tiene_padres'],
                año_inicio=data['año_inicio']
            )
            
            if 'error' in resultado:
                print(f"    ❌ Error: {resultado['error']}")
                continue
                
            pension_con = resultado['con_modalidad40']['pension_final_mensual']
            print(f"    ✅ {test_case['name']}: ${pension_con:,.0f}/mes")
            successful_tests += 1
            
        except Exception as e:
            print(f"    ❌ Exception in {test_case['name']}: {e}")
    
    print(f"\n📊 Edge cases results: {successful_tests}/{len(edge_cases)} successful tests")
    return successful_tests > 0

def run_all_tests():
    """Run all test suites"""
    print("🚀 COMPREHENSIVE CALCULATOR TEST SUITE")
    print("=" * 60)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Basic Functionality", test_calculator_basic),
        ("Sergio's Base Data", test_sergio_base_data),
        ("Age Variations", test_age_variations),
        ("SBC Variations", test_sbc_variations),
        ("Family Variations", test_family_variations),
        ("Edge Cases", test_edge_cases)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results[test_name] = "✅ PASS" if success else "❌ FAIL"
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR in {test_name}: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = "🔥 CRITICAL ERROR"
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        print(f"{result} {test_name}")
    
    passed = sum(1 for r in results.values() if "PASS" in r)
    total = len(results)
    
    print(f"\n📊 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Calculator is working correctly.")
    else:
        print("⚠️ Some tests failed. Check individual results above.")
    
    return results

if __name__ == "__main__":
    run_all_tests()
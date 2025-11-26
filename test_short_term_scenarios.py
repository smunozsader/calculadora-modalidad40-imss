#!/usr/bin/env python3
"""
Comprehensive test for short-term Modalidad 40 scenarios
Tests 1, 2, 3, and 4 year scenarios to ensure all work properly
"""
import sys
import os
sys.path.append('calculadoras-python')

from Calculadora_Modalidad_40_CORREGIDA import CalculadoraModalidad40Corregida

def test_short_term_scenarios():
    """Test various short-term scenarios"""
    print("🧪 TESTING SHORT-TERM MODALIDAD 40 SCENARIOS")
    print("=" * 70)
    
    calc = CalculadoraModalidad40Corregida()
    
    scenarios = [
        {"name": "1 Year (Age 64→65)", "edad_actual": 64, "edad_pension": 65},
        {"name": "2 Years (Age 63→65)", "edad_actual": 63, "edad_pension": 65}, 
        {"name": "3 Years (Age 62→65)", "edad_actual": 62, "edad_pension": 65},
        {"name": "4 Years (Age 61→65)", "edad_actual": 61, "edad_pension": 65},
        {"name": "1 Year (Age 66→67)", "edad_actual": 66, "edad_pension": 67},
    ]
    
    base_data = {
        'semanas_cotizadas_actuales': 1100,
        'sdp_actual_diario': 600,
        'sbc_modalidad40_diario': 1500,
        'tiene_esposa': True,
        'num_hijos_dependientes': 0, 
        'tiene_padres_dependientes': False,
        'año_inicio': 2025
    }
    
    results = []
    
    for scenario in scenarios:
        print(f"\n📊 TESTING: {scenario['name']}")
        print("-" * 50)
        
        test_data = {
            **base_data,
            'edad_actual': scenario['edad_actual'],
            'edad_pension': scenario['edad_pension']
        }
        
        años_disponibles = test_data['edad_pension'] - test_data['edad_actual']
        print(f"   • Years available: {años_disponibles}")
        
        try:
            resultado = calc.calcular_escenario_completo(**test_data)
            
            if 'error' in resultado:
                print(f"   ❌ ERROR: {resultado['error']}")
                results.append({'scenario': scenario['name'], 'success': False, 'error': resultado['error']})
                continue
                
            # Extract key metrics
            pension_sin = resultado['sin_modalidad40']['pension_final_mensual']
            pension_con = resultado['con_modalidad40']['pension_final_mensual']
            diferencia = resultado['analisis_roi']['diferencia_mensual']
            inversion = resultado['inversion']['total_años']
            roi = resultado['analisis_roi']['roi_anual_pct']
            recuperacion = resultado['analisis_roi']['años_recuperacion']
            
            print(f"   ✅ SUCCESS!")
            print(f"   • Without Mod40: ${pension_sin:,.0f}/month")
            print(f"   • With Mod40: ${pension_con:,.0f}/month") 
            print(f"   • Difference: ${diferencia:,.0f}/month")
            print(f"   • Investment: ${inversion:,.0f} over {años_disponibles} year(s)")
            print(f"   • Monthly cost: ${resultado['inversion']['promedio_mensual']:,.0f}")
            print(f"   • ROI: {roi:.1f}%")
            print(f"   • Recovery: {recuperacion:.1f} years")
            
            # Validate investment breakdown matches expected years
            desglose_años = len(resultado['inversion']['desglose_anual'])
            años_esperados = min(5, años_disponibles)  # Max 5 years for Modalidad 40
            if desglose_años == años_esperados:
                print(f"   ✅ Investment years correct: {desglose_años}")
            else:
                print(f"   ⚠️ Investment years mismatch: got {desglose_años}, expected {años_esperados}")
            
            results.append({
                'scenario': scenario['name'],
                'success': True,
                'años_disponibles': años_disponibles,
                'diferencia_mensual': diferencia,
                'inversion_total': inversion,
                'roi': roi,
                'recuperacion': recuperacion,
                'años_calculados': desglose_años
            })
            
        except Exception as e:
            print(f"   ❌ EXCEPTION: {str(e)}")
            results.append({'scenario': scenario['name'], 'success': False, 'error': str(e)})
    
    # Summary
    print(f"\n🎯 SUMMARY RESULTS")
    print("=" * 70)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Successful scenarios: {len(successful)}/{len(results)}")
    print(f"❌ Failed scenarios: {len(failed)}")
    
    if successful:
        print(f"\n📈 SUCCESS DETAILS:")
        for result in successful:
            print(f"   • {result['scenario']}: +${result['diferencia_mensual']:,.0f}/mo, ${result['inversion_total']:,.0f} investment, {result['roi']:.1f}% ROI")
    
    if failed:
        print(f"\n💥 FAILURES:")
        for result in failed:
            print(f"   • {result['scenario']}: {result.get('error', 'Unknown error')}")
    
    return len(failed) == 0

if __name__ == "__main__":
    success = test_short_term_scenarios()
    if success:
        print(f"\n🎉 ALL SHORT-TERM SCENARIOS WORKING!")
    else:
        print(f"\n💥 SOME SCENARIOS FAILED!")
        sys.exit(1)
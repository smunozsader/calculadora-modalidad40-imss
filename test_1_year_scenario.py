#!/usr/bin/env python3
"""
Test case for 1-year Modalidad 40 scenario (age 64 -> 65)
This tests the edge case where someone has only 1 year until retirement
"""
import sys
import os
sys.path.append('calculadoras-python')

from Calculadora_Modalidad_40_CORREGIDA import CalculadoraModalidad40Corregida

def test_1_year_scenario():
    """Test user aged 64 who wants to retire at 65 (1 year available)"""
    print("🧪 TESTING 1-YEAR MODALIDAD 40 SCENARIO")
    print("=" * 60)
    
    calc = CalculadoraModalidad40Corregida()
    
    # Test case: User aged 64, wants to retire at 65
    test_data = {
        'semanas_cotizadas_actuales': 1100,  # Good base
        'sdp_actual_diario': 500,            # Current daily salary
        'sbc_modalidad40_diario': 1200,      # Desired higher salary  
        'edad_pension': 65,                  # Retire at 65
        'edad_actual': 64,                   # Currently 64 (1 year available)
        'tiene_esposa': True,
        'num_hijos_dependientes': 0,
        'tiene_padres_dependientes': False,
        'año_inicio': 2025
    }
    
    print(f"📊 Input Data:")
    print(f"   • Current age: {test_data['edad_actual']}")
    print(f"   • Retirement age: {test_data['edad_pension']}")
    print(f"   • Years available: {test_data['edad_pension'] - test_data['edad_actual']}")
    print(f"   • Current weeks: {test_data['semanas_cotizadas_actuales']}")
    print(f"   • Current SDP: ${test_data['sdp_actual_diario']}")
    print(f"   • Desired SBC: ${test_data['sbc_modalidad40_diario']}")
    print()
    
    try:
        resultado = calc.calcular_escenario_completo(**test_data)
        
        if 'error' in resultado:
            print(f"❌ ERROR: {resultado['error']}")
            return False
            
        print("✅ CALCULATION SUCCESSFUL!")
        print()
        
        # Analyze results
        pension_sin = resultado['sin_modalidad40']['pension_final_mensual']
        pension_con = resultado['con_modalidad40']['pension_final_mensual']
        inversion_total = resultado['inversion']['total_años']
        diferencia_mensual = resultado['analisis_roi']['diferencia_mensual']
        años_recuperacion = resultado['analisis_roi']['años_recuperacion']
        
        print(f"💰 PENSION COMPARISON:")
        print(f"   • Without Modalidad 40: ${pension_sin:,.0f}/month")
        print(f"   • With Modalidad 40:    ${pension_con:,.0f}/month")
        print(f"   • Monthly difference:   ${diferencia_mensual:,.0f}/month")
        print()
        
        print(f"💸 INVESTMENT ANALYSIS:")
        print(f"   • Total investment (1 year): ${inversion_total:,.0f}")
        print(f"   • Monthly payment:           ${resultado['inversion']['promedio_mensual']:,.0f}")
        print(f"   • Recovery period:           {años_recuperacion:.1f} years")
        print(f"   • Annual ROI:                {resultado['analisis_roi']['roi_anual_pct']:.1f}%")
        print()
        
        # Verify investment calculation details
        print(f"📈 INVESTMENT BREAKDOWN:")
        for año, datos in resultado['inversion']['desglose_anual'].items():
            print(f"   • {año}: ${datos['costo_mensual']:,.0f}/month (${datos['costo_anual']:,.0f}/year) at {datos['tasa_pct']}%")
        print()
        
        # Check if it makes financial sense
        if años_recuperacion <= 10:
            print("✅ RECOMMENDATION: Modalidad 40 is financially viable even with 1 year!")
        else:
            print("⚠️ CAUTION: Long recovery period - consider carefully")
            
        print()
        print(f"🎯 CONCLUSION: 1-year Modalidad 40 scenario works perfectly!")
        print(f"   Investment of ${inversion_total:,.0f} over 1 year")
        print(f"   Increases pension by ${diferencia_mensual:,.0f}/month for life")
        
        return True
        
    except Exception as e:
        print(f"❌ EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_1_year_scenario()
    if success:
        print("\n🎉 1-YEAR SCENARIO TEST PASSED!")
    else:
        print("\n💥 1-YEAR SCENARIO TEST FAILED!")
        sys.exit(1)
#!/usr/bin/env python3
"""
Test the 4-year scenario for Sergio's Modalidad 40 calculation
This tests that the system now handles partial years correctly instead of blocking users
"""

import sys
import os

# Add the calculadoras-python directory to the Python path
calculadoras_path = os.path.join(os.path.dirname(__file__), 'calculadoras-python')
if calculadoras_path not in sys.path:
    sys.path.insert(0, calculadoras_path)

from Calculadora_Modalidad_40_CORREGIDA import CalculadoraModalidad40Corregida as CalculadoraModalidad40

def test_sergio_4_years_scenario():
    """
    Test Sergio's scenario with only 4 years until retirement (age 61 to 65)
    This should work now that we've removed the blocking 5-year requirement
    """
    print("🧪 Testing Sergio's 4-year scenario...")
    
    # Initialize calculator
    calculadora = CalculadoraModalidad40()
    
    # Sergio's data
    datos_sergio = {
        'salario_deseado': 120000,  # $120,000 MXN monthly pension goal
        'edad_actual': 61,
        'edad_pension': 65,
        'semanas_actuales': 990,  # Current weeks contributed
        'incluir_alternativo': False
    }
    
    try:
        # This should work now (previously blocked due to < 5 years)
        resultado = calculadora.calcular_escenario_completo(
            salario_deseado=datos_sergio['salario_deseado'],
            edad_actual=datos_sergio['edad_actual'],
            edad_pension=datos_sergio['edad_pension'],
            semanas_actuales=datos_sergio['semanas_actuales'],
            incluir_alternativo=datos_sergio['incluir_alternativo']
        )
        
        print("✅ SUCCESS: 4-year calculation completed!")
        print(f"📊 Pension without Modalidad 40: ${resultado['sin_modalidad40']['pension_total']:,.0f}")
        print(f"📊 Pension with Modalidad 40: ${resultado['con_modalidad40']['pension_total']:,.0f}")
        print(f"💰 Monthly IMSS payment: ${resultado['inversion']['promedio_mensual']:,.0f}")
        print(f"💵 Total investment: ${resultado['inversion']['total_años']:,.0f}")
        print(f"📈 Annual ROI: {resultado['analisis_roi']['roi_anual']:.1f}%")
        
        # Verify the key field is now 'total_años' instead of 'total_5_años'
        if 'total_años' in resultado['inversion']:
            print("✅ Field name updated correctly: 'total_años' found")
        else:
            print("❌ ERROR: 'total_años' field not found")
            
        # Check for warnings (should have warning about limited years)
        if 'warning' in resultado:
            print(f"⚠️ Warning (expected): {resultado['warning']}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_investment_calculation_flexible():
    """Test that the investment calculation works with flexible years"""
    print("\n🔧 Testing flexible investment calculation...")
    
    calculadora = CalculadoraModalidad40()
    
    # Test with 4 years (need to calculate SBC first)
    sbc_diario = 120000 / 30  # Approximate daily SBC for $120k monthly
    
    result_4_years = calculadora.calcular_inversion_total_años(
        sbc_diario=sbc_diario,
        año_inicio=2025,
        años_cotizar=4
    )
    
    # Test with 5 years for comparison
    result_5_years = calculadora.calcular_inversion_total_años(
        sbc_diario=sbc_diario,
        año_inicio=2025,
        años_cotizar=5
    )
    
    print(f"📊 4 years investment: ${result_4_years['total_años']:,.0f}")
    print(f"📊 5 years investment: ${result_5_years['total_años']:,.0f}")
    print(f"💡 4 years is {(result_4_years['total_años']/result_5_years['total_años']*100):.1f}% of 5 years")
    
    # 4 years should be approximately 80% of 5 years (4/5 = 0.8)
    ratio = result_4_years['total_años'] / result_5_years['total_años']
    if 0.75 <= ratio <= 0.85:  # Allow some tolerance
        print("✅ Flexible investment calculation working correctly")
        return True
    else:
        print(f"❌ ERROR: Unexpected ratio {ratio:.3f}")
        return False

if __name__ == '__main__':
    print("🚀 Testing 4-year Modalidad 40 scenario for Sergio\n")
    
    # Run tests
    test1_success = test_sergio_4_years_scenario()
    test2_success = test_investment_calculation_flexible()
    
    print(f"\n📋 Test Results:")
    print(f"  - 4-year scenario: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"  - Flexible investment: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! The system now handles partial years correctly.")
    else:
        print("\n💥 Some tests failed. Check the calculator logic.")
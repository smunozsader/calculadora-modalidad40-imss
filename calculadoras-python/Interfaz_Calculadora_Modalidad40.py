#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INTERFAZ INTERACTIVA - CALCULADORA MODALIDAD 40
Versión: 2.0 - Noviembre 2025

Esta es una interfaz amigable para la Calculadora Universal Modalidad 40
que permite a cualquier usuario evaluar su situación específica.
"""

import sys
import os

# Importar la calculadora principal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Calculadora_Modalidad_40_Universal import CalculadoraModalidad40

def obtener_int(prompt, minimo=0, maximo=None):
    """Obtener un entero válido del usuario"""
    while True:
        try:
            valor = int(input(prompt))
            if valor < minimo:
                print(f"❌ Valor mínimo: {minimo}")
                continue
            if maximo and valor > maximo:
                print(f"❌ Valor máximo: {maximo}")
                continue
            return valor
        except ValueError:
            print("❌ Por favor ingrese un número válido")

def obtener_float(prompt, minimo=0.0, maximo=None):
    """Obtener un float válido del usuario"""
    while True:
        try:
            valor = float(input(prompt))
            if valor < minimo:
                print(f"❌ Valor mínimo: {minimo}")
                continue
            if maximo and valor > maximo:
                print(f"❌ Valor máximo: {maximo}")
                continue
            return valor
        except ValueError:
            print("❌ Por favor ingrese un número válido")

def obtener_si_no(prompt):
    """Obtener respuesta Sí/No del usuario"""
    while True:
        respuesta = input(prompt + " (s/n): ").lower().strip()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif respuesta in ['n', 'no']:
            return False
        else:
            print("❌ Por favor responda 's' para sí o 'n' para no")

def main():
    """Interfaz principal de la calculadora"""
    print("="*80)
    print("🎯 CALCULADORA UNIVERSAL MODALIDAD 40 - IMSS LEY 73")
    print("   Versión 2.0 - Noviembre 2025")
    print("="*80)
    
    calc = CalculadoraModalidad40()
    
    print(f"\n📋 INFORMACIÓN IMPORTANTE:")
    print(f"• UMA 2025: ${calc.uma_diaria_2025:.2f} diario")
    print(f"• Tope máximo: 25 UMAs = ${calc.tope_diario_2025:.2f} diario")
    print(f"• Tasa Modalidad 40 2025: {calc.tasas_modalidad40[2025]:.3f}%")
    
    print("\n" + "="*60)
    print("📊 CAPTURA DE DATOS BÁSICOS")
    print("="*60)
    
    # 1. Semanas cotizadas
    print("\n🔸 1. SEMANAS COTIZADAS ACTUALES")
    print("   (Consulte su reporte de semanas cotizadas IMSS)")
    semanas_actuales = obtener_int("   Ingrese semanas cotizadas: ", minimo=500, maximo=3000)
    
    # 2. SDP actual
    print("\n🔸 2. SALARIO DIARIO PROMEDIO ACTUAL")
    print("   (Últimas 250 semanas según reporte IMSS)")
    sdp_actual = obtener_float("   Ingrese SDP en pesos: $", minimo=100.0, maximo=5000.0)
    
    # 3. Edad de pensión
    print("\n🔸 3. EDAD DE PENSIÓN DESEADA")
    edad_pension = obtener_int("   Ingrese edad (60-70 años): ", minimo=60, maximo=70)
    
    print("\n" + "="*60)
    print("👨‍👩‍👧‍👦 SITUACIÓN FAMILIAR (CRÍTICA PARA CÁLCULO)")
    print("="*60)
    
    # 4. Esposa/Concubina
    print("\n🔸 4. ¿TIENE ESPOSA O CONCUBINA?")
    print("   (Otorga 15% adicional sobre la pensión)")
    tiene_esposa = obtener_si_no("   ¿Tiene esposa/concubina?")
    
    # 5. Hijos dependientes
    print("\n🔸 5. HIJOS MENORES O ESTUDIANDO")
    print("   (10% adicional por cada hijo dependiente)")
    num_hijos = obtener_int("   Número de hijos menores o estudiando: ", minimo=0, maximo=10)
    
    # 6. Padres dependientes
    print("\n🔸 6. ¿TIENE PADRES DEPENDIENTES?")
    print("   (20% adicional, SOLO si no hay esposa ni hijos dependientes)")
    tiene_padres = False
    if not tiene_esposa and num_hijos == 0:
        tiene_padres = obtener_si_no("   ¿Tiene padres dependientes económicamente?")
    elif tiene_esposa or num_hijos > 0:
        print("   ❌ No aplica (tiene esposa o hijos dependientes)")
    
    print("\n" + "="*60)
    print("💰 ESCENARIOS DE MODALIDAD 40")
    print("="*60)
    
    # Calcular escenarios predefinidos
    escenarios_costo = [8000, 10000, 11000]
    
    # Agregar tope máximo si es diferente
    costo_tope = calc.calcular_costo_mensual(calc.tope_diario_2025, 2025)
    if costo_tope not in escenarios_costo:
        escenarios_costo.append(int(costo_tope))
    
    resultados = {}
    
    print(f"\n🎯 Analizando escenarios para su caso específico...")
    print(f"   Semanas: {semanas_actuales} | SDP: ${sdp_actual:.2f} | Edad: {edad_pension}")
    print(f"   Familia: {'Esposa✓' if tiene_esposa else 'Soltero'} | Hijos: {num_hijos} | Padres: {'✓' if tiene_padres else '✗'}")
    
    for costo_mensual in escenarios_costo:
        # Calcular SBC necesario para este costo
        sbc_requerido = (costo_mensual / (calc.tasas_modalidad40[2025] / 100)) / 30.4
        
        # Verificar si excede tope
        if sbc_requerido > calc.tope_diario_2025:
            sbc_real = calc.tope_diario_2025
            costo_real = calc.calcular_costo_mensual(sbc_real, 2025)
            es_tope = True
        else:
            sbc_real = sbc_requerido
            costo_real = costo_mensual
            es_tope = False
        
        # Calcular escenario completo
        resultado = calc.calcular_escenario_completo(
            semanas_cotizadas_actuales=semanas_actuales,
            sdp_actual_diario=sdp_actual,
            sbc_modalidad40_diario=sbc_real,
            edad_pension=edad_pension,
            tiene_esposa=tiene_esposa,
            num_hijos_dependientes=num_hijos,
            tiene_padres_dependientes=tiene_padres
        )
        
        if 'error' not in resultado:
            resultados[costo_real] = {
                'resultado': resultado,
                'es_tope': es_tope,
                'sbc_diario': sbc_real
            }
    
    # Mostrar resultados
    print(f"\n" + "="*80)
    print("🏆 RESULTADOS COMPARATIVOS")
    print("="*80)
    
    # Primero mostrar situación actual (sin Modalidad 40)
    if resultados:
        primer_resultado = list(resultados.values())[0]['resultado']
        sin_mod40 = primer_resultado['sin_modalidad40']
        
        print(f"\n🔻 SIN MODALIDAD 40 (situación actual):")
        print(f"   💰 Pensión mensual: ${sin_mod40['pension_final_mensual']:,.0f}")
        print(f"   📊 Desglose: ${sin_mod40['cuantia_basica_mensual']:,.0f} base + ${sin_mod40['incremento_mensual']:,.0f} incrementos + ${sin_mod40['total_asignaciones_mensual']:,.0f} asignaciones + ${sin_mod40['incremento_vejez_mensual']:,.0f} vejez")
    
    print(f"\n🔺 CON MODALIDAD 40 (escenarios de inversión):")
    
    for costo, datos in sorted(resultados.items()):
        resultado = datos['resultado']
        con_mod40 = resultado['con_modalidad40']
        roi = resultado['analisis_roi']
        inversion = resultado['inversion']
        
        print(f"\n   💵 Inversión ${costo:,.0f}/mes {'(TOPE MÁXIMO)' if datos['es_tope'] else ''}:")
        print(f"      • SBC diario: ${datos['sbc_diario']:.2f} ({datos['sbc_diario']/calc.uma_diaria_2025:.1f} UMAs)")
        print(f"      • Inversión total 5 años: ${inversion['total_5_años']:,.0f}")
        print(f"      • Pensión mensual: ${con_mod40['pension_final_mensual']:,.0f}")
        print(f"      • Ganancia vs actual: +${roi['diferencia_mensual']:,.0f}/mes")
        print(f"      • ROI anual: {roi['roi_anual_pct']:.1f}%")
        print(f"      • Recuperación: {roi['años_recuperacion']:.1f} años")
    
    # Recomendación
    print(f"\n" + "="*80)
    print("🎯 RECOMENDACIÓN PERSONALIZADA")
    print("="*80)
    
    if resultados:
        mejor_costo = max(resultados.keys())
        mejor_resultado = resultados[mejor_costo]['resultado']
        mejor_roi = mejor_resultado['analisis_roi']
        
        print(f"\n✅ RECOMENDACIÓN: Inversión de ${mejor_costo:,.0f}/mes")
        print(f"   • Es el escenario con mejor ROI: {mejor_roi['roi_anual_pct']:.1f}% anual")
        print(f"   • Incrementa su pensión en ${mejor_roi['diferencia_mensual']:,.0f}/mes")
        print(f"   • Recupera la inversión en {mejor_roi['años_recuperacion']:.1f} años")
        
        if mejor_roi['roi_anual_pct'] > 40:
            print(f"   🚀 ROI EXCEPCIONAL: Supera cualquier inversión comercial")
        elif mejor_roi['roi_anual_pct'] > 20:
            print(f"   📈 ROI EXCELENTE: Muy superior a instrumentos tradicionales")
        else:
            print(f"   ⚠️  ROI MODERADO: Evalúe otras opciones de inversión")
    
    # Mostrar detalles del mejor escenario
    if resultados:
        print(f"\n📋 DESGLOSE DETALLADO DEL ESCENARIO RECOMENDADO:")
        mejor_con_mod40 = mejor_resultado['con_modalidad40']
        
        print(f"   • Cuantía básica: ${mejor_con_mod40['cuantia_basica_mensual']:,.0f}/mes")
        print(f"   • Incrementos: ${mejor_con_mod40['incremento_mensual']:,.0f}/mes")
        
        if mejor_con_mod40['ayuda_esposa_mensual'] > 0:
            print(f"   • Ayuda esposa: ${mejor_con_mod40['ayuda_esposa_mensual']:,.0f}/mes")
        if mejor_con_mod40['ayuda_hijos_mensual'] > 0:
            print(f"   • Ayuda hijos: ${mejor_con_mod40['ayuda_hijos_mensual']:,.0f}/mes")
        if mejor_con_mod40['ayuda_padres_mensual'] > 0:
            print(f"   • Ayuda padres: ${mejor_con_mod40['ayuda_padres_mensual']:,.0f}/mes")
        if mejor_con_mod40['incremento_vejez_mensual'] > 0:
            print(f"   • Incremento vejez: ${mejor_con_mod40['incremento_vejez_mensual']:,.0f}/mes")
    
    print(f"\n" + "="*80)
    print("📝 ¿DESEA GENERAR REPORTE COMPLETO?")
    print("="*80)
    
    generar_reporte = obtener_si_no("\n¿Generar reporte detallado en archivo?")
    
    if generar_reporte and resultados:
        nombre_archivo = f"Reporte_Modalidad40_{semanas_actuales}sem_{sdp_actual:.0f}sdp.txt"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(calc.generar_reporte_completo(mejor_resultado))
        
        print(f"✅ Reporte guardado en: {nombre_archivo}")
    
    print(f"\n🎯 ¡Análisis completado!")
    print(f"Gracias por usar la Calculadora Universal Modalidad 40")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n👋 ¡Hasta pronto!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor contacte soporte técnico.")
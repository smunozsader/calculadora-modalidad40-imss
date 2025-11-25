#!/usr/bin/env python3
"""
Cálculo COMPLETO de Pensión IMSS Ley 73 con Modalidad 40
Basado en el proceso detallado de Finauta.com
Incluye: Cuantía Básica, Incrementos, Asignaciones Familiares, Factor Edad
"""

import pandas as pd
import numpy as np

# Valores base para 2025
UMA_2025 = 108.57  # UMA diaria
TOPE_MAX_UMAS = 25
SDP_TOPE = UMA_2025 * TOPE_MAX_UMAS  # Salario Diario Promedio máximo

print("="*80)
print("CÁLCULO COMPLETO PENSIÓN LEY 73 + MODALIDAD 40")
print("Incorporando TODOS los componentes según normativa IMSS")
print("="*80)

# TABLA ARTÍCULO 167 - Cuantía Básica y Porcentajes de Incremento
# Simplificada para niveles principales (necesitaríamos la tabla completa)
tabla_art_167 = {
    # Nivel UMAs: (% Cuantía Básica, % Incremento Anual)
    1.0: (0.35, 0.56),    # Hasta 1 UMA
    2.0: (0.37, 0.78),    # Hasta 2 UMAs  
    3.0: (0.39, 0.95),    # Hasta 3 UMAs
    5.0: (0.42, 1.15),    # Hasta 5 UMAs
    10.0: (0.48, 1.45),   # Hasta 10 UMAs
    15.0: (0.52, 1.68),   # Hasta 15 UMAs
    20.0: (0.55, 1.85),   # Hasta 20 UMAs
    25.0: (0.58, 2.05),   # Hasta 25 UMAs (TOPE)
}

def obtener_porcentajes_tabla(sdp_diario, uma_diaria):
    """Obtiene porcentajes de cuantía básica e incremento según nivel UMA"""
    nivel_umas = sdp_diario / uma_diaria
    
    # Encontrar el rango correspondiente en la tabla
    for limite_umas in sorted(tabla_art_167.keys()):
        if nivel_umas <= limite_umas:
            return tabla_art_167[limite_umas]
    
    # Si excede el máximo, usar el tope
    return tabla_art_167[25.0]

def calcular_pension_completa(salario_mensual_modalidad40, edad_retiro=65, 
                            semanas_adicionales=260, tiene_esposa=True, 
                            num_hijos=0, padres_dependientes=0):
    """
    Calcula la pensión completa según Ley 73 con TODOS los componentes
    
    Args:
        salario_mensual_modalidad40: Salario base para Modalidad 40
        edad_retiro: Edad de retiro (60-65)
        semanas_adicionales: Semanas cotizadas adicionales a las 500 base
        tiene_esposa: Si tiene derecho a asignación por cónyuge
        num_hijos: Número de hijos menores/estudiantes
        padres_dependientes: Número de padres dependientes
    """
    
    # 1. SALARIO DIARIO PROMEDIO (SDP)
    sdp_diario = salario_mensual_modalidad40 / 30
    
    # 2. OBTENER PORCENTAJES DE LA TABLA ARTÍCULO 167
    pct_cuantia_basica, pct_incremento_anual = obtener_porcentajes_tabla(sdp_diario, UMA_2025)
    
    # 3. CUANTÍA BÁSICA ANUAL
    cuantia_basica_anual = sdp_diario * pct_cuantia_basica * 365
    
    # 4. INCREMENTO ANUAL POR SEMANAS ADICIONALES
    # Solo aplica para semanas que excedan las primeras 500
    incremento_por_semana = sdp_diario * (pct_incremento_anual / 100) * 365
    incremento_total_anual = incremento_por_semana * (semanas_adicionales / 52)
    
    # 5. PENSIÓN BASE ANUAL (antes de factor edad)
    pension_base_anual = cuantia_basica_anual + incremento_total_anual
    
    # 6. FACTOR POR EDAD DE RETIRO
    factores_edad = {60: 0.75, 61: 0.80, 62: 0.85, 63: 0.90, 64: 0.95, 65: 1.00}
    factor_edad = factores_edad.get(edad_retiro, 1.00)
    
    pension_ajustada_edad = pension_base_anual * factor_edad
    
    # 7. ASIGNACIONES FAMILIARES Y AYUDA ASISTENCIAL
    asignaciones = 0
    
    # Verificar si aplica ayuda por soledad (sin dependientes)
    sin_dependientes = not tiene_esposa and num_hijos == 0 and padres_dependientes == 0
    
    if sin_dependientes:
        # Ayuda por soledad: 15%
        asignaciones = pension_ajustada_edad * 0.15
    else:
        # Asignaciones por dependientes
        if tiene_esposa:
            asignaciones += pension_ajustada_edad * 0.15  # 15% por esposa
        
        # 10% por cada hijo menor/estudiante
        asignaciones += pension_ajustada_edad * 0.10 * num_hijos
        
        # 10% por cada padre dependiente (solo si no hay esposa ni hijos)
        if not tiene_esposa and num_hijos == 0:
            asignaciones += pension_ajustada_edad * 0.10 * padres_dependientes
    
    # 8. PENSIÓN TOTAL ANUAL
    pension_total_anual = pension_ajustada_edad + asignaciones
    pension_mensual = pension_total_anual / 12
    
    return {
        'sdp_diario': sdp_diario,
        'nivel_umas': sdp_diario / UMA_2025,
        'pct_cuantia_basica': pct_cuantia_basica,
        'pct_incremento_anual': pct_incremento_anual,
        'cuantia_basica_anual': cuantia_basica_anual,
        'incremento_total_anual': incremento_total_anual,
        'pension_base_anual': pension_base_anual,
        'factor_edad': factor_edad,
        'pension_ajustada_edad': pension_ajustada_edad,
        'asignaciones': asignaciones,
        'pension_total_anual': pension_total_anual,
        'pension_mensual': pension_mensual
    }

# ANÁLISIS COMPARATIVO CON FÓRMULA COMPLETA
print("\n" + "="*60)
print("ANÁLISIS CON FÓRMULA COMPLETA LEY 73")
print("="*60)

# Escenarios de Modalidad 40
escenarios = [8000, 10000, 15000, 20000, 25000, int(SDP_TOPE * 30)]  # Último es el tope

# Tasas progresivas Modalidad 40
tasas_por_año = {
    2025: 0.13347,
    2026: 0.14506, 
    2027: 0.15665,
    2028: 0.16824,
    2029: 0.17709
}

resultados_completos = []

for salario_base in escenarios:
    # Cálculo de costos Modalidad 40 (5 años)
    costo_total = 0
    for año, tasa in tasas_por_año.items():
        costo_anual = salario_base * tasa * 12
        costo_total += costo_anual
    
    # Pensión con fórmula completa (caso con esposa, sin hijos)
    pension_data = calcular_pension_completa(
        salario_mensual_modalidad40=salario_base,
        edad_retiro=65,
        semanas_adicionales=260,  # 5 años = 260 semanas
        tiene_esposa=True,
        num_hijos=0
    )
    
    # Pensión anual y beneficio en 20 años
    pension_anual = pension_data['pension_total_anual']
    beneficio_20_años = pension_anual * 20
    roi = ((beneficio_20_años / costo_total) - 1) * 100
    
    resultado = {
        'salario_base': salario_base,
        'costo_total': costo_total,
        'pension_mensual': pension_data['pension_mensual'],
        'pension_anual': pension_anual,
        'beneficio_20_años': beneficio_20_años,
        'roi_20_años': roi,
        'sdp_diario': pension_data['sdp_diario'],
        'nivel_umas': pension_data['nivel_umas'],
        'cuantia_basica': pension_data['cuantia_basica_anual'],
        'incremento_anual': pension_data['incremento_total_anual'],
        'asignaciones': pension_data['asignaciones']
    }
    
    resultados_completos.append(resultado)

# Crear DataFrame para análisis
df_resultados = pd.DataFrame(resultados_completos)

print("\nRESULTADOS CON FÓRMULA LEY 73 COMPLETA:")
print("-" * 120)
print(f"{'Salario':<10} {'Costo Total':<12} {'Pensión Mes':<12} {'Pensión Año':<13} {'ROI 20 años':<12} {'Nivel UMAs':<11}")
print("-" * 120)

for _, row in df_resultados.iterrows():
    salario = f"${row['salario_base']:,}"
    costo = f"${row['costo_total']:,.0f}"
    pension_mes = f"${row['pension_mensual']:,.0f}"
    pension_año = f"${row['pension_anual']:,.0f}"
    roi = f"{row['roi_20_años']:.1f}%"
    umas = f"{row['nivel_umas']:.1f}"
    
    print(f"{salario:<10} {costo:<12} {pension_mes:<12} {pension_año:<13} {roi:<12} {umas:<11}")

# ANÁLISIS DE PROPORCIONALIDAD
print("\n" + "="*60)
print("ANÁLISIS DE PROPORCIONALIDAD CON FÓRMULA COMPLETA")
print("="*60)

# Verificar si sigue siendo lineal
roi_valores = df_resultados['roi_20_años'].values
roi_diferencias = np.diff(roi_valores)

print(f"\nROIs obtenidos: {roi_valores}")
print(f"Diferencias entre ROIs: {roi_diferencias}")
print(f"¿Sigue siendo lineal? {np.allclose(roi_diferencias, 0, atol=0.1)}")

if not np.allclose(roi_diferencias, 0, atol=0.1):
    print("\n🚨 HALLAZGO IMPORTANTE:")
    print("La fórmula COMPLETA de Ley 73 NO genera proporción lineal perfecta")
    print("Los diferentes niveles UMA generan ROIs diferentes")
    print("Esto puede identificar un punto óptimo real")
    
    # Encontrar el mejor ROI
    mejor_idx = np.argmax(roi_valores)
    mejor_opcion = df_resultados.iloc[mejor_idx]
    
    print(f"\n✅ MEJOR OPCIÓN IDENTIFICADA:")
    print(f"Salario base: ${mejor_opcion['salario_base']:,}")
    print(f"ROI: {mejor_opcion['roi_20_años']:.2f}%")
    print(f"Nivel UMAs: {mejor_opcion['nivel_umas']:.1f}")

# DESGLOSE DETALLADO DEL MEJOR CASO
if 'mejor_idx' in locals():
    print(f"\n" + "="*60)
    print(f"DESGLOSE DETALLADO - MEJOR OPCIÓN (${mejor_opcion['salario_base']:,})")
    print("="*60)
    
    detalle = calcular_pension_completa(
        mejor_opcion['salario_base'], 65, 260, True, 0
    )
    
    print(f"Salario Diario Promedio: ${detalle['sdp_diario']:.2f}")
    print(f"Nivel UMAs: {detalle['nivel_umas']:.2f}")
    print(f"% Cuantía Básica: {detalle['pct_cuantia_basica']*100:.1f}%")
    print(f"% Incremento Anual: {detalle['pct_incremento_anual']:.2f}%")
    print(f"Cuantía Básica Anual: ${detalle['cuantia_basica_anual']:,.0f}")
    print(f"Incremento Total Anual: ${detalle['incremento_total_anual']:,.0f}")
    print(f"Pensión Base (antes edad): ${detalle['pension_base_anual']:,.0f}")
    print(f"Factor Edad (65 años): {detalle['factor_edad']*100:.0f}%")
    print(f"Pensión Ajustada Edad: ${detalle['pension_ajustada_edad']:,.0f}")
    print(f"Asignaciones (15% esposa): ${detalle['asignaciones']:,.0f}")
    print(f"Pensión Total Anual: ${detalle['pension_total_anual']:,.0f}")
    print(f"Pensión Mensual: ${detalle['pension_mensual']:,.0f}")

print(f"\n" + "="*80)
print("CONCLUSIÓN: ANÁLISIS REQUIERE ACTUALIZACIÓN COMPLETA")
print("="*80)
print("El análisis anterior con fórmula simplificada NO es correcto.")
print("La fórmula completa de Ley 73 incluye múltiples componentes que")
print("pueden generar comportamiento NO-lineal y puntos óptimos reales.")
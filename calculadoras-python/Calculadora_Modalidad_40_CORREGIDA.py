#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CALCULADORA MODALIDAD 40 CORREGIDA - TABLAS VARIABLES LEY 73
Versión: 3.0 - Noviembre 2025 (CORREGIDA)
Autor: Análisis Actuarial Especializado

Esta calculadora usa las TABLAS REALES de porcentajes variables
según el nivel del Salario Diario Promedio expresado en UMAs.
"""

import math
from datetime import datetime
from typing import Dict, Tuple, List

class CalculadoraModalidad40Corregida:
    """
    Calculadora CORREGIDA para análisis de Modalidad 40 IMSS bajo Ley 73
    Usa tablas variables de porcentajes según SDP/UMA
    """
    
    def __init__(self):
        """Inicializar con valores oficiales 2025 y tablas variables"""
        # Valores oficiales 2025
        self.uma_diaria_2025 = 113.14
        self.uma_mensual_2025 = 3439.46
        self.tope_maximo_umas = 25
        self.tope_diario_2025 = self.uma_diaria_2025 * self.tope_maximo_umas
        
        # Proyecciones UMA oficiales basadas en análisis INEGI/Banxico (inflación proyectada)
        self.uma_proyecciones = {
            # Valores históricos oficiales (INEGI)
            2016: 73.04,
            2017: 80.60,
            2018: 84.39,
            2019: 86.88,
            2020: 89.62,
            2021: 92.97,
            2022: 96.22,
            2023: 103.74,
            2024: 108.57,
            2025: 113.14,
            # Proyecciones profesionales (Encuesta Banxico/Citi)
            2026: 117.47,  # +3.8% inflación proyectada
            2027: 121.82,  # +3.7% inflación proyectada
            2028: 126.20,  # +3.6% inflación proyectada
            2029: 130.62,  # +3.5% inflación proyectada
            2030: 135.08   # +3.4% inflación proyectada
        }
        
        # Tasas de inflación proyectadas para referencia
        self.inflacion_proyectada = {
            2026: 3.80,
            2027: 3.70,
            2028: 3.60,
            2029: 3.50,
            2030: 3.40
        }
        
        # Tablas oficiales de tasas Modalidad 40 (incremento anual)
        self.tasas_modalidad40 = {
            2021: 10.075,
            2022: 10.075,
            2023: 11.166,
            2024: 12.256,
            2025: 13.347,
            2026: 14.438,
            2027: 15.528,
            2028: 16.619,
            2029: 17.709,
            2030: 18.000
        }
        
        # TABLAS REALES DE PORCENTAJES VARIABLES LEY 73
        # Basadas en múltiplos de UMA (VSM)
        self.tabla_porcentajes_ley73 = [
            {"rango_min": 0.00, "rango_max": 1.00, "cuantia_basica": 80.00, "incremento_anual": 0.56},
            {"rango_min": 1.01, "rango_max": 1.25, "cuantia_basica": 77.11, "incremento_anual": 0.81},
            {"rango_min": 1.26, "rango_max": 1.50, "cuantia_basica": 55.18, "incremento_anual": 1.18},
            {"rango_min": 1.51, "rango_max": 1.75, "cuantia_basica": 49.23, "incremento_anual": 1.43},
            {"rango_min": 1.76, "rango_max": 2.00, "cuantia_basica": 42.67, "incremento_anual": 1.62},
            {"rango_min": 2.01, "rango_max": 2.25, "cuantia_basica": 37.65, "incremento_anual": 1.76},
            {"rango_min": 2.26, "rango_max": 2.50, "cuantia_basica": 33.68, "incremento_anual": 1.87},
            {"rango_min": 2.51, "rango_max": 2.75, "cuantia_basica": 30.48, "incremento_anual": 1.96},
            {"rango_min": 2.76, "rango_max": 3.00, "cuantia_basica": 27.83, "incremento_anual": 2.03},
            {"rango_min": 3.01, "rango_max": 3.25, "cuantia_basica": 25.60, "incremento_anual": 2.10},
            {"rango_min": 3.26, "rango_max": 3.50, "cuantia_basica": 23.70, "incremento_anual": 2.15},
            {"rango_min": 3.51, "rango_max": 3.75, "cuantia_basica": 22.07, "incremento_anual": 2.20},
            {"rango_min": 3.76, "rango_max": 4.00, "cuantia_basica": 20.65, "incremento_anual": 2.24},
            {"rango_min": 4.01, "rango_max": 4.25, "cuantia_basica": 19.39, "incremento_anual": 2.27},
            {"rango_min": 4.26, "rango_max": 4.50, "cuantia_basica": 18.29, "incremento_anual": 2.30},
            {"rango_min": 4.51, "rango_max": 4.75, "cuantia_basica": 17.30, "incremento_anual": 2.33},
            {"rango_min": 4.76, "rango_max": 5.00, "cuantia_basica": 16.41, "incremento_anual": 2.36},
            {"rango_min": 5.01, "rango_max": 5.25, "cuantia_basica": 15.61, "incremento_anual": 2.38},
            {"rango_min": 5.26, "rango_max": 5.50, "cuantia_basica": 14.88, "incremento_anual": 2.40},
            {"rango_min": 5.51, "rango_max": 5.75, "cuantia_basica": 14.22, "incremento_anual": 2.42},
            {"rango_min": 5.76, "rango_max": 6.00, "cuantia_basica": 13.62, "incremento_anual": 2.43},
            {"rango_min": 6.01, "rango_max": float('inf'), "cuantia_basica": 13.00, "incremento_anual": 2.45}
        ]
        
        # Porcentajes de asignaciones familiares (estos sí son fijos)
        self.ayuda_esposa_pct = 0.15        # 15% si existe esposa
        self.ayuda_hijo_pct = 0.10          # 10% por hijo menor/estudiando
        self.ayuda_padres_pct = 0.20        # 20% si no hay viuda/huérfanos (CORREGIDO: era 10%)
        self.ayuda_soledad_pct = 0.15       # 15% si no tiene esposa (ayuda por soledad)
        self.incremento_vejez_pct = 0.11    # 11% a partir de 65 años
        
        # Tabla de porcentajes por edad (cesantía en edad avanzada)
        self.tabla_edad = {
            60: 0.75,  # 75%
            61: 0.80,  # 80%
            62: 0.85,  # 85%
            63: 0.90,  # 90%
            64: 0.95,  # 95%
            65: 1.00   # 100%
        }
        
        # Mínimo garantizado (salario mínimo regional)
        self.minimo_garantizado_diario = 248.93
        self.minimo_garantizado_mensual = self.minimo_garantizado_diario * 30.4
    
    def get_uma_para_año(self, año: int) -> float:
        """
        Obtener valor UMA proyectado para un año específico
        Basado en valores históricos INEGI y proyecciones Banxico/analistas
        
        Args:
            año: Año para el cual obtener UMA
            
        Returns:
            Valor UMA diario proyectado
        """
        if año in self.uma_proyecciones:
            return self.uma_proyecciones[año]
        elif año < 2025:
            # Para años históricos no incluidos, usar 2025 como base
            return self.uma_diaria_2025  
        else:
            # Extrapolar para años posteriores a 2030 usando última tasa proyectada (3.4%)
            base_year = max([y for y in self.uma_proyecciones.keys() if y <= año])
            years_ahead = año - base_year
            return self.uma_proyecciones[base_year] * (1.034 ** years_ahead)
    
    def buscar_porcentajes_por_sdp(self, sdp_diario: float, uma_diaria: float = None) -> Tuple[float, float]:
        """
        Buscar porcentajes de cuantía básica e incremento según SDP
        
        Args:
            sdp_diario: Salario Diario Promedio
            uma_diaria: UMA diaria (usa 2025 si no se especifica)
            
        Returns:
            Tuple (cuantia_basica_pct, incremento_anual_pct)
        """
        if uma_diaria is None:
            uma_diaria = self.uma_diaria_2025
        
        # Calcular múltiple de UMA (VSM)
        multiple_uma = sdp_diario / uma_diaria
        
        # Buscar en la tabla
        for rango in self.tabla_porcentajes_ley73:
            if rango["rango_min"] <= multiple_uma <= rango["rango_max"]:
                return (rango["cuantia_basica"] / 100, rango["incremento_anual"] / 100)
        
        # Si no encuentra (no debería pasar), usar los más altos
        return (0.13, 0.0245)  # 13% y 2.45%
    
    def calcular_costo_mensual(self, sbc_diario: float, año: int) -> float:
        """
        Calcular el costo mensual de Modalidad 40 para un SBC y año dados
        ACTUALIZADO: Considera incrementos UMA anuales
        
        Args:
            sbc_diario: Salario Base de Cotización diario deseado
            año: Año de cotización
            
        Returns:
            Costo mensual en pesos
        """
        if año not in self.tasas_modalidad40:
            raise ValueError(f"Año {año} no válido. Use años 2021-2030")
        
        # FIXED: Usar UMA del año correspondiente para mantener múltiplos UMA consistentes
        uma_año = self.get_uma_para_año(año)
        uma_2025 = self.uma_proyecciones[2025]
        
        # Ajustar SBC para mantener el mismo múltiplo de UMA
        multiple_uma = sbc_diario / uma_2025  # Múltiplo UMA deseado
        sbc_ajustado = multiple_uma * uma_año  # SBC en pesos del año
        
        sbc_mensual = sbc_ajustado * 30.4  # Promedio días por mes
        tasa = self.tasas_modalidad40[año] / 100
        return sbc_mensual * tasa
    
    def calcular_inversion_total_5_años(self, sbc_diario: float, año_inicio: int = 2025) -> Dict:
        """
        Calcular inversión total durante hasta 6 años con tasas progresivas (2025-2030)
        
        Args:
            sbc_diario: SBC diario deseado
            año_inicio: Año de inicio (default 2025)
            
        Returns:
            Dictionary con desglose anual y total
        """
        resultado = {
            'desglose_anual': {},
            'total_5_años': 0,
            'promedio_mensual': 0
        }
        
        total = 0
        # Calcular proyecciones hasta 2030 para mostrar todas las tasas
        años_calculados = 0
        for i in range(6):  # 2025-2030 = 6 años
            año = año_inicio + i
            if año > 2030:  # No calcular más allá de 2030
                break
            costo_mensual = self.calcular_costo_mensual(sbc_diario, año)
            costo_anual = costo_mensual * 12
            total += costo_anual
            años_calculados += 1
            
            resultado['desglose_anual'][año] = {
                'tasa_pct': self.tasas_modalidad40[año],
                'costo_mensual': costo_mensual,
                'costo_anual': costo_anual
            }
        
        resultado['total_5_años'] = total
        resultado['promedio_mensual'] = total / (años_calculados * 12)  # años * 12 meses
        
        return resultado
    
    def calcular_inversion_total_años(self, sbc_diario: float, año_inicio: int = 2025, años_cotizar: int = 5) -> Dict:
        """
        Calcular inversión total durante el número de años especificado
        
        Args:
            sbc_diario: SBC diario deseado
            año_inicio: Año de inicio (default 2025)
            años_cotizar: Número de años a cotizar (default 5, puede ser menor)
            
        Returns:
            Dictionary con desglose anual y total
        """
        resultado = {
            'desglose_anual': {},
            'total_años': 0,
            'promedio_mensual': 0,
            'años_cotizados': años_cotizar
        }
        
        total = 0
        for i in range(años_cotizar):
            año = año_inicio + i
            costo_mensual = self.calcular_costo_mensual(sbc_diario, año)
            costo_anual = costo_mensual * 12
            total += costo_anual
            
            resultado['desglose_anual'][año] = {
                'tasa_pct': self.tasas_modalidad40[año],
                'costo_mensual': costo_mensual,
                'costo_anual': costo_anual
            }
        
        resultado['total_años'] = total
        resultado['promedio_mensual'] = total / (años_cotizar * 12)
        
        return resultado
    
    def calcular_pension_ley73_corregida(self, 
                                       semanas_cotizadas: int,
                                       sdp_diario: float,
                                       edad_pension: int,
                                       tiene_esposa: bool = False,
                                       num_hijos_dependientes: int = 0,
                                       tiene_padres_dependientes: bool = False,
                                       uma_diaria_referencia: float = None) -> Dict:
        """
        Calcular pensión completa bajo Ley 73 con TABLAS VARIABLES CORRECTAS
        
        Args:
            semanas_cotizadas: Total de semanas cotizadas
            sdp_diario: Salario Diario Promedio (últimas 250 semanas)
            edad_pension: Edad al momento de pensionarse
            tiene_esposa: Si tiene esposa/concubina
            num_hijos_dependientes: Número de hijos menores o estudiando
            tiene_padres_dependientes: Si tiene padres dependientes (solo si no hay viuda/huérfanos)
            uma_diaria_referencia: UMA a usar para cálculo (default: 2025)
            
        Returns:
            Dictionary con desglose completo de la pensión
        """
        # Validaciones
        if semanas_cotizadas < 500:
            return {'error': 'Requiere mínimo 500 semanas cotizadas'}
        
        if uma_diaria_referencia is None:
            uma_diaria_referencia = self.uma_diaria_2025
        
        # 1. BUSCAR PORCENTAJES SEGÚN SDP/UMA
        cuantia_basica_pct, incremento_anual_pct = self.buscar_porcentajes_por_sdp(
            sdp_diario, uma_diaria_referencia
        )
        
        # 2. CUANTÍA BÁSICA (porcentaje variable según tabla)
        cuantia_basica_anual = sdp_diario * cuantia_basica_pct * 365
        
        # 3. INCREMENTO POR AÑOS ADICIONALES (porcentaje variable según tabla)
        # Cada año completo después de 500 semanas
        semanas_adicionales = semanas_cotizadas - 500
        años_adicionales = math.floor(semanas_adicionales / 52)
        incremento_anual = sdp_diario * incremento_anual_pct * 365 * años_adicionales
        
        # 4. PENSIÓN BASE (Cuantía Básica + Incrementos)
        pension_base_anual = cuantia_basica_anual + incremento_anual
        
        # 5. ASIGNACIONES FAMILIARES
        ayuda_esposa_anual = 0
        ayuda_soledad_anual = 0
        
        if tiene_esposa:
            ayuda_esposa_anual = pension_base_anual * self.ayuda_esposa_pct
        else:
            # Si no tiene esposa, aplica ayuda por soledad
            ayuda_soledad_anual = pension_base_anual * self.ayuda_soledad_pct
        
        ayuda_hijos_anual = 0
        if num_hijos_dependientes > 0:
            ayuda_hijos_anual = pension_base_anual * self.ayuda_hijo_pct * num_hijos_dependientes
        
        ayuda_padres_anual = 0
        if tiene_padres_dependientes and not tiene_esposa and num_hijos_dependientes == 0:
            ayuda_padres_anual = pension_base_anual * self.ayuda_padres_pct
        
        # 6. PENSIÓN CON ASIGNACIONES
        total_asignaciones = ayuda_esposa_anual + ayuda_hijos_anual + ayuda_padres_anual + ayuda_soledad_anual
        pension_con_asignaciones = pension_base_anual + total_asignaciones
        
        # 7. FACTOR POR EDAD (si es cesantía en edad avanzada antes de 65)
        factor_edad = 1.0
        if edad_pension < 65:
            factor_edad = self.tabla_edad.get(edad_pension, 0.75)
        
        pension_ajustada_edad = pension_con_asignaciones * factor_edad
        
        # 8. INCREMENTO POR VEJEZ (11% si tiene 65 años o más)
        incremento_vejez_anual = 0
        if edad_pension >= 65:
            incremento_vejez_anual = pension_ajustada_edad * self.incremento_vejez_pct
        
        # 9. PENSIÓN FINAL
        pension_final_anual = pension_ajustada_edad + incremento_vejez_anual
        
        # 10. VERIFICAR MÍNIMO GARANTIZADO
        if pension_final_anual < self.minimo_garantizado_mensual * 12:
            pension_final_anual = self.minimo_garantizado_mensual * 12
            es_minimo_garantizado = True
        else:
            es_minimo_garantizado = False
        
        # Convertir a valores mensuales y calcular múltiple UMA
        multiple_uma = sdp_diario / uma_diaria_referencia
        
        return {
            'sdp_diario': sdp_diario,
            'multiple_uma': multiple_uma,
            'cuantia_basica_pct': cuantia_basica_pct * 100,
            'incremento_anual_pct': incremento_anual_pct * 100,
            'semanas_cotizadas': semanas_cotizadas,
            'años_adicionales': años_adicionales,
            'edad_pension': edad_pension,
            'factor_edad': factor_edad,
            
            # Componentes mensuales
            'cuantia_basica_mensual': cuantia_basica_anual / 12,
            'incremento_mensual': incremento_anual / 12,
            'pension_base_mensual': pension_base_anual / 12,
            
            # Asignaciones mensuales
            'ayuda_esposa_mensual': ayuda_esposa_anual / 12,
            'ayuda_hijos_mensual': ayuda_hijos_anual / 12,
            'ayuda_padres_mensual': ayuda_padres_anual / 12,
            'ayuda_soledad_mensual': ayuda_soledad_anual / 12,
            'total_asignaciones_mensual': total_asignaciones / 12,
            
            # Pensión con asignaciones
            'pension_con_asignaciones_mensual': pension_con_asignaciones / 12,
            
            # Ajuste por edad
            'pension_ajustada_edad_mensual': pension_ajustada_edad / 12,
            
            # Incremento por vejez
            'incremento_vejez_mensual': incremento_vejez_anual / 12,
            
            # Pensión final
            'pension_final_mensual': pension_final_anual / 12,
            
            # Información adicional
            'es_minimo_garantizado': es_minimo_garantizado,
            'minimo_garantizado_mensual': self.minimo_garantizado_mensual,
            
            # Factores aplicados
            'tiene_esposa': tiene_esposa,
            'num_hijos_dependientes': num_hijos_dependientes,
            'tiene_padres_dependientes': tiene_padres_dependientes,
            'aplica_incremento_vejez': edad_pension >= 65
        }
    
    def calcular_escenario_completo(self,
                                  semanas_cotizadas_actuales: int,
                                  sdp_actual_diario: float,
                                  sbc_modalidad40_diario: float,
                                  edad_pension: int,
                                  tiene_esposa: bool = False,
                                  num_hijos_dependientes: int = 0,
                                  tiene_padres_dependientes: bool = False,
                                  año_inicio: int = 2025,
                                  edad_actual: int = None) -> Dict:
        """
        Calcular escenario completo con TABLAS VARIABLES: situación actual vs con Modalidad 40
        
        Args:
            semanas_cotizadas_actuales: Semanas ya cotizadas
            sdp_actual_diario: SDP actual (últimas 250 semanas)
            sbc_modalidad40_diario: SBC deseado para Modalidad 40
            edad_pension: Edad al pensionarse
            tiene_esposa: Si tiene esposa/concubina
            num_hijos_dependientes: Número de hijos menores/estudiando
            tiene_padres_dependientes: Si tiene padres dependientes
            año_inicio: Año de inicio Modalidad 40
            
        Returns:
            Dictionary completo con ambos escenarios y análisis ROI
        """
        # Validar tope máximo
        if sbc_modalidad40_diario > self.tope_diario_2025:
            return {
                'error': f'SBC de ${sbc_modalidad40_diario:.2f} excede tope máximo de ${self.tope_diario_2025:.2f}'
            }
        
        # Validar límite legal de edad (65 años máximo para pensión IMSS)
        if edad_pension > 65:
            return {
                'error': f'Edad máxima legal para pensión IMSS: 65 años. Edad solicitada: {edad_pension} años.'
            }
        
        # ESCENARIO SIN MODALIDAD 40
        semanas_finales_sin_mod40 = semanas_cotizadas_actuales  # No cotiza más
        pension_sin_mod40 = self.calcular_pension_ley73_corregida(
            semanas_finales_sin_mod40, sdp_actual_diario, edad_pension,
            tiene_esposa, num_hijos_dependientes, tiene_padres_dependientes
        )
        
        # ESCENARIO CON MODALIDAD 40 (calcular semanas según años disponibles)
        # Calcular años reales disponibles desde edad actual hasta pensión
        if edad_actual is not None:
            años_disponibles = edad_pension - edad_actual
        else:
            # Fallback: asumir se retira a los 65 (máximo común)
            años_disponibles = max(1, 65 - edad_pension) if edad_pension < 65 else 1
        
        # Modalidad 40 permite máximo 6 años (hasta 2030), pero debe permitir mínimo 1 año
        años_para_modalidad40 = max(1, min(6, años_disponibles))
        semanas_modalidad40 = años_para_modalidad40 * 52
        semanas_finales_con_mod40 = semanas_cotizadas_actuales + semanas_modalidad40
        
        # Calcular nuevo SDP (promedio últimas 250 semanas)
        # Asumiendo que las 250 semanas incluyen principalmente Modalidad 40
        if semanas_cotizadas_actuales >= 250:
            # Las últimas 250 semanas serían principalmente del período Modalidad 40
            nuevo_sdp_diario = sbc_modalidad40_diario
        else:
            # Mezcla del SDP actual y el nuevo SBC
            semanas_antiguas_en_250 = 250 - (260 - (250 - semanas_cotizadas_actuales))
            if semanas_antiguas_en_250 < 0:
                semanas_antiguas_en_250 = 0
            
            peso_antiguo = semanas_antiguas_en_250 / 250
            peso_nuevo = 1 - peso_antiguo
            nuevo_sdp_diario = (sdp_actual_diario * peso_antiguo) + (sbc_modalidad40_diario * peso_nuevo)
        
        pension_con_mod40 = self.calcular_pension_ley73_corregida(
            semanas_finales_con_mod40, nuevo_sdp_diario, edad_pension,
            tiene_esposa, num_hijos_dependientes, tiene_padres_dependientes
        )
        
        # ANÁLISIS DE INVERSIÓN (usar años reales disponibles)
        inversion_mod40 = self.calcular_inversion_total_años(sbc_modalidad40_diario, año_inicio, años_para_modalidad40)
        
        # ANÁLISIS ROI
        diferencia_mensual = pension_con_mod40['pension_final_mensual'] - pension_sin_mod40['pension_final_mensual']
        diferencia_anual = diferencia_mensual * 12
        
        # ROI simple anual
        roi_anual = (diferencia_anual / inversion_mod40['total_años']) * 100
        
        # Período de recuperación
        años_recuperacion = inversion_mod40['total_años'] / diferencia_anual
        
        return {
            'inputs': {
                'semanas_cotizadas_actuales': semanas_cotizadas_actuales,
                'sdp_actual_diario': sdp_actual_diario,
                'sbc_modalidad40_diario': sbc_modalidad40_diario,
                'edad_pension': edad_pension,
                'tiene_esposa': tiene_esposa,
                'num_hijos_dependientes': num_hijos_dependientes,
                'tiene_padres_dependientes': tiene_padres_dependientes,
                'año_inicio': año_inicio
            },
            
            'sin_modalidad40': pension_sin_mod40,
            'con_modalidad40': pension_con_mod40,
            'nuevo_sdp_diario': nuevo_sdp_diario,
            
            'inversion': inversion_mod40,
            
            'analisis_roi': {
                'diferencia_mensual': diferencia_mensual,
                'diferencia_anual': diferencia_anual,
                'roi_anual_pct': roi_anual,
                'años_recuperacion': años_recuperacion,
                'factible': sbc_modalidad40_diario <= self.tope_diario_2025,
                'nivel_umas': sbc_modalidad40_diario / self.uma_diaria_2025
            }
        }

# Función de prueba
def main():
    """Función principal para probar la calculadora corregida"""
    print("🎯 CALCULADORA MODALIDAD 40 CORREGIDA - TABLAS VARIABLES LEY 73")
    print("=" * 70)
    
    calc = CalculadoraModalidad40Corregida()
    
    # Probar con el ejemplo del archivo CSV
    print("\n📋 PRUEBA CON EJEMPLO DEL ARCHIVO CSV:")
    print("-" * 40)
    
    # Datos del archivo CSV
    sdp_ejemplo = 2004.08
    uma_2018 = 80.60  # UMA del ejemplo
    
    # Buscar porcentajes
    cuantia_pct, incremento_pct = calc.buscar_porcentajes_por_sdp(sdp_ejemplo, uma_2018)
    multiple = sdp_ejemplo / uma_2018
    
    print(f"• SDP: ${sdp_ejemplo:.2f}")
    print(f"• UMA referencia: ${uma_2018:.2f}")
    print(f"• Múltiple UMA: {multiple:.2f}")
    print(f"• Cuantía básica: {cuantia_pct*100:.2f}%")
    print(f"• Incremento anual: {incremento_pct*100:.2f}%")
    
    # Comparar con tu caso (SDP actual bajo)
    print("\n📋 COMPARACIÓN CON TU CASO ACTUAL:")
    print("-" * 40)
    
    sdp_sergio = 222.02
    cuantia_sergio, incremento_sergio = calc.buscar_porcentajes_por_sdp(sdp_sergio)
    multiple_sergio = sdp_sergio / calc.uma_diaria_2025
    
    print(f"• SDP Sergio actual: ${sdp_sergio:.2f}")
    print(f"• UMA 2025: ${calc.uma_diaria_2025:.2f}")
    print(f"• Múltiple UMA: {multiple_sergio:.2f}")
    print(f"• Cuantía básica: {cuantia_sergio*100:.2f}%")
    print(f"• Incremento anual: {incremento_sergio*100:.2f}%")
    
    print(f"\n🎯 ¡ESTO EXPLICA LA DIFERENCIA!")
    print("Con SDP bajo (1.96 UMAs) aplican porcentajes MÁS ALTOS")
    print("que con SDP alto (24.86 UMAs)")


if __name__ == "__main__":
    main()
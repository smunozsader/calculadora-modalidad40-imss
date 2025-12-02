#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CALCULADORA UNIVERSAL MODALIDAD 40 - IMSS LEY 73
Versión: 2.0 - Noviembre 2025
Autor: Análisis Actuarial Especializado

Esta calculadora permite evaluar diferentes escenarios de Modalidad 40 
con inputs personalizables para cualquier usuario.
"""

import math
from datetime import datetime
from typing import Dict, Tuple, List

class CalculadoraModalidad40:
    """
    Calculadora completa para análisis de Modalidad 40 IMSS bajo Ley 73
    """
    
    def __init__(self):
        """Inicializar con valores oficiales 2025"""
        # Valores oficiales 2025
        self.uma_diaria_2025 = 113.14
        self.uma_mensual_2025 = 3439.46
        self.tope_maximo_umas = 25
        self.tope_diario_2025 = self.uma_diaria_2025 * self.tope_maximo_umas
        
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
        
        # Porcentajes fijos fórmula Ley 73
        self.cuantia_basica_pct = 0.13      # 13%
        self.incremento_anual_pct = 0.0245  # 2.45% por año adicional
        self.ayuda_esposa_pct = 0.15        # 15% si existe esposa
        self.ayuda_hijo_pct = 0.10          # 10% por hijo menor/estudiando
        self.ayuda_padres_pct = 0.20        # 20% si no hay viuda/huérfanos
        self.incremento_vejez_pct = 0.11    # 11% a partir de 65 años
        
        # Mínimo garantizado (salario mínimo regional)
        self.minimo_garantizado_diario = 248.93
        self.minimo_garantizado_mensual = self.minimo_garantizado_diario * 30.4
    
    def calcular_costo_mensual(self, sbc_diario: float, año: int) -> float:
        """
        Calcular el costo mensual de Modalidad 40 para un SBC y año dados
        
        Args:
            sbc_diario: Salario Base de Cotización diario deseado
            año: Año de cotización
            
        Returns:
            Costo mensual en pesos
        """
        if año not in self.tasas_modalidad40:
            raise ValueError(f"Año {año} no válido. Use años 2021-2030")
        
        sbc_mensual = sbc_diario * 30.4  # Promedio días por mes
        tasa = self.tasas_modalidad40[año] / 100
        return sbc_mensual * tasa
    
    def calcular_inversion_total_5_años(self, sbc_diario: float, año_inicio: int = 2025) -> Dict:
        """
        Calcular inversión total durante 5 años con tasas progresivas
        
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
        for i in range(5):
            año = año_inicio + i
            costo_mensual = self.calcular_costo_mensual(sbc_diario, año)
            costo_anual = costo_mensual * 12
            total += costo_anual
            
            resultado['desglose_anual'][año] = {
                'tasa_pct': self.tasas_modalidad40[año],
                'costo_mensual': costo_mensual,
                'costo_anual': costo_anual
            }
        
        resultado['total_5_años'] = total
        resultado['promedio_mensual'] = total / 60  # 5 años * 12 meses
        
        return resultado
    
    def calcular_pension_ley73(self, 
                              semanas_cotizadas: int,
                              sdp_diario: float,
                              edad_pension: int,
                              tiene_esposa: bool = False,
                              num_hijos_dependientes: int = 0,
                              tiene_padres_dependientes: bool = False) -> Dict:
        """
        Calcular pensión completa bajo Ley 73 con todos los componentes
        
        Args:
            semanas_cotizadas: Total de semanas cotizadas
            sdp_diario: Salario Diario Promedio (últimas 250 semanas)
            edad_pension: Edad al momento de pensionarse
            tiene_esposa: Si tiene esposa/concubina
            num_hijos_dependientes: Número de hijos menores o estudiando
            tiene_padres_dependientes: Si tiene padres dependientes (solo si no hay viuda/huérfanos)
            
        Returns:
            Dictionary con desglose completo de la pensión
        """
        # Validaciones
        if semanas_cotizadas < 500:
            return {'error': 'Requiere mínimo 500 semanas cotizadas'}
        
        # 1. CUANTÍA BÁSICA (13% del SDP)
        cuantia_basica_anual = sdp_diario * self.cuantia_basica_pct * 365
        
        # 2. INCREMENTO POR AÑOS ADICIONALES
        # Cada año completo después de 500 semanas = 2.45% adicional
        semanas_adicionales = semanas_cotizadas - 500
        años_adicionales = math.floor(semanas_adicionales / 52)
        incremento_anual = sdp_diario * self.incremento_anual_pct * 365 * años_adicionales
        
        # 3. PENSIÓN BASE (Cuantía Básica + Incrementos)
        pension_base_anual = cuantia_basica_anual + incremento_anual
        
        # 4. ASIGNACIONES FAMILIARES
        ayuda_esposa_anual = 0
        if tiene_esposa:
            ayuda_esposa_anual = pension_base_anual * self.ayuda_esposa_pct
        
        ayuda_hijos_anual = 0
        if num_hijos_dependientes > 0:
            ayuda_hijos_anual = pension_base_anual * self.ayuda_hijo_pct * num_hijos_dependientes
        
        ayuda_padres_anual = 0
        if tiene_padres_dependientes and not tiene_esposa and num_hijos_dependientes == 0:
            ayuda_padres_anual = pension_base_anual * self.ayuda_padres_pct
        
        # 5. PENSIÓN CON ASIGNACIONES
        total_asignaciones = ayuda_esposa_anual + ayuda_hijos_anual + ayuda_padres_anual
        pension_con_asignaciones = pension_base_anual + total_asignaciones
        
        # 6. INCREMENTO POR VEJEZ (11% si tiene 65 años o más)
        incremento_vejez_anual = 0
        if edad_pension >= 65:
            incremento_vejez_anual = pension_con_asignaciones * self.incremento_vejez_pct
        
        # 7. PENSIÓN FINAL
        pension_final_anual = pension_con_asignaciones + incremento_vejez_anual
        
        # 8. VERIFICAR MÍNIMO GARANTIZADO
        if pension_final_anual < self.minimo_garantizado_mensual * 12:
            pension_final_anual = self.minimo_garantizado_mensual * 12
            es_minimo_garantizado = True
        else:
            es_minimo_garantizado = False
        
        # Convertir a valores mensuales
        return {
            'sdp_diario': sdp_diario,
            'semanas_cotizadas': semanas_cotizadas,
            'años_adicionales': años_adicionales,
            'edad_pension': edad_pension,
            
            # Componentes mensuales
            'cuantia_basica_mensual': cuantia_basica_anual / 12,
            'incremento_mensual': incremento_anual / 12,
            'pension_base_mensual': pension_base_anual / 12,
            
            # Asignaciones mensuales
            'ayuda_esposa_mensual': ayuda_esposa_anual / 12,
            'ayuda_hijos_mensual': ayuda_hijos_anual / 12,
            'ayuda_padres_mensual': ayuda_padres_anual / 12,
            'total_asignaciones_mensual': total_asignaciones / 12,
            
            # Pensión con asignaciones
            'pension_con_asignaciones_mensual': pension_con_asignaciones / 12,
            
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
                                  año_inicio: int = 2025) -> Dict:
        """
        Calcular escenario completo: situación actual vs con Modalidad 40
        
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
        
        # ESCENARIO SIN MODALIDAD 40
        semanas_finales_sin_mod40 = semanas_cotizadas_actuales  # No cotiza más
        pension_sin_mod40 = self.calcular_pension_ley73(
            semanas_finales_sin_mod40, sdp_actual_diario, edad_pension,
            tiene_esposa, num_hijos_dependientes, tiene_padres_dependientes
        )
        
        # ESCENARIO CON MODALIDAD 40 (5 años = 260 semanas)
        semanas_finales_con_mod40 = semanas_cotizadas_actuales + 260
        
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
        
        pension_con_mod40 = self.calcular_pension_ley73(
            semanas_finales_con_mod40, nuevo_sdp_diario, edad_pension,
            tiene_esposa, num_hijos_dependientes, tiene_padres_dependientes
        )
        
        # ANÁLISIS DE INVERSIÓN
        inversion_mod40 = self.calcular_inversion_total_5_años(sbc_modalidad40_diario, año_inicio)
        
        # ANÁLISIS ROI
        diferencia_mensual = pension_con_mod40['pension_final_mensual'] - pension_sin_mod40['pension_final_mensual']
        diferencia_anual = diferencia_mensual * 12
        
        # ROI simple anual
        roi_anual = (diferencia_anual / inversion_mod40['total_5_años']) * 100
        
        # Período de recuperación
        años_recuperacion = inversion_mod40['total_5_años'] / diferencia_anual
        
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
    
    def generar_reporte_completo(self, resultado: Dict) -> str:
        """
        Generar reporte textual completo del análisis
        
        Args:
            resultado: Dictionary del análisis completo
            
        Returns:
            String con reporte formateado
        """
        if 'error' in resultado:
            return f"❌ ERROR: {resultado['error']}"
        
        inputs = resultado['inputs']
        sin_mod40 = resultado['sin_modalidad40']
        con_mod40 = resultado['con_modalidad40']
        roi = resultado['analisis_roi']
        inversion = resultado['inversion']
        
        reporte = f"""
===============================================================================
🎯 ANÁLISIS COMPLETO MODALIDAD 40 - LEY 73
===============================================================================

📊 DATOS DE ENTRADA:
─────────────────────
• Semanas cotizadas actuales: {inputs['semanas_cotizadas_actuales']:,}
• SDP actual: ${inputs['sdp_actual_diario']:.2f} diario
• SBC deseado Modalidad 40: ${inputs['sbc_modalidad40_diario']:.2f} diario ({roi['nivel_umas']:.1f} UMAs)
• Edad de pensión: {inputs['edad_pension']} años
• Tiene esposa/concubina: {'✅ SÍ' if inputs['tiene_esposa'] else '❌ NO'}
• Hijos dependientes: {inputs['num_hijos_dependientes']}
• Padres dependientes: {'✅ SÍ' if inputs['tiene_padres_dependientes'] else '❌ NO'}

💰 INVERSIÓN REQUERIDA (5 años):
──────────────────────────────────
• Total inversión: ${inversion['total_5_años']:,.0f}
• Promedio mensual: ${inversion['promedio_mensual']:,.0f}

Desglose anual:"""
        
        for año, datos in inversion['desglose_anual'].items():
            reporte += f"""
  {año}: ${datos['costo_mensual']:,.0f}/mes (Tasa: {datos['tasa_pct']:.3f}%) = ${datos['costo_anual']:,.0f}/año"""
        
        reporte += f"""

🏆 RESULTADOS COMPARATIVOS:
─────────────────────────────

📍 SIN MODALIDAD 40:
• Semanas totales: {sin_mod40['semanas_cotizadas']:,}
• SDP: ${sin_mod40['sdp_diario']:.2f} diario
• Cuantía básica: ${sin_mod40['cuantia_basica_mensual']:,.0f}/mes
• Incrementos: ${sin_mod40['incremento_mensual']:,.0f}/mes
• Asignaciones familiares: ${sin_mod40['total_asignaciones_mensual']:,.0f}/mes
• Incremento vejez: ${sin_mod40['incremento_vejez_mensual']:,.0f}/mes
• 🎯 PENSIÓN FINAL: ${sin_mod40['pension_final_mensual']:,.0f}/mes

📈 CON MODALIDAD 40:
• Semanas totales: {con_mod40['semanas_cotizadas']:,}
• SDP final: ${resultado['nuevo_sdp_diario']:.2f} diario
• Cuantía básica: ${con_mod40['cuantia_basica_mensual']:,.0f}/mes
• Incrementos: ${con_mod40['incremento_mensual']:,.0f}/mes
• Asignaciones familiares: ${con_mod40['total_asignaciones_mensual']:,.0f}/mes
• Incremento vejez: ${con_mod40['incremento_vejez_mensual']:,.0f}/mes
• 🎯 PENSIÓN FINAL: ${con_mod40['pension_final_mensual']:,.0f}/mes

📈 ANÁLISIS DE RENTABILIDAD:
──────────────────────────────
• 💡 Diferencia mensual: +${roi['diferencia_mensual']:,.0f}
• 📅 Diferencia anual: +${roi['diferencia_anual']:,.0f}
• 🚀 ROI anual: {roi['roi_anual_pct']:.1f}%
• ⏱️  Recuperación inversión: {roi['años_recuperacion']:.1f} años
• ✅ Factible: {'SÍ (dentro del tope)' if roi['factible'] else 'NO (excede tope)'}

📋 DESGLOSE DETALLADO ASIGNACIONES:
──────────────────────────────────────"""
        
        if inputs['tiene_esposa']:
            reporte += f"""
• Ayuda esposa/concubina (15%): ${con_mod40['ayuda_esposa_mensual']:,.0f}/mes"""
        
        if inputs['num_hijos_dependientes'] > 0:
            reporte += f"""
• Ayuda hijos dependientes (10% c/u): ${con_mod40['ayuda_hijos_mensual']:,.0f}/mes"""
        
        if inputs['tiene_padres_dependientes']:
            reporte += f"""
• Ayuda padres (20%): ${con_mod40['ayuda_padres_mensual']:,.0f}/mes"""
        
        if inputs['edad_pension'] >= 65:
            reporte += f"""
• Incremento por vejez (11%): ${con_mod40['incremento_vejez_mensual']:,.0f}/mes"""
        
        reporte += f"""

✅ CONCLUSIÓN:
──────────────
{'🎯 MODALIDAD 40 ES ALTAMENTE RENTABLE' if roi['roi_anual_pct'] > 50 else '⚠️  EVALUAR OTRAS OPCIONES'}
Invirtiendo ${inversion['total_5_años']:,.0f} en 5 años obtienes ${roi['diferencia_mensual']:,.0f} adicionales mensuales de por vida.

===============================================================================
"""
        return reporte


# Función principal para uso interactivo
def main():
    """Función principal para uso interactivo de la calculadora"""
    print("🎯 CALCULADORA UNIVERSAL MODALIDAD 40 - IMSS LEY 73")
    print("=" * 60)
    
    calc = CalculadoraModalidad40()
    
    # Ejemplo de uso con datos del caso Sergio
    print("\n📋 EJEMPLO: Caso Sergio (MUMS640728UQ0)")
    print("-" * 40)
    
    resultado = calc.calcular_escenario_completo(
        semanas_cotizadas_actuales=758,
        sdp_actual_diario=222.02,
        sbc_modalidad40_diario=2464.58,  # Para $10K/mes
        edad_pension=65,
        tiene_esposa=True,  # Tiene concubina
        num_hijos_dependientes=0,  # Hijos mayores de edad
        tiene_padres_dependientes=False
    )
    
    print(calc.generar_reporte_completo(resultado))


if __name__ == "__main__":
    main()
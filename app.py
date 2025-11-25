#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEB APP - CALCULADORA MODALIDAD 40 IMSS
Versión: 1.0 - Noviembre 2025

Aplicación web Flask para calcular pensiones Modalidad 40 IMSS
Usa las tablas variables corregidas de Ley 73
"""

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import sys
import os

# Importar la calculadora corregida
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Calculadora_Modalidad_40_CORREGIDA import CalculadoraModalidad40Corregida

app = Flask(__name__)
app.config['SECRET_KEY'] = 'modalidad40-imss-2025'

@app.route('/')
def index():
    """Página principal de la calculadora"""
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    """Endpoint para calcular la pensión"""
    try:
        # Obtener datos del formulario
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = [
            'semanas_cotizadas', 'sdp_actual', 'sbc_modalidad40', 'edad_pension'
        ]
        
        for field in required_fields:
            if field not in data or data[field] == '':
                return jsonify({
                    'error': f'Campo requerido faltante: {field}'
                }), 400
        
        # Convertir a números
        semanas_cotizadas = int(data['semanas_cotizadas'])
        sdp_actual = float(data['sdp_actual'])
        sbc_modalidad40 = float(data['sbc_modalidad40'])
        edad_pension = int(data['edad_pension'])
        
        # Opciones familiares
        tiene_esposa = data.get('tiene_esposa', False)
        num_hijos = int(data.get('num_hijos', 0))
        tiene_padres = data.get('tiene_padres', False)
        año_inicio = int(data.get('año_inicio', 2025))
        
        # Validaciones básicas
        if semanas_cotizadas < 500:
            return jsonify({
                'error': 'Se requieren mínimo 500 semanas cotizadas para acceder a pensión'
            }), 400
        
        if edad_pension < 60:
            return jsonify({
                'error': 'Edad mínima para pensión: 60 años'
            }), 400
        
        # Calcular con la calculadora corregida
        calc = CalculadoraModalidad40Corregida()
        
        resultado = calc.calcular_escenario_completo(
            semanas_cotizadas_actuales=semanas_cotizadas,
            sdp_actual_diario=sdp_actual,
            sbc_modalidad40_diario=sbc_modalidad40,
            edad_pension=edad_pension,
            tiene_esposa=tiene_esposa,
            num_hijos_dependientes=num_hijos,
            tiene_padres_dependientes=tiene_padres,
            año_inicio=año_inicio
        )
        
        if 'error' in resultado:
            return jsonify({'error': resultado['error']}), 400
        
        # Formatear respuesta para el frontend
        respuesta = {
            'success': True,
            'sin_modalidad40': {
                'pension_base': round(resultado['sin_modalidad40']['pension_base_mensual'], 0),
                'asignaciones': round(resultado['sin_modalidad40']['total_asignaciones_mensual'], 0),
                'pension_total': round(resultado['sin_modalidad40']['pension_final_mensual'], 0),
                'cuantia_pct': round(resultado['sin_modalidad40']['cuantia_basica_pct'], 2),
                'incremento_pct': round(resultado['sin_modalidad40']['incremento_anual_pct'], 2),
                'multiple_uma': round(resultado['sin_modalidad40']['multiple_uma'], 2)
            },
            'con_modalidad40': {
                'pension_base': round(resultado['con_modalidad40']['pension_base_mensual'], 0),
                'asignaciones': round(resultado['con_modalidad40']['total_asignaciones_mensual'], 0),
                'pension_total': round(resultado['con_modalidad40']['pension_final_mensual'], 0),
                'cuantia_pct': round(resultado['con_modalidad40']['cuantia_basica_pct'], 2),
                'incremento_pct': round(resultado['con_modalidad40']['incremento_anual_pct'], 2),
                'multiple_uma': round(resultado['con_modalidad40']['multiple_uma'], 2)
            },
            'inversion': {
                'total_5_años': round(resultado['inversion']['total_5_años'], 0),
                'promedio_mensual': round(resultado['inversion']['promedio_mensual'], 0),
                'desglose_anual': resultado['inversion']['desglose_anual']
            },
            'analisis_roi': {
                'diferencia_mensual': round(resultado['analisis_roi']['diferencia_mensual'], 0),
                'diferencia_anual': round(resultado['analisis_roi']['diferencia_anual'], 0),
                'roi_anual': round(resultado['analisis_roi']['roi_anual_pct'], 1),
                'años_recuperacion': round(resultado['analisis_roi']['años_recuperacion'], 1),
                'factible': resultado['analisis_roi']['factible'],
                'nivel_umas': round(resultado['analisis_roi']['nivel_umas'], 1)
            },
            'fecha_calculo': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'tope_maximo': calc.tope_diario_2025,
            'uma_2025': calc.uma_diaria_2025
        }
        
        return jsonify(respuesta)
        
    except ValueError as e:
        return jsonify({'error': f'Error en formato de números: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@app.route('/info')
def info():
    """Página con información sobre Modalidad 40"""
    return render_template('info.html')

@app.route('/api/topes')
def api_topes():
    """API para obtener topes y valores actuales"""
    calc = CalculadoraModalidad40Corregida()
    return jsonify({
        'uma_diaria_2025': calc.uma_diaria_2025,
        'uma_mensual_2025': calc.uma_mensual_2025,
        'tope_diario_maximo': calc.tope_diario_2025,
        'tope_mensual_maximo': calc.tope_diario_2025 * 30.4,
        'minimo_garantizado_diario': calc.minimo_garantizado_diario,
        'minimo_garantizado_mensual': calc.minimo_garantizado_mensual,
        'tasas_modalidad40': calc.tasas_modalidad40
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
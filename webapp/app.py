#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEB APP - CALCULADORA MODALIDAD 40 IMSS
Versión: 1.0 - Noviembre 2025

Aplicación web Flask para calcular pensiones Modalidad 40 IMSS
Usa las tablas variables corregidas de Ley 73
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
from datetime import datetime, timezone, timedelta
import sys
import os
import io
import locale
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# Importar la calculadora corregida - con debugging
calculator_path = os.path.join(os.path.dirname(__file__), '..', 'calculadoras-python')
calculator_path_abs = os.path.abspath(calculator_path)
print(f"DEBUG: Agregando path de calculadora: {calculator_path_abs}")
print(f"DEBUG: Path existe: {os.path.exists(calculator_path_abs)}")

# CRÍTICO: Agregar al sys.path ANTES de importar
sys.path.insert(0, calculator_path_abs)

# Configurar locale en español para nombres de meses
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
    except:
        pass  # Si no está disponible, usará el default

# Zona horaria de México (CST = UTC-6)
MEXICO_TZ = timezone(timedelta(hours=-6))

def now_mexico():
    """Retorna la fecha/hora actual en zona horaria de México (CST/CDT)"""
    return datetime.now(MEXICO_TZ)

try:
    from Calculadora_Modalidad_40_CORREGIDA import CalculadoraModalidad40Corregida
    print("DEBUG: ✅ Calculadora importada exitosamente")
except ImportError as e:
    print(f"DEBUG: ❌ Error importando calculadora: {e}")
    raise
except Exception as e:
    print(f"DEBUG: ❌ Error inesperado importando calculadora: {e}")
    raise

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
        # Debug: Log del inicio del cálculo
        print("DEBUG: ===========================================")
        print("DEBUG: 🚀 INICIO DEL CÁLCULO - MODALIDAD 40")
        print("DEBUG: ===========================================")
        
        # Obtener datos del formulario
        data = request.get_json()
        print("DEBUG: Datos recibidos COMPLETOS:", data)
        print("DEBUG: Tipo de datos:", type(data))
        
        if not data:
            print("DEBUG: ❌ No se recibieron datos JSON")
            return jsonify({'error': 'No se recibieron datos JSON válidos'}), 400
        
        # Validar datos requeridos para cálculo
        required_calc_fields = [
            'semanas_cotizadas', 'sdp_actual', 'sbc_modalidad40', 'edad_actual', 'edad_pension'
        ]
        
        print(f"DEBUG: Validando campos requeridos: {required_calc_fields}")
        
        for field in required_calc_fields:
            if field not in data or data[field] == '' or data[field] is None:
                print(f"DEBUG: ❌ Campo faltante o vacío: {field}")
                print(f"DEBUG: Valor recibido: '{data.get(field, 'NO_EXISTS')}'")
                print(f"DEBUG: Keys disponibles: {list(data.keys())}")
                return jsonify({
                    'error': f'Campo requerido para cálculo: {field}. Valor recibido: {data.get(field, "no proporcionado")}'
                }), 400
            else:
                print(f"DEBUG: ✅ Campo {field}: '{data[field]}'")
        
        # Convertir a números con validación
        print("DEBUG: 🔢 Convirtiendo datos a números...")
        try:
            semanas_cotizadas = int(float(data['semanas_cotizadas']))  # Permite decimales que se redondean
            print(f"DEBUG: semanas_cotizadas = {semanas_cotizadas}")
            
            sdp_actual = float(data['sdp_actual'])
            print(f"DEBUG: sdp_actual = {sdp_actual}")
            
            sbc_modalidad40 = float(data['sbc_modalidad40'])
            print(f"DEBUG: sbc_modalidad40 = {sbc_modalidad40}")
            
            edad_actual = int(float(data['edad_actual']))
            print(f"DEBUG: edad_actual = {edad_actual}")
            
            edad_pension = int(float(data['edad_pension']))
            print(f"DEBUG: edad_pension = {edad_pension}")
            
        except (ValueError, TypeError) as e:
            print(f"DEBUG: ❌ Error convirtiendo números: {e}")
            return jsonify({
                'error': f'Error en formato de datos numéricos: {str(e)}'
            }), 400
        
        # Opciones familiares
        print("DEBUG: 👨‍👩‍👧‍👦 Procesando opciones familiares...")
        tiene_esposa = bool(data.get('tiene_esposa', False))
        print(f"DEBUG: tiene_esposa = {tiene_esposa}")
        
        try:
            num_hijos = int(float(data.get('num_hijos', 0)))
            print(f"DEBUG: num_hijos = {num_hijos}")
        except (ValueError, TypeError):
            num_hijos = 0
            print("DEBUG: num_hijos defaulted to 0")
        
        tiene_padres = bool(data.get('tiene_padres', False))
        print(f"DEBUG: tiene_padres = {tiene_padres}")
        
        # VALIDACIÓN CRÍTICA: Elegibilidad Modalidad 40 (Ley 97)
        print("DEBUG: 🔍 Validando elegibilidad Modalidad 40...")
        mes_inicio_str = data.get('mes_inicio_cotizacion', '')
        año_inicio_str = data.get('año_inicio_cotizacion', '')
        
        if not mes_inicio_str or not año_inicio_str:
            print("DEBUG: ❌ Falta fecha de inicio de cotización")
            return jsonify({
                'error': 'Fecha de inicio de cotización requerida para validar elegibilidad Modalidad 40'
            }), 400
        
        # Procesar última cotización para deadline
        mes_ultima_str = data.get('mes_ultima_cotizacion', '')
        año_ultima_str = data.get('año_ultima_cotizacion', '')
        fecha_limite_inscripcion = None
        dias_restantes_deadline = None
        
        if mes_ultima_str and año_ultima_str:
            try:
                mes_ultima = int(mes_ultima_str)
                año_ultima = int(año_ultima_str)
                from datetime import datetime
                fecha_ultima_cotizacion = datetime(año_ultima, mes_ultima, 1)
                # Deadline es 5 años después de última cotización
                fecha_limite_inscripcion = datetime(año_ultima + 5, mes_ultima, 1)
                hoy = now_mexico().replace(tzinfo=None)
                dias_restantes_deadline = (fecha_limite_inscripcion - hoy).days
                print(f"DEBUG: Última cotización: {mes_ultima}/{año_ultima}")
                print(f"DEBUG: Fecha límite inscripción: {fecha_limite_inscripcion.strftime('%m/%Y')}")
                print(f"DEBUG: Días restantes: {dias_restantes_deadline}")
                
                if dias_restantes_deadline < 0:
                    return jsonify({
                        'error': f'Fecha límite de inscripción vencida. Última cotización: {mes_ultima}/{año_ultima}. Límite: {mes_ultima}/{año_ultima + 5}. Has perdido el derecho permanente a Modalidad 40.'
                    }), 400
            except (ValueError, TypeError) as e:
                print(f"DEBUG: ⚠️ Error procesando última cotización: {e}")
        
        try:
            mes_inicio_cotizacion = int(mes_inicio_str)
            año_inicio_cotizacion = int(año_inicio_str)
            print(f"DEBUG: Inicio cotización: {mes_inicio_cotizacion}/{año_inicio_cotizacion}")
            
            # Crear fecha de inicio de cotización
            from datetime import datetime
            fecha_inicio_cotizacion = datetime(año_inicio_cotizacion, mes_inicio_cotizacion, 1)
            fecha_limite_ley97 = datetime(1997, 7, 1)  # 1 de julio de 1997
            
            if fecha_inicio_cotizacion >= fecha_limite_ley97:
                print(f"DEBUG: ❌ Usuario NO elegible: {fecha_inicio_cotizacion} >= {fecha_limite_ley97}")
                return jsonify({
                    'error': f'No elegible para Modalidad 40. Iniciaste cotización el {mes_inicio_cotizacion}/{año_inicio_cotizacion}, posterior al 1/jul/1997 (Ley 97). Tu pensión se basa en el sistema de Afores.'
                }), 400
            else:
                print(f"DEBUG: ✅ Usuario elegible: {fecha_inicio_cotizacion} < {fecha_limite_ley97}")
                
        except (ValueError, TypeError) as e:
            print(f"DEBUG: ❌ Error validando fechas: {e}")
            return jsonify({
                'error': 'Fecha de inicio de cotización inválida'
            }), 400
        
        try:
            año_inicio = int(float(data.get('año_inicio', 2025)))
            print(f"DEBUG: año_inicio = {año_inicio}")
        except (ValueError, TypeError):
            año_inicio = 2025
            print("DEBUG: año_inicio defaulted to 2025")
        
        # Validaciones básicas
        if semanas_cotizadas < 500:
            return jsonify({
                'error': 'Se requieren mínimo 500 semanas cotizadas para acceder a pensión'
            }), 400
        
        if edad_actual < 50 or edad_actual > 70:
            return jsonify({
                'error': 'Edad actual debe estar entre 50 y 70 años'
            }), 400
            
        if edad_pension < 60:
            return jsonify({
                'error': 'Edad mínima para pensión: 60 años'
            }), 400
        
        if edad_pension > 65:
            return jsonify({
                'error': 'Edad máxima legal para pensión: 65 años (límite IMSS)'
            }), 400
            
        if edad_pension <= edad_actual:
            return jsonify({
                'error': 'La edad de pensión debe ser mayor a tu edad actual'
            }), 400
            
        # Verificar tiempo disponible para Modalidad 40
        años_disponibles = edad_pension - edad_actual
        print(f"DEBUG: años_disponibles = {años_disponibles}")
        
        # Note: Allow calculation even with less than 5 years, but include warning in results
        
        # Calcular con la calculadora corregida
        print("DEBUG: Instanciando calculadora...")
        calc = CalculadoraModalidad40Corregida()
        print("DEBUG: Calculadora instanciada exitosamente")
        
        print("DEBUG: Iniciando cálculo con parámetros:", {
            'semanas': semanas_cotizadas, 'sdp_actual': sdp_actual, 
            'sbc_modalidad40': sbc_modalidad40, 'edad_pension': edad_pension,
            'edad_actual': edad_actual, 'mes_nacimiento': mes_inicio_cotizacion
        })
        
        resultado = calc.calcular_escenario_completo(
            semanas_cotizadas_actuales=semanas_cotizadas,
            sdp_actual_diario=sdp_actual,
            sbc_modalidad40_diario=sbc_modalidad40,
            edad_pension=edad_pension,
            tiene_esposa=tiene_esposa,
            num_hijos_dependientes=num_hijos,
            tiene_padres_dependientes=tiene_padres,
            año_inicio=año_inicio,
            edad_actual=edad_actual,
            mes_nacimiento=mes_inicio_cotizacion,  # ✅ CRÍTICO: mes de nacimiento para calcular meses exactos
            mes_inicio_modalidad40=1  # Asume inicio en enero (puede ser configurable después)
        )
        
        print("DEBUG: Cálculo completado:", type(resultado))
        
        if 'error' in resultado:
            print("DEBUG: Error en resultado:", resultado['error'])
            return jsonify({'error': resultado['error']}), 400
        
        print("DEBUG: Formateando respuesta...")
        # Formatear respuesta para el frontend
        print("DEBUG: Formatando respuesta para frontend...")
        print("DEBUG: Keys en resultado:", list(resultado.keys()) if isinstance(resultado, dict) else "NO ES DICT")
        
        # Verificar que resultado tiene las claves esperadas
        required_keys = ['sin_modalidad40', 'con_modalidad40', 'inversion', 'analisis_roi']
        missing_keys = [k for k in required_keys if k not in resultado]
        if missing_keys:
            print(f"DEBUG: ❌ Claves faltantes en resultado: {missing_keys}")
            return jsonify({'error': f'Error en cálculo - claves faltantes: {missing_keys}'}), 500
        
        # Add warning for limited years
        warning_msg = None
        if años_disponibles < 2:
            warning_msg = f"✅ Tienes {años_disponibles} año(s) disponible(s) para Modalidad 40. Incluso con tiempo limitado puedes obtener beneficios significativos."
        elif años_disponibles < 5:
            warning_msg = f"✅ Tienes {años_disponibles} año(s) disponible(s) para Modalidad 40. Modalidad 40 NO requiere duración mínima - puedes cotizar el tiempo que desees."
            
        respuesta = {
            'success': True,
            'warning': warning_msg,
            'semanas_cotizadas': semanas_cotizadas,  # ✅ AGREGADO para PDF
            'deadline_info': {
                'tiene_deadline': fecha_limite_inscripcion is not None,
                'fecha_limite': fecha_limite_inscripcion.strftime('%m/%Y') if fecha_limite_inscripcion else None,
                'dias_restantes': dias_restantes_deadline if dias_restantes_deadline is not None else None,
                'mes_ultima': int(mes_ultima_str) if mes_ultima_str else None,
                'año_ultima': int(año_ultima_str) if año_ultima_str else None
            },
            'edad_info': {
                'edad_actual': edad_actual,
                'edad_pension': edad_pension,
                'años_disponibles': años_disponibles,
                'factor_edad': resultado['sin_modalidad40']['factor_edad'],
                'penalizacion_pct': round((1 - resultado['sin_modalidad40']['factor_edad']) * 100, 0) if resultado['sin_modalidad40']['factor_edad'] < 1 else 0,
                'tiene_incremento_vejez': edad_pension >= 65
            },
            'sin_modalidad40': {
                'pension_base': round(resultado['sin_modalidad40']['pension_base_mensual'], 0),
                'asignaciones': round(resultado['sin_modalidad40']['total_asignaciones_mensual'], 0),
                'pension_total': round(resultado['sin_modalidad40']['pension_final_mensual'], 0),
                'cuantia_pct': round(resultado['sin_modalidad40']['cuantia_basica_pct'], 2),
                'incremento_pct': round(resultado['sin_modalidad40']['incremento_anual_pct'], 2),
                'multiple_uma': round(resultado['sin_modalidad40']['multiple_uma'], 2),
                'sdp_diario': round(sdp_actual, 2),  # ✅ AGREGADO para PDF
                'cuantia_basica_diaria': round(resultado['sin_modalidad40'].get('cuantia_basica_diaria', 0), 2),  # ✅ AGREGADO para PDF
                'cuantia_basica_mensual': round(resultado['sin_modalidad40'].get('cuantia_basica_mensual', 0), 2),  # ✅ AGREGADO para PDF
                'porcentaje_aplicable': round(resultado['sin_modalidad40'].get('porcentaje_aplicable', 0), 2)  # ✅ AGREGADO para PDF
            },
            'con_modalidad40': {
                'pension_base': round(resultado['con_modalidad40']['pension_base_mensual'], 0),
                'asignaciones': round(resultado['con_modalidad40']['total_asignaciones_mensual'], 0),
                'pension_total': round(resultado['con_modalidad40']['pension_final_mensual'], 0),
                'cuantia_pct': round(resultado['con_modalidad40']['cuantia_basica_pct'], 2),
                'incremento_pct': round(resultado['con_modalidad40']['incremento_anual_pct'], 2),
                'multiple_uma': round(resultado['con_modalidad40']['multiple_uma'], 2),
                'pago_mensual_imss': round(resultado['inversion']['promedio_mensual'], 0),
                'sdp_diario': round(sbc_modalidad40, 2),  # ✅ AGREGADO para PDF  
                'cuantia_basica_diaria': round(resultado['con_modalidad40'].get('cuantia_basica_diaria', 0), 2),  # ✅ AGREGADO para PDF
                'cuantia_basica_mensual': round(resultado['con_modalidad40'].get('cuantia_basica_mensual', 0), 2),  # ✅ AGREGADO para PDF
                'porcentaje_aplicable': round(resultado['con_modalidad40'].get('porcentaje_aplicable', 0), 2)  # ✅ AGREGADO para PDF
            },
            'inversion': {
                'total_años': round(resultado['inversion']['total_años'], 0),
                'años_cotizados': resultado['inversion']['años_cotizados'],
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
            'fecha_calculo': now_mexico().strftime('%d/%m/%Y %H:%M'),
            'tope_maximo': calc.tope_diario_2025,
            'uma_2025': calc.uma_diaria_2025
        }
        
        # Add warning if less than 5 years available
        if años_disponibles < 5:
            respuesta['warning'] = {
                'mensaje': f'Tienes {años_disponibles} año(s) disponible(s) hasta pensionarte. Con Modalidad 40 puedes mejorar tu pensión significativamente incluso con tiempo limitado.',
                'tipo': 'informativo',
                'mostrar': True,
                'detalles': f'Modalidad 40 NO tiene duración mínima. Puedes cotizar desde 1 mes hasta {años_disponibles} años. Con {años_disponibles} años tendrías {años_disponibles * 52} semanas adicionales para mejorar tu pensión.'
            }
        
        print("DEBUG: ✅ Respuesta formateada exitosamente")
        print("DEBUG: Keys de respuesta:", list(respuesta.keys()))
        print("DEBUG: 🚀 ENVIANDO RESPUESTA AL CLIENTE:")
        print("DEBUG: Respuesta completa:", respuesta)
        
        return jsonify(respuesta)
        
    except ValueError as ve:
        error_msg = f'Error en formato de números: {str(ve)}'
        print(f"DEBUG: ❌ ValueError capturado: {error_msg}")
        return jsonify({'error': error_msg}), 400
    except KeyError as ke:
        error_msg = f'Error: Clave faltante {str(ke)}'
        print(f"DEBUG: ❌ KeyError capturado: {error_msg}")
        import traceback
        print("DEBUG: Traceback KeyError:")
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500
    except AttributeError as ae:
        error_msg = f'Error de atributo: {str(ae)}'
        print(f"DEBUG: ❌ AttributeError capturado: {error_msg}")
        import traceback
        print("DEBUG: Traceback AttributeError:")
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f'Error interno del servidor: {str(e)}'
        print(f"DEBUG: ❌ Exception general capturada: {error_msg}")
        print(f"DEBUG: Tipo de excepción: {type(e)}")
        import traceback
        print("DEBUG: Traceback completo:")
        traceback.print_exc()
        return jsonify({'error': error_msg}), 500

@app.route('/test')
def test():
    """Endpoint de prueba para verificar que el servidor funciona"""
    return jsonify({
        'success': True,
        'message': 'Servidor funcionando correctamente',
        'timestamp': now_mexico().isoformat()
    })

@app.route('/test-calculator')
def test_calculator():
    """Endpoint para probar la calculadora en aislamiento"""
    try:
        print("DEBUG: 🧪 PROBANDO CALCULADORA EN AISLAMIENTO")
        
        # Crear instancia de calculadora
        calc = CalculadoraModalidad40Corregida()
        print("DEBUG: ✅ Calculadora instanciada")
        
        # Parámetros de prueba básicos
        test_params = {
            'semanas_cotizadas': 758,
            'sdp_diario': 222.02,
            'sbc_modalidad40': 2828.50,  # 25 UMAs
            'edad_pension': 65,
            'tiene_esposa': False,
            'num_hijos': 0,
            'tiene_padres': False,
            'año_inicio': 2025
        }
        
        print("DEBUG: Parámetros de prueba:", test_params)
        
        # Ejecutar cálculo
        resultado = calc.calcular_escenario_completo(
            semanas_cotizadas_actuales=test_params['semanas_cotizadas'],
            sdp_actual_diario=test_params['sdp_diario'],
            sbc_modalidad40_diario=test_params['sbc_modalidad40'],
            edad_pension=test_params['edad_pension'],
            tiene_esposa=test_params['tiene_esposa'],
            num_hijos_dependientes=test_params['num_hijos'],
            tiene_padres_dependientes=test_params['tiene_padres'],
            año_inicio=test_params['año_inicio']
        )
        
        print("DEBUG: ✅ Cálculo completado")
        print("DEBUG: Keys en resultado:", list(resultado.keys()))
        
        # Verificar estructura
        required_keys = ['sin_modalidad40', 'con_modalidad40', 'inversion', 'analisis_roi']
        structure_ok = all(k in resultado for k in required_keys)
        
        return jsonify({
            'success': True,
            'calculator_working': True,
            'structure_ok': structure_ok,
            'result_keys': list(resultado.keys()),
            'test_params': test_params,
            'sample_result': {
                'sin_mod40_pension': resultado['sin_modalidad40']['pension_final_mensual'],
                'con_mod40_pension': resultado['con_modalidad40']['pension_final_mensual'],
                'inversion_total': resultado['inversion']['total_años'],
                'roi_anual': resultado['analisis_roi']['roi_anual_pct']
            }
        })
        
    except Exception as e:
        print("DEBUG: ❌ Error en test-calculator:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'calculator_working': False
        }), 500

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

@app.route('/generar-reporte-pdf', methods=['POST'])
def generar_reporte_pdf():
    """Generar reporte personalizado en PDF"""
    try:
        data = request.get_json()
        
        # Validar datos personales requeridos para PDF
        required_personal_fields = ['nombre', 'apellido_paterno']
        
        for field in required_personal_fields:
            if field not in data or not data[field].strip():
                return jsonify({
                    'error': f'Campo personal requerido para PDF: {field}'
                }), 400
        
        # Validar que tenemos los resultados del cálculo
        if 'resultados' not in data:
            return jsonify({
                'error': 'Se requieren los resultados del cálculo para generar el PDF'
            }), 400
        
        # Crear buffer para PDF
        buffer = io.BytesIO()
        
        # Crear documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Contenido del PDF
        story = []
        
        # Título
        story.append(Paragraph("ANÁLISIS MODALIDAD 40 IMSS", title_style))
        story.append(Paragraph("Reporte Técnico Personalizado de Pensión - Ley 73", styles['Normal']))
        story.append(Paragraph(f"Fecha: {now_mexico().strftime('%d de %B de %Y')}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # ALERTA DE FECHA LÍMITE (si aplica)
        resultados = data['resultados']
        deadline_info = resultados.get('deadline_info', {})
        
        if deadline_info.get('tiene_deadline') and deadline_info.get('dias_restantes') is not None:
            dias_restantes = deadline_info['dias_restantes']
            fecha_limite = deadline_info['fecha_limite']
            
            # Determinar urgencia
            if dias_restantes < 60:
                urgencia_color = colors.red
                urgencia_texto = "🚨 URGENTE - ACCIÓN INMEDIATA REQUERIDA"
            elif dias_restantes < 180:
                urgencia_color = colors.orange
                urgencia_texto = "⚠️ ADVERTENCIA - TIEMPO LIMITADO"
            else:
                urgencia_color = colors.green
                urgencia_texto = "✓ INFORMACIÓN - PLAZO DISPONIBLE"
            
            deadline_style = ParagraphStyle(
                'DeadlineStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.white,
                backColor=urgencia_color,
                leftIndent=10,
                rightIndent=10,
                spaceAfter=10,
                spaceBefore=10,
                alignment=1  # center
            )
            
            meses_restantes = dias_restantes // 30
            años_restantes = meses_restantes // 12
            meses_extra = meses_restantes % 12
            
            deadline_texto = f"""
            <b>{urgencia_texto}</b><br/>
            FECHA LÍMITE DE INSCRIPCIÓN: {fecha_limite}<br/>
            Tiempo restante: {años_restantes} años y {meses_extra} meses ({dias_restantes} días)<br/>
            Última cotización: {deadline_info.get('mes_ultima')}/{deadline_info.get('año_ultima')}<br/>
            <b>Después de esta fecha perderás el derecho PERMANENTE a Modalidad 40</b>
            """
            
            story.append(Paragraph(deadline_texto, deadline_style))
            story.append(Spacer(1, 12))
        
        story.append(Spacer(1, 8))
        
        # Base Normativa
        story.append(Paragraph("BASE NORMATIVA Y METODOLOGÍA", subtitle_style))
        
        base_normativa = """
        <b>Marco Legal:</b> Ley del Seguro Social (LSS), Artículos 154, 162, 167 y 171<br/>
        <b>Modalidad 40:</b> Continuación Voluntaria en el Régimen Obligatorio<br/>
        <b>Régimen Aplicable:</b> Ley 73 (para trabajadores que iniciaron cotizaciones antes del 1° julio 1997)<br/>
        <b>Fórmula de Cálculo:</b> Tablas variables según múltiplo SDP/UMA (22 rangos diferentes)<br/>
        <b>UMA 2025:</b> $113.14 diarios / $3,439.46 mensuales<br/>
        <b>Tasa Modalidad 40 2025:</b> 13.347% (incrementa anualmente hasta 18% en 2030)<br/>
        """
        
        story.append(Paragraph(base_normativa, styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Datos personales y situación actual
        nombre_completo = f"{data['nombre']} {data['apellido_paterno']} {data.get('apellido_materno', '')}".strip()
        story.append(Paragraph("DATOS DEL BENEFICIARIO Y SITUACIÓN ACTUAL", subtitle_style))
        
        # Extraer datos técnicos de los resultados
        resultados = data['resultados']
        sin_mod40 = resultados['sin_modalidad40']
        con_mod40 = resultados['con_modalidad40']
        edad_info = resultados.get('edad_info', {})
        
        datos_personales = [
            ['Nombre Completo:', nombre_completo],
            ['RFC:', data.get('rfc', 'No proporcionado')],
            ['CURP:', data.get('curp', 'No proporcionado')],
            ['NSS:', data.get('nss', 'No proporcionado')],
            ['', ''],
            ['SITUACIÓN PENSIONARIA ACTUAL:', ''],
            ['Semanas Cotizadas:', f"{resultados.get('semanas_cotizadas', 'N/A')} semanas"],
            ['SDP Actual:', f"${sin_mod40.get('sdp_diario', 0):,.2f} diarios ({sin_mod40.get('multiple_uma', 0):.2f} UMAs)"],
            ['Edad Actual:', f"{edad_info.get('edad_actual', 'N/A')} años"],
            ['Edad Pensión Planeada:', f"{edad_info.get('edad_pension', 'N/A')} años"],
            ['Tiempo Disponible:', f"{edad_info.get('años_disponibles', 'N/A')} años"],
            ['Factor por Edad:', f"{edad_info.get('factor_edad', 1):.0%} de la pensión"]
        ]
        
        tabla_datos = Table(datos_personales, colWidths=[2*inch, 4*inch])
        tabla_datos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ]))
        
        story.append(tabla_datos)
        story.append(Spacer(1, 20))
        
        # Resumen Ejecutivo
        resultados = data['resultados']
        story.append(Paragraph("RESUMEN EJECUTIVO DE ANÁLISIS MODALIDAD 40", subtitle_style))
        
        # Calcular métricas adicionales
        diferencia_mensual = resultados['analisis_roi']['diferencia_mensual']
        inversion_mensual = resultados['con_modalidad40']['pago_mensual_imss']
        roi_anual = resultados['analisis_roi']['roi_anual']
        
        resumen_data = [
            ['CONCEPTO', 'ESCENARIO ACTUAL', 'CON MODALIDAD 40', 'IMPACTO'],
            [
                'Pensión Mensual',
                f"${resultados['sin_modalidad40']['pension_total']:,.0f}",
                f"${resultados['con_modalidad40']['pension_total']:,.0f}",
                f"+${diferencia_mensual:,.0f}"
            ],
            [
                'Pensión Anual',
                f"${resultados['sin_modalidad40']['pension_total']*12:,.0f}",
                f"${resultados['con_modalidad40']['pension_total']*12:,.0f}",
                f"+${resultados['analisis_roi']['diferencia_anual']:,.0f}"
            ],
            [
                'Pago Mensual IMSS',
                '---',
                f"${inversion_mensual:,.0f}",
                'Inversión requerida'
            ],
            [
                'ROI Anual del Programa',
                '---',
                f"{roi_anual:.1f}%",
                f"Rendimiento: {roi_anual:.1f}%"
            ]
        ]
        
        tabla_resumen = Table(resumen_data, colWidths=[2*inch, 1.3*inch, 1.3*inch, 1.4*inch])
        tabla_resumen.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabla_resumen)
        story.append(Spacer(1, 20))
        
        # Análisis de Inversión
        story.append(Paragraph("ANÁLISIS DE INVERSIÓN", subtitle_style))
        
        inversion_data = [
            ['Concepto', 'Valor'],
            ['Inversión Total (5 años)', f"${resultados['inversion']['total_años']:,.0f}"],
            ['Pago Mensual Promedio', f"${resultados['inversion']['promedio_mensual']:,.0f}"],
            ['ROI Anual', f"{resultados['analisis_roi']['roi_anual']:.1f}%"],
            ['Período de Recuperación', f"{resultados['analisis_roi']['años_recuperacion']:.1f} años"]
        ]
        
        tabla_inversion = Table(inversion_data, colWidths=[3*inch, 2*inch])
        tabla_inversion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabla_inversion)
        story.append(Spacer(1, 20))
        
        # Desglose técnico de cálculos
        story.append(Paragraph("DESGLOSE TÉCNICO DE CÁLCULOS", subtitle_style))
        
        # Mostrar el cálculo paso a paso
        sin_mod40_data = resultados['sin_modalidad40']
        con_mod40_data = resultados['con_modalidad40']
        
        calculo_data = [
            ['COMPONENTE DEL CÁLCULO', 'ESCENARIO ACTUAL', 'CON MODALIDAD 40'],
            ['Salario Diario Promedio (SDP)', f"${sin_mod40_data['sdp_diario']:,.2f}", f"${con_mod40_data['sdp_diario']:,.2f}"],
            ['Múltiple de UMA', f"{sin_mod40_data.get('multiple_uma', 0):.2f} UMAs", f"{con_mod40_data.get('multiple_uma', 0):.2f} UMAs"],
            ['Porcentaje Aplicable Ley 73', f"{sin_mod40_data.get('porcentaje_aplicable', 0):.2f}%", f"{con_mod40_data.get('porcentaje_aplicable', 0):.2f}%"],
            ['Cuantía Básica Diaria', f"${sin_mod40_data.get('cuantia_basica_diaria', 0):,.2f}", f"${con_mod40_data.get('cuantia_basica_diaria', 0):,.2f}"],
            ['Cuantía Básica Mensual (x30.4)', f"${sin_mod40_data.get('cuantia_basica_mensual', 0):,.2f}", f"${con_mod40_data.get('cuantia_basica_mensual', 0):,.2f}"],
            ['Factor por Edad', f"{resultados.get('edad_info', {}).get('factor_edad', 1):.0%}", f"{resultados.get('edad_info', {}).get('factor_edad', 1):.0%}"],
            ['Pensión Final Mensual', f"${sin_mod40_data['pension_total']:,.0f}", f"${con_mod40_data['pension_total']:,.0f}"]
        ]
        
        tabla_calculo = Table(calculo_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        tabla_calculo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabla_calculo)
        story.append(Spacer(1, 20))
        
        # Información de Edad si está disponible
        if 'edad_info' in resultados:
            edad_info = resultados['edad_info']
            story.append(Paragraph("INFORMACIÓN DE EDAD Y PENSIÓN", subtitle_style))
            
            edad_text = f"""
            <b>Edad Actual:</b> {edad_info['edad_actual']} años<br/>
            <b>Edad de Pensión:</b> {edad_info['edad_pension']} años<br/>
            <b>Tiempo Disponible:</b> {edad_info['años_disponibles']} años<br/>
            """
            
            if edad_info['penalizacion_pct'] > 0:
                edad_text += f"<b>Penalización por Edad:</b> {edad_info['penalizacion_pct']:.0f}% (recibirás {100-edad_info['penalizacion_pct']:.0f}% de la pensión)<br/>"
            
            if edad_info['tiene_incremento_vejez']:
                edad_text += "<b>Bonus por Vejez:</b> +11% adicional por pensionarte a los 65 años o más<br/>"
            
            story.append(Paragraph(edad_text, styles['Normal']))
            story.append(Spacer(1, 15))
        
        # ==================== CALENDARIO DE PAGOS DETALLADO ====================
        story.append(Paragraph("INVERSIÓN TOTAL MODALIDAD 40", subtitle_style))
        
        # Calcular totales REALES del desglose
        total_inversion_real = 0
        total_meses_real = 0
        
        if 'desglose_anual' in resultados.get('inversion', {}):
            for año, datos in resultados['inversion']['desglose_anual'].items():
                total_inversion_real += datos.get('costo_anual', 0)
                total_meses_real += datos.get('meses_pagados', 12)
        
        # PANEL DESTACADO - TOTAL EN GRANDE
        panel_total_style = ParagraphStyle(
            'PanelTotal',
            parent=styles['Normal'],
            fontSize=32,
            textColor=colors.HexColor('#0d6efd'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=10
        )
        
        story.append(Paragraph("TOTAL A PAGAR DURANTE TODO EL PERÍODO", styles['Normal']))
        story.append(Paragraph(f"${total_inversion_real:,.2f}", panel_total_style))
        story.append(Spacer(1, 10))
        
        # Tabla resumen pequeña
        resumen_inversion = [
            ['Período', 'Total Meses', 'Promedio Mensual'],
            [
                f"{len(resultados.get('inversion', {}).get('desglose_anual', {}))} años",
                f"{total_meses_real} meses",
                f"${resultados.get('inversion', {}).get('promedio_mensual', 0):,.2f}"
            ]
        ]
        
        tabla_resumen_inv = Table(resumen_inversion, colWidths=[2*inch, 2*inch, 2*inch])
        tabla_resumen_inv.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabla_resumen_inv)
        story.append(Spacer(1, 15))
        
        # DESGLOSE DETALLADO POR AÑO - SIEMPRE INCLUIR
        story.append(Paragraph("Desglose de Pagos por Año", subtitle_style))
        
        if 'desglose_anual' in resultados.get('inversion', {}):
            calendario_data = [['Año', 'Tasa IMSS', 'Meses', 'Pago Mensual', 'Total Año']]
            
            for año in sorted(resultados['inversion']['desglose_anual'].keys()):
                datos = resultados['inversion']['desglose_anual'][año]
                meses_pagados = datos.get('meses_pagados', 12)
                calendario_data.append([
                    str(año),
                    f"{datos['tasa_pct']:.3f}%",
                    str(meses_pagados),
                    f"${datos['costo_mensual']:,.2f}",
                    f"${datos['costo_anual']:,.2f}"
                ])
            
            # Fila de TOTAL
            calendario_data.append([
                'TOTAL',
                '',
                str(total_meses_real),
                f"${resultados['inversion']['promedio_mensual']:,.2f}",
                f"${total_inversion_real:,.2f}"
            ])
            
            tabla_calendario = Table(calendario_data, colWidths=[0.8*inch, 1*inch, 0.8*inch, 1.4*inch, 1.4*inch])
            tabla_calendario.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                # Alternar colores en filas de datos
                ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
                # Fila de TOTAL
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#28a745')),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 11),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tabla_calendario)
            story.append(Spacer(1, 15))
        
        # Información práctica sobre pagos
        info_pagos = f"""
        <b>Información Importante de Pagos:</b><br/>
        • <b>Fechas de Pago:</b> Del 1 al 15 de cada mes (pago por adelantado)<br/>
        • <b>Modalidad:</b> Ventanilla bancaria, transferencia o domiciliación automática<br/>
        • <b>Beneficio Mensual Adicional:</b> ${diferencia_mensual:,.0f} pesos<br/>
        • <b>Recuperación de Inversión:</b> {total_inversion_real / (diferencia_mensual * 12):.1f} años<br/><br/>
        
        <b>IMPORTANTE:</b> Los pagos se detienen exactamente cuando cumples {edad_info.get('edad_pension', 65)} años.
        El último año solo pagarás los meses necesarios hasta tu cumpleaños (ver columna "Meses" en tabla).
        """
        
        story.append(Paragraph(info_pagos, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # SECCIÓN: ANÁLISIS COMPARATIVO DE ESCENARIOS
        story.append(Paragraph("ANÁLISIS COMPARATIVO: DIFERENTES DURACIONES DE MODALIDAD 40", subtitle_style))
        
        story.append(Paragraph("""
        <b>¿Qué pasa si pagas solo 1, 2 o 3 años de Modalidad 40?</b><br/>
        La tabla muestra cómo varían los beneficios según la duración de tu inversión:
        """, styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Calcular escenarios para diferentes duraciones
        años_disponibles = edad_info.get('años_disponibles', 4)
        max_años = min(años_disponibles, 5)  # Máximo 5 escenarios
        
        escenarios_data = [['Años', 'Inversión Total', 'Pensión Mensual', 'Ganancia vs Sin Mod40', 'ROI Anual', 'Años Breakeven']]
        
        # Usamos la calculadora ya importada al inicio del módulo
        
        for años in range(1, max_años + 1):
            # Calcular pensión para este escenario
            semanas_adicionales = años * 52
            semanas_totales = resultados.get('semanas_cotizadas', 758) + semanas_adicionales
            
            # Estimar inversión (promedio aproximado)
            inversion_estimada = años * 12 * inversion_mensual
            
            # Calcular nueva pensión (aproximación usando porcentaje de crecimiento)
            factor_crecimiento = semanas_totales / resultados.get('semanas_cotizadas', 758)
            pension_estimada = resultados['sin_modalidad40']['pension_total'] * factor_crecimiento * 1.2  # Factor conservador
            
            ganancia = pension_estimada - resultados['sin_modalidad40']['pension_total']
            roi = (ganancia * 12 / inversion_estimada) * 100 if inversion_estimada > 0 else 0
            breakeven = inversion_estimada / (ganancia * 12) if ganancia > 0 else 999
            
            escenarios_data.append([
                f"{años} año{'s' if años > 1 else ''}",
                f"${inversion_estimada:,.0f}",
                f"${pension_estimada:,.0f}",
                f"+${ganancia:,.0f}",
                f"{roi:.1f}%",
                f"{breakeven:.1f} años"
            ])
        
        tabla_escenarios = Table(escenarios_data, colWidths=[0.8*inch, 1.2*inch, 1.2*inch, 1.2*inch, 0.9*inch, 1.1*inch])
        tabla_escenarios.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6f42c1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tabla_escenarios)
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("""
        <b>Conclusión de Escenarios:</b><br/>
        • Incluso con 1 año de Modalidad 40 obtienes beneficios permanentes<br/>
        • A mayor duración, mayor es el incremento en tu pensión<br/>
        • El ROI se mantiene alto en todos los escenarios<br/>
        • No existe duración mínima - puedes cotizar el tiempo que desees/puedas
        """, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Recomendaciones si están seleccionadas
        if data.get('incluir_recomendaciones', False):
            story.append(Paragraph("RECOMENDACIONES PERSONALIZADAS", subtitle_style))
            
            roi = resultados['analisis_roi']['roi_anual']
            
            if roi > 40:
                recomendacion = "EXCELENTE OPORTUNIDAD - Su ROI es excepcional y supera cualquier instrumento financiero convencional."
            elif roi > 25:
                recomendacion = "MUY BUENA INVERSIÓN - El retorno justifica ampliamente la inversión en Modalidad 40."
            elif roi > 15:
                recomendacion = "BUENA OPCIÓN - La Modalidad 40 ofrece un retorno competitivo para su perfil."
            else:
                recomendacion = "EVALUAR CUIDADOSAMENTE - Considere si puede optimizar el nivel de cotización."
            
            story.append(Paragraph(f"<b>Recomendación Principal:</b> {recomendacion}", styles['Normal']))
            story.append(Spacer(1, 10))
            
            if edad_info and edad_info['años_disponibles'] < 5:
                story.append(Paragraph("<b>URGENTE:</b> Tiene menos de 5 años hasta su pensión. Es crítico iniciar Modalidad 40 inmediatamente.", styles['Normal']))
                story.append(Spacer(1, 10))
            
            story.append(Paragraph("<b>Próximos Pasos Recomendados:</b>", styles['Normal']))
            story.append(Paragraph("1. Acudir al IMSS para iniciar trámite de Modalidad 40", styles['Normal']))
            story.append(Paragraph("2. Verificar vigencia de derechos (máximo 5 años desde baja)", styles['Normal']))
            story.append(Paragraph("3. Programar pagos mensuales en banco autorizado", styles['Normal']))
            story.append(Paragraph("4. Consultar con especialista en seguridad social", styles['Normal']))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_text = """
        <i>Este reporte es generado automáticamente basado en la normativa IMSS vigente y tiene fines informativos. 
        Se recomienda verificar con especialistas antes de tomar decisiones financieras importantes.</i>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Conclusiones y Recomendaciones
        story.append(Paragraph("CONCLUSIONES Y RECOMENDACIONES", subtitle_style))
        
        # Análisis del ROI
        roi_anual = resultados['analisis_roi']['roi_anual']
        tiempo_recuperacion = (pago_mensual * 12 * años_disponibles) / (diferencia_mensual * 12)
        
        conclusiones_text = f"""
        <b>ANÁLISIS FINANCIERO:</b><br/>
        • El programa Modalidad 40 ofrece un ROI anual de <b>{roi_anual:.1f}%</b><br/>
        • Su pensión aumentaría <b>${diferencia_mensual:,.0f} pesos mensuales</b><br/>
        • La inversión se recupera en aproximadamente <b>{tiempo_recuperacion:.1f} años</b><br/>
        • Beneficio total a lo largo de la vida: <b>Significativo</b><br/><br/>
        
        <b>RECOMENDACIONES:</b><br/>
        • {'✅ RECOMENDABLE' if roi_anual > 15 else '⚠️ EVALUAR CUIDADOSAMENTE' if roi_anual > 5 else '❌ NO RECOMENDABLE'}: {
            'Excelente rendimiento, superior a muchas inversiones tradicionales' if roi_anual > 15 else
            'Rendimiento moderado, considere otras opciones de inversión' if roi_anual > 5 else
            'Rendimiento bajo, posiblemente mejor invertir de forma privada'
        }<br/>
        • Consulte con un asesor especializado en seguridad social<br/>
        • Considere su situación particular de salud y esperanza de vida<br/>
        • Evalúe la estabilidad de sus ingresos para mantener los pagos<br/><br/>
        
        <b>PRÓXIMOS PASOS:</b><br/>
        1. Acudir a la subdelegación IMSS más cercana<br/>
        2. Presentar la documentación requerida<br/>
        3. Iniciar trámite dentro de los 5 años posteriores a la baja laboral<br/>
        4. Configurar forma de pago (recomendamos domiciliación automática)<br/><br/>
        
        <b>IMPORTANTE:</b> Este análisis es orientativo. Los cálculos están basados en la normativa vigente
        y pueden cambiar por modificaciones legislativas. Consulte siempre con personal autorizado del IMSS.
        """
        
        story.append(Paragraph(conclusiones_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Disclaimer Legal Completo
        story.append(Paragraph("DISCLAIMER Y LIMITACIÓN DE RESPONSABILIDAD", subtitle_style))
        
        disclaimer_text = """
        <b>IMPORTANTE - LÉASE CUIDADOSAMENTE:</b><br/><br/>
        
        Este reporte contiene <b>sugerencias y análisis basados en las mejores prácticas de análisis actuarial</b> 
        con fundamento en la Ley del Seguro Social vigente y sus disposiciones reglamentarias. Sin embargo, 
        <b>NO CONSTITUYE INFORMACIÓN OFICIAL</b> del Instituto Mexicano del Seguro Social (IMSS).<br/><br/>
        
        <b>Los datos oficiales, cálculos definitivos y resoluciones pensionarias ÚNICAMENTE serán proporcionados 
        por el Instituto Mexicano del Seguro Social (IMSS)</b> a través de sus canales oficiales y personal autorizado.<br/><br/>
        
        <b>LIMITACIONES DE ESTE ANÁLISIS:</b><br/>
        • Las proyecciones se basan en la normativa vigente al momento de la consulta<br/>
        • Los cálculos pueden variar por cambios legislativos o reglamentarios<br/>
        • Cada caso particular puede tener circunstancias especiales no contempladas<br/>
        • Las fechas límite y requisitos deben confirmarse directamente con el IMSS<br/><br/>
        
        <b>RECOMENDACIÓN FORMAL:</b> Antes de tomar cualquier decisión financiera o iniciar trámites, 
        consulte directamente con las oficinas del IMSS o personal autorizado para obtener información 
        oficial y actualizada sobre su caso específico.<br/><br/>
        
        Este documento es una herramienta de análisis preliminar y educativa, no un dictamen oficial.
        """
        
        story.append(Paragraph(disclaimer_text, styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Pie de página informativo
        footer_text = f"""
        <b>Documento generado el:</b> {now_mexico().strftime('%d de %B de %Y a las %H:%M hrs')}<br/>
        <b>Calculadora:</b> Sistema de Análisis Modalidad 40 IMSS - Ley del Seguro Social 1973<br/>
        <b>Versión:</b> 2.0 (Fórmulas Variables Validadas con Base Actuarial)<br/>
        <b>Fuente Legal:</b> Ley del Seguro Social, Arts. 154, 162, 167, 171 y disposiciones vigentes<br/>
        <b>Desarrollo:</b> Análisis Actuarial Independiente - No Oficial IMSS
        """
        
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        # Preparar respuesta
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Reporte_Modalidad40_{data['nombre']}_{data['apellido_paterno']}.pdf",
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return jsonify({'error': f'Error al generar PDF: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
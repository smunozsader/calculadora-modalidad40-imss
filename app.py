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
from datetime import datetime
import sys
import os
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

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
            'semanas_cotizadas', 'sdp_actual', 'sbc_modalidad40', 'edad_actual', 'edad_pension'
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
        edad_actual = int(data['edad_actual'])
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
        
        if edad_actual < 50 or edad_actual > 70:
            return jsonify({
                'error': 'Edad actual debe estar entre 50 y 70 años'
            }), 400
            
        if edad_pension < 60:
            return jsonify({
                'error': 'Edad mínima para pensión: 60 años'
            }), 400
            
        if edad_pension <= edad_actual:
            return jsonify({
                'error': 'La edad de pensión debe ser mayor a tu edad actual'
            }), 400
            
        # Verificar tiempo disponible para Modalidad 40
        años_disponibles = edad_pension - edad_actual
        if años_disponibles < 5:
            return jsonify({
                'warning': f'Solo tienes {años_disponibles} años hasta pensionarte. Modalidad 40 requiere 5 años completos.',
                'continuar': True
            })
        
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

@app.route('/generar-reporte-pdf', methods=['POST'])
def generar_reporte_pdf():
    """Generar reporte personalizado en PDF"""
    try:
        data = request.get_json()
        
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
        story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d de %B de %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
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
            ['Inversión Total (5 años)', f"${resultados['inversion']['total_5_años']:,.0f}"],
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
        
        # Calendario de Pagos y Proyección Financiera
        story.append(Paragraph("CALENDARIO DE PAGOS Y PROYECCIÓN FINANCIERA", subtitle_style))
        
        # Agregar información práctica sobre pagos
        pago_mensual = con_mod40_data['pago_mensual_imss']
        años_disponibles = resultados.get('edad_info', {}).get('años_disponibles', 1)
        
        info_pagos = f"""
        <b>Información de Pagos IMSS:</b><br/>
        • Pago Mensual a IMSS: ${pago_mensual:,.0f} pesos<br/>
        • Pago Anual: ${pago_mensual * 12:,.0f} pesos<br/>
        • Inversión Total Estimada: ${pago_mensual * 12 * años_disponibles:,.0f} pesos<br/>
        • Beneficio Mensual Adicional: ${diferencia_mensual:,.0f} pesos<br/>
        • Recuperación de Inversión: {(pago_mensual * 12 * años_disponibles) / (diferencia_mensual * 12):.1f} años<br/><br/>
        
        <b>Fechas de Pago:</b> Del 1 al 15 de cada mes (pago por adelantado)<br/>
        <b>Modalidad:</b> Ventanilla bancaria, transferencia o domiciliación automática
        """
        
        story.append(Paragraph(info_pagos, styles['Normal']))
        story.append(Spacer(1, 15))
        
        # Tabla de proyección anual si hay datos disponibles
        if data.get('incluir_calendario', False) and 'desglose_anual' in resultados.get('inversion', {}):
            calendario_data = [['Año', 'Tasa IMSS', 'Pago Mensual', 'Total Anual']]
            
            for año, datos in resultados['inversion']['desglose_anual'].items():
                calendario_data.append([
                    año,
                    f"{datos['tasa_pct']:.3f}%",
                    f"${datos['costo_mensual']:,.0f}",
                    f"${datos['costo_anual']:,.0f}"
                ])
            
            tabla_calendario = Table(calendario_data, colWidths=[1*inch, 1.2*inch, 1.5*inch, 1.5*inch])
            tabla_calendario.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.orange),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('ALTERNATEROWCOLORS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(tabla_calendario)
            story.append(Spacer(1, 15))
        
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
        <b>Documento generado el:</b> {datetime.now().strftime('%d de %B de %Y a las %H:%M hrs')}<br/>
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
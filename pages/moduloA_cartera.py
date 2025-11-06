import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calcular_tasa_periodo(tea, frecuencia):
    """
    Convierte la TEA a tasa por periodo según la frecuencia de aportes.
    
    Parámetros:
    -----------
    tea : float
        Tasa Efectiva Anual (en decimal, ej: 0.08 para 8%)
    frecuencia : str
        "Mensual", "Trimestral", "Semestral", "Anual"
    
    Retorna:
    --------
    tasa_periodo : float
        Tasa equivalente por periodo
    periodos_por_año : int
        Número de periodos en un año
    """
    frecuencias = {
        "Mensual": 12,
        "Trimestral": 4,
        "Semestral": 2,
        "Anual": 1
    }
    
    periodos_por_año = frecuencias[frecuencia]
    
    # Fórmula de tasa equivalente: (1 + TEA)^(1/n) - 1
    tasa_periodo = (1 + tea) ** (1 / periodos_por_año) - 1
    
    return tasa_periodo, periodos_por_año


def simular_crecimiento_cartera(monto_inicial, aporte_periodico, frecuencia, tea, edad_actual, edad_jubilacion):
    """
    Simula el crecimiento de una cartera con interés compuesto.
    
    Parámetros:
    -----------
    monto_inicial : float
        Depósito inicial en USD
    aporte_periodico : float
        Aporte regular en USD (0 si no hay aportes)
    frecuencia : str
        "Mensual", "Trimestral", "Semestral", "Anual"
    tea : float
        Tasa Efectiva Anual en porcentaje (ej: 8 para 8%)
    edad_actual : int
        Edad actual del usuario
    edad_jubilacion : int
        Edad planeada de jubilación
    
    Retorna:
    --------
    df_resultados : pandas.DataFrame
        Tabla detallada periodo por periodo
    saldo_final : float
        Capital acumulado al final del plazo
    total_aportado : float
        Total de dinero aportado (inicial + aportes)
    interes_total_ganado : float
        Total de intereses generados
    """
    
    # Validaciones básicas
    if edad_jubilacion <= edad_actual:
        raise ValueError("La edad de jubilación debe ser mayor a la edad actual")
    if tea < 0 or tea > 50:
        raise ValueError("La TEA debe estar entre 0% y 50%")
    if monto_inicial < 0 or aporte_periodico < 0:
        raise ValueError("Los montos no pueden ser negativos")
    
    # Cálculos iniciales
    plazo_años = edad_jubilacion - edad_actual
    tea_decimal = tea / 100  # Convertir porcentaje a decimal
    tasa_periodo, periodos_por_año = calcular_tasa_periodo(tea_decimal, frecuencia)
    total_periodos = plazo_años * periodos_por_año
    
    # Inicializar listas para almacenar resultados
    periodos = []
    saldos_iniciales = []
    aportes = []
    intereses = []
    saldos_finales = []
    
    # Simulación periodo por periodo
    saldo = monto_inicial
    
    for periodo in range(total_periodos + 1):
        # Registrar estado inicial del periodo
        periodos.append(periodo)
        saldos_iniciales.append(saldo)
        
        if periodo == 0:
            # En el periodo 0 solo tenemos el monto inicial
            aportes.append(monto_inicial)
            intereses.append(0.0)
            saldos_finales.append(monto_inicial)
        else:
            # Agregar aporte periódico
            saldo_con_aporte = saldo + aporte_periodico
            
            # Calcular interés sobre el saldo (incluye el aporte)
            interes_periodo = saldo_con_aporte * tasa_periodo
            
            # Nuevo saldo al final del periodo
            saldo = saldo_con_aporte + interes_periodo
            
            # Registrar valores
            aportes.append(aporte_periodico)
            intereses.append(interes_periodo)
            saldos_finales.append(saldo)
    
    # Crear DataFrame con resultados
    df_resultados = pd.DataFrame({
        'Periodo': periodos,
        'Saldo Inicial (USD)': saldos_iniciales,
        'Aporte (USD)': aportes,
        'Interés Ganado (USD)': intereses,
        'Saldo Final (USD)': saldos_finales
    })
    
    # Redondear a 2 decimales
    df_resultados = df_resultados.round(2)
    
    # Calcular métricas finales
    saldo_final = saldos_finales[-1]
    total_aportado = monto_inicial + (aporte_periodico * total_periodos)
    interes_total_ganado = saldo_final - total_aportado
    
    return df_resultados, saldo_final, total_aportado, interes_total_ganado


def graficar_crecimiento(df_resultados):
    """
    Genera gráfica de crecimiento de la cartera usando matplotlib.
    
    Parámetros:
    -----------
    df_resultados : pandas.DataFrame
        Tabla con los resultados periodo por periodo
    
    Retorna:
    --------
    fig : matplotlib.figure.Figure
        Figura de matplotlib para mostrar en Streamlit
    """
    # Calcular aportes acumulados por periodo
    aportes_acumulados = df_resultados['Aporte (USD)'].cumsum()
    
    # Crear la gráfica
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df_resultados['Periodo'], df_resultados['Saldo Final (USD)'], 
            label='Saldo Total', linewidth=2.5, color='#2E86AB')
    ax.plot(df_resultados['Periodo'], aportes_acumulados, 
            label='Aportes Acumulados', linewidth=2, color='#A23B72', linestyle='--')
    
    ax.fill_between(df_resultados['Periodo'], 
                    aportes_acumulados, 
                    df_resultados['Saldo Final (USD)'],
                    alpha=0.3, color='#06D6A0', label='Intereses Ganados')
    
    ax.set_xlabel('Periodo', fontsize=12)
    ax.set_ylabel('Monto (USD)', fontsize=12)
    ax.set_title('Crecimiento de la Cartera en el Tiempo', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Formatear eje Y con separadores de miles
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    plt.tight_layout()
    
    return fig


def mostrar_moduloA():
    """
    Módulo A: Crecimiento de cartera.
    Función principal para la interfaz Streamlit.
    
    Retorna:
    --------
    saldo_bruto : float
        Saldo final acumulado (para pasar al Módulo B1)
    aportes_totales : float
        Total de aportes realizados (para pasar al Módulo B1)
    """
    st.subheader("📈 Módulo A – Crecimiento de Cartera")
    
    st.markdown("""
    Este módulo calcula cómo crece tu dinero a lo largo del tiempo mediante **interés compuesto**.
    Puedes simular con un depósito inicial, aportes periódicos, o ambos.
    """)
    
    # ============ INPUTS DEL USUARIO ============
    st.markdown("### 💵 Datos de inversión")
    
    col1, col2 = st.columns(2)
    
    with col1:
        monto_inicial = st.number_input(
            "Monto inicial (USD)",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            help="Depósito único al inicio de la inversión. Puede ser $0 si solo deseas hacer aportes periódicos."
        )
        
        frecuencia = st.selectbox(
            "Frecuencia de aportes",
            options=["Mensual", "Trimestral", "Semestral", "Anual"],
            help="¿Cada cuánto tiempo realizarás aportes? Si no deseas aportes periódicos, deja el monto en $0."
        )
        
        edad_actual = st.number_input(
            "Edad actual",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
            help="Tu edad actual en años."
        )
    
    with col2:
        aporte_periodico = st.number_input(
            "Aporte periódico (USD)",
            min_value=0.0,
            value=200.0,
            step=50.0,
            help="Cantidad que aportarás de forma regular. Si no deseas aportes periódicos, ingresa $0."
        )
        
        tea = st.number_input(
            "Tasa Efectiva Anual - TEA (%)",
            min_value=0.0,
            max_value=50.0,
            value=8.0,
            step=0.5,
            help="Tasa de retorno esperada por año. Ejemplo: 8 para 8% anual."
        )
        
        edad_jubilacion = st.number_input(
            "Edad de jubilación",
            min_value=edad_actual + 1,
            max_value=100,
            value=65,
            step=1,
            help="Edad a la que planeas jubilarte. Debe ser mayor a tu edad actual."
        )
    
    # ============ VALIDACIONES ============
    if monto_inicial == 0 and aporte_periodico == 0:
        st.warning("⚠️ Debes ingresar al menos un monto inicial o un aporte periódico.")
        return None, None
    
    if edad_jubilacion <= edad_actual:
        st.error("❌ La edad de jubilación debe ser mayor a la edad actual.")
        return None, None
    
    # ============ BOTÓN PARA CALCULAR ============
    if st.button("🚀 Calcular Crecimiento", type="primary", use_container_width=True):
        
        try:
            with st.spinner("Calculando proyección..."):
                # Ejecutar simulación
                df_resultados, saldo_final, total_aportado, interes_total = simular_crecimiento_cartera(
                    monto_inicial=monto_inicial,
                    aporte_periodico=aporte_periodico,
                    frecuencia=frecuencia,
                    tea=tea,
                    edad_actual=edad_actual,
                    edad_jubilacion=edad_jubilacion
                )
                
                plazo_años = edad_jubilacion - edad_actual
                
                # ============ MOSTRAR RESULTADOS ============
                st.divider()
                st.markdown("### 📊 Resultados de la Simulación")
                
                # Métricas principales
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Total Aportado", f"${total_aportado:,.2f} USD")
                with col_m2:
                    st.metric("Intereses Ganados", f"${interes_total:,.2f} USD")
                with col_m3:
                    st.metric("💰 Saldo Final", f"${saldo_final:,.2f} USD")
                
                # Rentabilidad
                rentabilidad = (interes_total / total_aportado) * 100 if total_aportado > 0 else 0
                st.info(f"📈 **Rentabilidad total:** {rentabilidad:.2f}% en {plazo_años} años")
                
                # ============ GRÁFICA ============
                st.markdown("### 📉 Gráfica de Crecimiento")
                fig = graficar_crecimiento(df_resultados)
                st.pyplot(fig)
                
                # ============ TABLA DETALLADA ============
                st.markdown("### 📋 Tabla Detallada de Crecimiento")
                
                # Mostrar opciones de visualización
                opcion_tabla = st.radio(
                    "Selecciona qué mostrar:",
                    ["Primeros 10 periodos", "Últimos 10 periodos", "Tabla completa"],
                    horizontal=True
                )
                
                if opcion_tabla == "Primeros 10 periodos":
                    st.dataframe(df_resultados.head(10), use_container_width=True)
                elif opcion_tabla == "Últimos 10 periodos":
                    st.dataframe(df_resultados.tail(10), use_container_width=True)
                else:
                    st.dataframe(df_resultados, use_container_width=True, height=400)
                
                # ============ GUARDAR EN SESSION STATE ============
                st.session_state['saldo_bruto'] = saldo_final
                st.session_state['aportes_totales'] = total_aportado
                
                st.success("✅ Cálculo completado. Los valores se han guardado para usar en el Módulo B (Jubilación).")
                
                # Retornar valores para integración
                return saldo_final, total_aportado
        
        except Exception as e:
            st.error(f"❌ Error en el cálculo: {str(e)}")
            return None, None
    
    # Si aún no se ha calculado, retornar None
    return None, None


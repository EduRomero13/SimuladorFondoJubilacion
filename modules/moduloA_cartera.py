import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def calcular_tasa_periodo(tea, frecuencia):
    """
    Convierte la TEA a tasa por periodo según la frecuencia de aportes.
    """
    frecuencias = {
        "Mensual": 12,
        "Trimestral": 4,
        "Semestral": 2,
        "Anual": 1
    }

    periodos_por_año = frecuencias[frecuencia]

    tasa_periodo = (1 + tea) ** (1 / periodos_por_año) - 1

    return tasa_periodo, periodos_por_año


def simular_crecimiento_cartera(monto_inicial, aporte_periodico, frecuencia, tea, edad_actual, edad_jubilacion):
    """
    Simula el crecimiento de una cartera con interés compuesto.
    """
    if edad_jubilacion <= edad_actual:
        raise ValueError("La edad de jubilación debe ser mayor a la edad actual")
    if tea < 0 or tea > 50:
        raise ValueError("La TEA debe estar entre 0% y 50%")
    if monto_inicial < 0 or aporte_periodico < 0:
        raise ValueError("Los montos no pueden ser negativos")

    plazo_años = edad_jubilacion - edad_actual
    tea_decimal = tea / 100
    tasa_periodo, periodos_por_año = calcular_tasa_periodo(tea_decimal, frecuencia)
    total_periodos = plazo_años * periodos_por_año

    periodos = []
    saldos_iniciales = []
    aportes = []
    intereses = []
    saldos_finales = []

    saldo = monto_inicial

    for periodo in range(total_periodos + 1):
        periodos.append(periodo)
        saldos_iniciales.append(saldo)

        if periodo == 0:
            aportes.append(monto_inicial)
            intereses.append(0.0)
            saldos_finales.append(monto_inicial)
        else:
            saldo_con_aporte = saldo + aporte_periodico
            interes_periodo = saldo_con_aporte * tasa_periodo
            saldo = saldo_con_aporte + interes_periodo
            aportes.append(aporte_periodico)
            intereses.append(interes_periodo)
            saldos_finales.append(saldo)

    df_resultados = pd.DataFrame({
        'Periodo': periodos,
        'Saldo Inicial (USD)': saldos_iniciales,
        'Aporte (USD)': aportes,
        'Interés Ganado (USD)': intereses,
        'Saldo Final (USD)': saldos_finales
    })

    df_resultados = df_resultados.round(2)

    saldo_final = saldos_finales[-1]
    total_aportado = monto_inicial + (aporte_periodico * total_periodos)
    interes_total_ganado = saldo_final - total_aportado

    return df_resultados, saldo_final, total_aportado, interes_total_ganado


def graficar_crecimiento(df_resultados):
    aportes_acumulados = df_resultados['Aporte (USD)'].cumsum()

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

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    plt.tight_layout()

    return fig


def mostrar_moduloA():
    st.subheader("📈 Módulo A – Crecimiento de Cartera")

    st.markdown("""
    Este módulo calcula cómo crece tu dinero a lo largo del tiempo mediante **interés compuesto**.
    Puedes simular con un depósito inicial, aportes periódicos, o ambos.
    """)

    st.markdown("### 💵 Datos de inversión")

    col1, col2 = st.columns(2)

    with col1:
        monto_inicial = st.number_input(
            "Monto inicial (USD)",
            min_value=0.0,
            value=5000.0,
            step=100.0,
        )
        
        frecuencia = st.selectbox(
            "Frecuencia de aportes",
            options=["Mensual", "Trimestral", "Semestral", "Anual"],
        )
        
        edad_actual = st.number_input(
            "Edad actual",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
        )
    
    with col2:
        aporte_periodico = st.number_input(
            "Aporte periódico (USD)",
            min_value=0.0,
            value=200.0,
            step=50.0,
        )
        
        tea = st.number_input(
            "Tasa Efectiva Anual - TEA (%)",
            min_value=0.0,
            max_value=50.0,
            value=8.0,
            step=0.5,
        )
        
        edad_jubilacion = st.number_input(
            "Edad de jubilación",
            min_value=edad_actual + 1,
            max_value=100,
            value=65,
            step=1,
        )

    if monto_inicial == 0 and aporte_periodico == 0:
        st.warning("⚠️ Debes ingresar al menos un monto inicial o un aporte periódico.")
        return None, None

    if edad_jubilacion <= edad_actual:
        st.error("❌ La edad de jubilación debe ser mayor a la edad actual.")
        return None, None

    if st.button("🚀 Calcular Crecimiento", type="primary", use_container_width=True):
        try:
            with st.spinner("Calculando proyección..."):
                df_resultados, saldo_final, total_aportado, interes_total = simular_crecimiento_cartera(
                    monto_inicial=monto_inicial,
                    aporte_periodico=aporte_periodico,
                    frecuencia=frecuencia,
                    tea=tea,
                    edad_actual=edad_actual,
                    edad_jubilacion=edad_jubilacion
                )

                plazo_años = edad_jubilacion - edad_actual

                st.divider()
                st.markdown("### 📊 Resultados de la Simulación")

                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Total Aportado", f"${total_aportado:,.2f} USD")
                with col_m2:
                    st.metric("Intereses Ganados", f"${interes_total:,.2f} USD")
                with col_m3:
                    st.metric("💰 Saldo Final", f"${saldo_final:,.2f} USD")

                rentabilidad = (interes_total / total_aportado) * 100 if total_aportado > 0 else 0
                st.info(f"📈 **Rentabilidad total:** {rentabilidad:.2f}% en {plazo_años} años")

                st.markdown("### 📉 Gráfica de Crecimiento")
                fig = graficar_crecimiento(df_resultados)
                st.pyplot(fig)

                st.markdown("### 📋 Tabla Detallada de Crecimiento")

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

                st.session_state['saldo_bruto'] = saldo_final
                st.session_state['aportes_totales'] = total_aportado

                st.success("✅ Cálculo completado. Los valores se han guardado para usar en el Módulo B (Jubilación).")

                return saldo_final, total_aportado

        except Exception as e:
            st.error(f"❌ Error en el cálculo: {str(e)}")
            return None, None

    return None, None

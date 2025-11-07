import streamlit as st
import numpy as np


# Módulo B — PROYECCIÓN DE RETIRO O PENSIÓN MENSUAL
def mostrar_moduloB2():
    st.title("🧮 Módulo B — Proyección de retiro o pensión mensual")

   st.subheader("1️⃣ Capital acumulado")
    saldo_final = st.number_input(
        "Saldo final acumulado (USD):",
        min_value=0.0,
        value=50000.0,
        step=1000.0,
        format="%.2f"
    )

    # 2️⃣ Parámetros financieros
    st.subheader("2️⃣ Parámetros financieros")

    tasa_retorno = st.number_input(
        "Tasa de retorno anual durante el retiro (%):",
        min_value=0.0,
        value=5.0,
        step=0.1,
        format="%.2f"
    ) / 100
    
    años_retiro = st.number_input(
        "Años de duración estimada de la jubilación:",
        min_value=1,
        value=20,
        step=1
    )
    
    tipo_ganancia = st.selectbox(
        "Tipo de ganancia (para calcular impuesto):",
        ["Fuente extranjera (29.5%)", "Bolsa local (5%)", "Sin impuesto"]
    )
    
    if tipo_ganancia == "Fuente extranjera (29.5%)":
        tasa_impuesto = 0.295
    elif tipo_ganancia == "Bolsa local (5%)":
        tasa_impuesto = 0.05
    else:
        tasa_impuesto = 0.0
    
    # 3️⃣ Cálculo principal (solo pensión mensual)
    st.subheader("3️⃣ Resultados")
    
    # Pensión mensual calculada con fórmula de renta financiera
    tasa_mensual = tasa_retorno / 12
    n_meses = años_retiro * 12
    
    if tasa_mensual == 0:
        pension_mensual = saldo_final / n_meses
    else:
        pension_mensual = saldo_final * (tasa_mensual / (1 - (1 + tasa_mensual) ** -n_meses))
    
    # Aplicar impuesto sobre ganancia total estimada
    total_recibido = pension_mensual * n_meses
    ganancia_total = total_recibido - saldo_final
    impuesto = ganancia_total * tasa_impuesto
    total_neto = total_recibido - impuesto
    
    st.success(f"💰 Pensión mensual estimada: **${pension_mensual:,.2f} USD**")
    st.write(f"Total estimado recibido en {años_retiro} años: **${total_neto:,.2f} USD netos**")
    st.caption(f"(Impuesto aplicado: ${impuesto:,.2f})")
    
    # 4️⃣ Comparador de escenarios
    st.subheader("4️⃣ Comparar escenarios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        edad_1 = st.number_input("Edad de retiro (escenario 1):", min_value=50, max_value=80, value=60)
        tasa_1 = st.number_input("Tasa retorno escenario 1 (%):", min_value=0.0, value=5.0, step=0.1) / 100
    
    with col2:
        edad_2 = st.number_input("Edad de retiro (escenario 2):", min_value=50, max_value=80, value=65)
        tasa_2 = st.number_input("Tasa retorno escenario 2 (%):", min_value=0.0, value=6.0, step=0.1) / 100
    
    if st.button("🔍 Comparar escenarios"):
        # Suponiendo que el capital crece adicionalmente con los años de diferencia
        años_extra = edad_2 - edad_1
        saldo_esc2 = saldo_final * ((1 + tasa_2) ** años_extra)
    
        st.write(f"Escenario 1 ({edad_1} años): Saldo = **${saldo_final:,.2f}** con tasa {tasa_1*100:.1f}%")
        st.write(f"Escenario 2 ({edad_2} años): Saldo = **${saldo_esc2:,.2f}** con tasa {tasa_2*100:.1f}%")
    
        diff = saldo_esc2 - saldo_final
        if diff > 0:
            st.success(f"Jubilarse a los {edad_2} años daría **${diff:,.2f}** más de capital acumulado.")
        else:
            st.warning(f"Jubilarse antes reduce el capital en **${abs(diff):,.2f}**.")

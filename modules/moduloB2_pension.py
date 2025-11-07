import streamlit as st
import numpy as np

def mostrar_moduloB2():
    """
    Módulo B2: Proyección de pensión mensual a partir del saldo neto obtenido en B1.
    Lee el saldo_neto desde st.session_state y calcula la pensión mensual estimada.
    También permite comparar dos escenarios de jubilación.
    """

    st.subheader("💰 Módulo B2 – Proyección de pensión mensual")

    # 1️⃣ Obtener saldo neto y edades desde Módulo B1
    saldo_neto = st.session_state.get("saldo_neto", None)
    edad_actual = st.session_state.get("edad_actual", None)
    edad_jubilacion = st.session_state.get("edad_jubilacion", None)

    if saldo_neto is None:
        st.warning("⚠️ No se encontró el saldo neto del Módulo B1. Por favor, completa primero el **Crecimiento de Cartera**.")
        return None

    st.info(f"Saldo neto disponible al jubilarse: **USD ${saldo_neto:,.2f}**")

    # 2️⃣ Parámetros principales del retiro
    st.markdown("### 📆 Parámetros del retiro")

    años_retiro = st.number_input(
        "Años estimados de jubilación:",
        min_value=1,
        value=20,
        step=1,
        help="Número de años que esperas recibir la pensión."
    )

    tasa_retorno = st.number_input(
        "Tasa de retorno anual durante el retiro (%):",
        min_value=0.0,
        value=5.0,
        step=0.1,
        format="%.2f",
        help="Rentabilidad esperada del fondo durante el retiro."
    ) / 100

    # 3️⃣ Cálculo de pensión mensual base
    st.markdown("### 🧮 Cálculo de pensión mensual")

    tasa_mensual = tasa_retorno / 12
    n_meses = años_retiro * 12

    if tasa_mensual == 0:
        pension_mensual = saldo_neto / n_meses
    else:
        pension_mensual = saldo_neto * (tasa_mensual / (1 - (1 + tasa_mensual) ** -n_meses))

    total_recibido = pension_mensual * n_meses
    ganancia_total = total_recibido - saldo_neto

    st.success(f"💵 Pensión mensual estimada: **${pension_mensual:,.2f} USD**")
    st.write(f"Total estimado recibido en {años_retiro} años: **${total_recibido:,.2f} USD**")
    st.caption(f"(Incluye una ganancia estimada de ${ganancia_total:,.2f})")

    # 4️⃣ Comparar escenarios
    st.divider()
    st.markdown("### 🔍 Comparar escenarios de jubilación")

    col1, col2 = st.columns(2)
    with col1:
        edad_1 = st.number_input("Edad de retiro (escenario 1):", min_value=50, max_value=80, value=60)
        tasa_1 = st.number_input("Tasa de retorno anual (escenario 1) %:", min_value=0.0, value=5.0, step=0.1) / 100
        años_retiro_1 = st.number_input("Años de jubilación (escenario 1):", min_value=1, value=20, step=1)
    with col2:
        edad_2 = st.number_input("Edad de retiro (escenario 2):", min_value=50, max_value=80, value=65)
        tasa_2 = st.number_input("Tasa de retorno anual (escenario 2) %:", min_value=0.0, value=6.0, step=0.1) / 100
        años_retiro_2 = st.number_input("Años de jubilación (escenario 2):", min_value=1, value=18, step=1)

    if st.button("🔎 Comparar escenarios"):
        if edad_actual is None:
            edad_actual = st.number_input("Ingresa tu edad actual (solo para comparar):", min_value=18, value=40)

        # Simular crecimiento del fondo hasta la edad de jubilación
        saldo_esc1 = saldo_neto * ((1 + tasa_1) ** (edad_1 - edad_actual))
        saldo_esc2 = saldo_neto * ((1 + tasa_2) ** (edad_2 - edad_actual))

        # Calcular pensión mensual para cada escenario
        tasa_mensual_1 = tasa_1 / 12
        tasa_mensual_2 = tasa_2 / 12
        n_meses_1 = años_retiro_1 * 12
        n_meses_2 = años_retiro_2 * 12

        if tasa_mensual_1 == 0:
            pension_1 = saldo_esc1 / n_meses_1
        else:
            pension_1 = saldo_esc1 * (tasa_mensual_1 / (1 - (1 + tasa_mensual_1) ** -n_meses_1))

        if tasa_mensual_2 == 0:
            pension_2 = saldo_esc2 / n_meses_2
        else:
            pension_2 = saldo_esc2 * (tasa_mensual_2 / (1 - (1 + tasa_mensual_2) ** -n_meses_2))

        # Mostrar resultados
        st.markdown("#### 📊 Resultados comparativos")

        colA, colB = st.columns(2)
        with colA:
            st.info(f"**Escenario 1 ({edad_1} años)**")
            st.write(f"- Saldo acumulado: **${saldo_esc1:,.2f}**")
            st.write(f"- Pensión mensual: **${pension_1:,.2f}**")
            st.write(f"- Duración del retiro: {años_retiro_1} años")
        with colB:
            st.success(f"**Escenario 2 ({edad_2} años)**")
            st.write(f"- Saldo acumulado: **${saldo_esc2:,.2f}**")
            st.write(f"- Pensión mensual: **${pension_2:,.2f}**")
            st.write(f"- Duración del retiro: {años_retiro_2} años")

        diferencia_pension = pension_2 - pension_1
        diferencia_saldo = saldo_esc2 - saldo_esc1

        if diferencia_pension > 0:
            st.success(f"🟢 Jubilarse a los {edad_2} años aumenta la pensión mensual en **${diferencia_pension:,.2f}** (y el saldo en ${diferencia_saldo:,.2f}).")
        else:
            st.warning(f"🟠 Jubilarse antes reduce la pensión mensual en **${abs(diferencia_pension):,.2f}** (y el saldo en ${abs(diferencia_saldo):,.2f}).")

    # 5️⃣ Guardar resultados en session_state
    st.session_state["pension_mensual"] = pension_mensual
    st.session_state["total_recibido"] = total_recibido

    return pension_mensual

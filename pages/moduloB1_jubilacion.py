import streamlit as st

def mostrar_moduloB1(saldo_bruto=None, aportes_totales=None):
    """
    Módulo B1: Cálculo del saldo neto en jubilación tras impuestos.

    Parámetros:
        saldo_bruto (float): Fondo acumulado desde Módulo A (VF).
        aportes_totales (float): Total invertido (inicial + aportes).

    La función intenta usar los parámetros, y si no están disponibles,
    busca en st.session_state (donde Módulo A los guarda al calcular).
    """
    st.subheader("🧮 Módulo B1 – Impuestos y Saldo Neto en Jubilación")

    # 1. Obtener datos desde parámetros o session_state
    if saldo_bruto is None:
        saldo_bruto = st.session_state.get("saldo_bruto", None)
    if aportes_totales is None:
        aportes_totales = st.session_state.get("aportes_totales", None)

    # 2. Si no hay datos de Módulo A, avisar
    if saldo_bruto is None or aportes_totales is None:
        st.warning("⚠️ No se encontraron resultados del Módulo A. Por favor, completa primero el **Crecimiento de Cartera**.")
        st.stop()

    # 3. Entradas del usuario
    col1, col2 = st.columns(2)
    with col1:
        edad_actual = st.number_input(
            "Edad actual",
            min_value=18, max_value=100, value=30,
            help="Edad actual (usada solo para confirmar el horizonte de inversión)."
        )
    with col2:
        edad_jubilacion = st.number_input(
            "Edad de jubilación",
            min_value=edad_actual + 1, max_value=100, value=65,
            help="Edad de retiro. Debe ser mayor a la edad actual."
        )

    tipo_inversion = st.selectbox(
        "Tipo de inversión",
        options=["BVL - Bolsa local", "BEX - Fuente extranjera"],
        help="Determina la tasa de impuesto: 5% (BVL) o 29.5% (BEX) sobre **las ganancias**."
    )

    # 4. Validar que edad_jubilacion > edad_actual
    if edad_jubilacion <= edad_actual:
        st.error("❌ La edad de jubilación debe ser mayor que la edad actual.")
        return None

    # 5. Cálculos
    anos_inversion = edad_jubilacion - edad_actual
    ganancia = max(0.0, saldo_bruto - aportes_totales)  # Nunca negativa
    tasa_impuesto = 0.05 if "BVL" in tipo_inversion else 0.295
    monto_impuesto = ganancia * tasa_impuesto
    saldo_neto = saldo_bruto - monto_impuesto

    # 6. Mostrar resultados
    st.divider()
    st.markdown("### 📊 Resumen del cálculo")

    col1, col2, col3 = st.columns(3)
    col1.metric("Fondo acumulado (bruto)", f"${saldo_bruto:,.2f}")
    col2.metric("Aportes totales", f"${aportes_totales:,.2f}")
    col3.metric("Ganancia", f"${ganancia:,.2f}")

    st.markdown("### 💰 Resultado después de impuestos")
    st.write(f"- **Tasa de impuesto aplicada:** {tasa_impuesto*100:.1f}% ({'BVL' if tasa_impuesto == 0.05 else 'BEX'})")
    st.write(f"- **Impuesto a pagar:** USD ${monto_impuesto:,.2f}")
    st.success(f"### Saldo neto disponible: **USD ${saldo_neto:,.2f}**")

    # 7. Guardar en session_state para Módulo B2
    st.session_state["saldo_neto"] = saldo_neto
    st.session_state["edad_jubilacion"] = edad_jubilacion
    st.session_state["anos_inversion"] = anos_inversion

    return saldo_neto

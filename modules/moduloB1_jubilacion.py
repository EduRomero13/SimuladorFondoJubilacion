import streamlit as st

def mostrar_moduloB1():
    """
    Módulo B1: Cálculo del saldo neto en jubilación tras impuestos.
    
    Lee los datos del Módulo A desde st.session_state, incluyendo las edades.
    """
    st.subheader("🧮 Módulo B1 – Impuestos y Saldo Neto en Jubilación")

    # 1. Obtener datos del Módulo A desde session_state
    saldo_bruto = st.session_state.get("saldo_bruto", None)
    aportes_totales = st.session_state.get("aportes_totales", None)
    edad_actual = st.session_state.get("edad_actual", None)  # 👈 LEER DESDE SESSION STATE
    edad_jubilacion = st.session_state.get("edad_jubilacion", None)  # 👈 LEER DESDE SESSION STATE

    if saldo_bruto is None or aportes_totales is None:
        st.warning("⚠️ No se encontraron resultados del Módulo A. Por favor, completa primero el **Crecimiento de Cartera**.")
        st.stop()

    # 2. Mostrar las edades (ya no pedirlas, solo mostrarlas)
    st.markdown("### 📅 Edad del usuario")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Edad actual: **{edad_actual} años**")  # 👈 MOSTRAR, NO PEDIR
    with col2:
        st.info(f"Edad de jubilación: **{edad_jubilacion} años**")  # 👈 MOSTRAR, NO PEDIR

    # 3. Validar que edad_jubilacion > edad_actual
    if edad_jubilacion <= edad_actual:
        st.error("❌ La edad de jubilación debe ser mayor que la edad actual.")
        st.stop()

    # 4. Entrada del tipo de inversión
    tipo_inversion = st.selectbox(
        "Tipo de inversión",
        options=["BVL - Bolsa local", "BEX - Fuente extranjera"],
        help="Determina la tasa de impuesto: 5% (BVL) o 29.5% (BEX) sobre **las ganancias**."
    )

    # 5. Cálculos
    anos_inversion = edad_jubilacion - edad_actual
    ganancia = max(0.0, saldo_bruto - aportes_totales)  # Nunca negativa
    tasa_impuesto = 0.05 if "BVL" in tipo_inversion else 0.295
    monto_impuesto = ganancia * tasa_impuesto
    saldo_neto = saldo_bruto - monto_impuesto

    # 6. Mostrar resultados
    st.divider()
    st.markdown("### 📊 Resumen del cálculo")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Fondo acumulado (bruto)", f"${saldo_bruto:,.2f}")
    col_b.metric("Aportes totales", f"${aportes_totales:,.2f}")
    col_c.metric("Ganancia", f"${ganancia:,.2f}")

    st.markdown("### 💰 Resultado después de impuestos")
    st.write(f"- **Tasa de impuesto aplicada:** {tasa_impuesto*100:.1f}%")
    st.write(f"- **Impuesto a pagar:** USD ${monto_impuesto:,.2f}")
    st.success(f"### Saldo neto disponible: **USD ${saldo_neto:,.2f}**")

    # 7. Guardar en session_state para Módulo B2
    st.session_state["saldo_neto"] = saldo_neto
    st.session_state["anos_inversion"] = anos_inversion  # Por si acaso

    return saldo_neto
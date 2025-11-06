import streamlit as st

def mostrar_moduloB1(saldo_bruto=None, aportes_totales=None):
    """
    Módulo B1: Cálculos base de jubilación.
    Recibe el fondo acumulado (saldo_bruto) y los aportes totales.
    Calcula impuestos sobre la ganancia y devuelve el saldo neto.
    
    Parámetros:
        saldo_bruto (float): Valor futuro acumulado desde Módulo A.
        aportes_totales (float): Suma de fondo inicial + aportes periódicos.
    
    Retorna:
        float: saldo_neto después de impuestos.
    """
    st.subheader("🧮 Módulo B1 – Cálculo del Saldo Neto en Jubilación")

    # Entradas obligatorias del usuario
    col1, col2 = st.columns(2)
    with col1:
        edad_actual = st.number_input(
            "Edad actual",
            min_value=18, max_value=100, value=30,
            help="Edad actual del usuario (entre 18 y 100 años)."
        )
    with col2:
        edad_jubilacion = st.number_input(
            "Edad de jubilación",
            min_value=edad_actual + 1, max_value=85, value=65,
            help="Edad a la que planea jubilarse (debe ser mayor a la edad actual)."
        )

    tipo_inversion = st.selectbox(
        "Tipo de inversión",
        options=["BVL - Bolsa local", "BEX - Fuente extranjera"],
        help="Determina la tasa de impuesto sobre ganancias: 5% (BVL) o 29.5% (BEX)."
    )

    # Valores de prueba si no se reciben del Módulo A
    if saldo_bruto is None or aportes_totales is None:
        st.info("ℹ️ Modo de prueba: usando valores predeterminados desde Módulo A.")
        saldo_bruto = 650000.0      # Valor futuro simulado
        aportes_totales = 250000.0  # Ej: fondo inicial + aportes

    # Cálculos
    años_inversion = edad_jubilacion - edad_actual
    ganancia = max(0.0, saldo_bruto - aportes_totales)
    tasa_impuesto = 0.05 if "BVL" in tipo_inversion else 0.295
    impuesto = ganancia * tasa_impuesto
    saldo_neto = saldo_bruto - impuesto

    # Mostrar resultados
    st.divider()
    st.write("### 📊 Resultados del cálculo")
    st.write(f"- **Años de inversión:** {años_inversion} años")
    st.write(f"- **Fondo acumulado (bruto):** USD ${saldo_bruto:,.2f}")
    st.write(f"- **Aportes totales realizados:** USD ${aportes_totales:,.2f}")
    st.write(f"- **Ganancia generada:** USD ${ganancia:,.2f}")
    st.write(f"- **Impuesto aplicado ({tasa_impuesto*100:.1f}%):** USD ${impuesto:,.2f}")
    st.success(f"### 💰 **Saldo neto disponible en jubilación:** USD ${saldo_neto:,.2f}")

    return saldo_neto
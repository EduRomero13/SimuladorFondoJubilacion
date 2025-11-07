import streamlit as st

def mostrar_reporte():
    """Renderiza la sección de reporte consolidado y permite generar/descargar el PDF.
    Usa valores guardados en `st.session_state` por los demás módulos.
    """
    st.markdown('<div id="modExport"></div>', unsafe_allow_html=True)
    st.markdown("## 🖨️ Reporte consolidado (PDF)")

    has_a = 'saldo_bruto' in st.session_state and 'aportes_totales' in st.session_state
    has_b1 = 'saldo_neto' in st.session_state
    has_b2 = 'pension_mensual' in st.session_state
    has_c = 'bono_vp' in st.session_state

    if not (has_a and has_b1 and has_b2 and has_c):
        st.info("El reporte estará disponible una vez que se hayan ejecutado los módulos A (Crecimiento), B1 (Impuestos), B2 (Pensión) y C (Bonos).\n\nActualmente faltan:")
        faltantes = []
        if not has_a:
            faltantes.append("Módulo A: resultados de crecimiento")
        if not has_b1:
            faltantes.append("Módulo B1: saldo neto después de impuestos")
        if not has_b2:
            faltantes.append("Módulo B2: pensión mensual estimada")
        if not has_c:
            faltantes.append("Módulo C: resultados del bono")
        for f in faltantes:
            st.write(f"- {f}")
        return

    st.success("✅ Todos los módulos se han ejecutado. Genera el reporte PDF abajo.")

    # Preparar datos clave (ordenados de forma legible)
    datos = {
        'Fondo acumulado (bruto)': st.session_state.get('saldo_bruto'),
        'Aportes totales': st.session_state.get('aportes_totales'),
        'Saldo neto (post-impuestos)': st.session_state.get('saldo_neto'),
        'Edad de jubilación': st.session_state.get('edad_jubilacion'),
        'Años de inversión': st.session_state.get('anos_inversion'),
        'Pensión mensual estimada': st.session_state.get('pension_mensual'),
        'Total recibido estimado': st.session_state.get('total_recibido')
    }

    # Incluir datos del bono (Módulo C)
    datos['Valor presente (bono)'] = st.session_state.get('bono_vp')
    datos['Parámetros bono'] = st.session_state.get('bono_params')

    st.write("### Valores incluidos en el reporte")

    ordered_keys = [
        'Fondo acumulado (bruto)',
        'Aportes totales',
        'Saldo neto (post-impuestos)',
        'Edad de jubilación',
        'Años de inversión',
        'Pensión mensual estimada',
        'Total recibido estimado',
        'Valor presente (bono)'
    ]

    for key in ordered_keys:
        val = datos.get(key)
        if val is None:
            display = "-"
        else:
            if isinstance(val, (int, float)) and 'Pensión' not in key and 'Edad' not in key and 'Años' not in key:
                display = f"${val:,.2f}"
            else:
                display = f"{val}"
        st.markdown(f"**{key}**: {display}")

    params = datos.get('Parámetros bono') or {}
    if params:
        p_str = (
            f"Nominal: {params.get('valor_nominal')}, "
            f"Cupón: {params.get('tasa_cupon')}%, "
            f"Frecuencia: {params.get('frecuencia')}, "
            f"TEA: {params.get('tasa_tea')}%, "
            f"Años: {params.get('anios')}"
        )
        st.markdown(f"**Parámetros del bono:** <small>{p_str}</small>", unsafe_allow_html=True)

    st.markdown("\n")

    # Generar PDF y ofrecer descarga directa al usuario con un único control
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, height - 72, "Reporte consolidado - Simulador de Jubilación")

        c.setFont("Helvetica", 12)
        y = height - 110
        # Escribir los datos en un orden legible
        for label in [
            'Fondo acumulado (bruto)', 'Aportes totales', 'Saldo neto (post-impuestos)',
            'Edad de jubilación', 'Años de inversión', 'Pensión mensual estimada', 'Total recibido estimado'
        ]:
            val = datos.get(label)
            c.drawString(72, y, f"{label}: {val}")
            y -= 18
            if y < 72:
                c.showPage()
                y = height - 72

        # Sección bonos
        y -= 8
        c.drawString(72, y, "Bonos:")
        y -= 18
        c.drawString(72, y, f"Valor presente (bono): {datos.get('Valor presente (bono)')}")
        y -= 18
        params = datos.get('Parámetros bono') or {}
        for k, v in params.items():
            c.drawString(72, y, f"{k}: {v}")
            y -= 16
            if y < 72:
                c.showPage()
                y = height - 72

        c.showPage()
        c.save()
        buffer.seek(0)

        pdf_bytes = buffer.getvalue()

        # Botón que descarga directamente el PDF cuando el usuario hace clic
        st.download_button("Generar reporte PDF", data=pdf_bytes, file_name="reporte_simulador.pdf", mime="application/pdf")

    except Exception as e:
        st.error("No se pudo generar el PDF porque falta la librería 'reportlab' o ocurrió un error. Instálala con: pip install reportlab")
        st.exception(e)

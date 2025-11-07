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

    # === VISTA SIMPLE EN LA PÁGINA: un dato por línea, sin columnas ===
    st.markdown("### Resumen rápido (vista en página)")

    # Módulo A
    st.markdown("**Módulo A — Crecimiento de Cartera**")
    monto_inicial = st.session_state.get('monto_inicial')
    aporte_periodico = st.session_state.get('aporte_periodico')
    frecuencia_aporte = st.session_state.get('frecuencia_aporte')
    # Leer otras variables desde session_state (si existen)
    tea = st.session_state.get('tea')
    saldo_bruto = st.session_state.get('saldo_bruto')
    total_aportado = st.session_state.get('total_aportado') or st.session_state.get('aportes_totales')
    interes_total = st.session_state.get('interes_total')

    # Módulo B1
    tipo_inversion = st.session_state.get('tipo_inversion')
    tasa_impuesto = st.session_state.get('tasa_impuesto', 0)
    monto_impuesto = st.session_state.get('monto_impuesto')
    ganancia = st.session_state.get('ganancia')

    # Módulo B2
    tasa_retorno = st.session_state.get('tasa_retorno', 0)
    años_retiro = st.session_state.get('años_retiro') or st.session_state.get('anos_retiro')
    pension_mensual = st.session_state.get('pension_mensual')
    total_recibido = st.session_state.get('total_recibido') or st.session_state.get('total_neto')

    # Módulo C
    bono_params = st.session_state.get('bono_params', {})
    bono_vp = st.session_state.get('bono_vp')
    # ---- VISTA EN PÁGINA: mostrar cada dato en una línea ----
    def fmt_money_page(x):
        try:
            return f"${x:,.2f}"
        except Exception:
            return str(x)

    # Módulo A (vista rápida)
    st.write(f"- Monto inicial: {fmt_money_page(monto_inicial)}")
    st.write(f"- Aporte periódico: {fmt_money_page(aporte_periodico)}")
    st.write(f"- Frecuencia: {frecuencia_aporte}")
    st.write(f"- TEA: {tea}%")
    st.write(f"- Saldo bruto (final): {fmt_money_page(saldo_bruto)}")
    st.write(f"- Total aportado: {fmt_money_page(total_aportado)}")
    st.write(f"- Intereses: {fmt_money_page(interes_total)}")

    st.markdown("**Módulo B1 — Impuestos (vista rápida)**")
    st.write(f"- Tipo inversión: {tipo_inversion}")
    try:
        st.write(f"- Tasa impuesto: {tasa_impuesto*100:.1f}%")
    except Exception:
        st.write(f"- Tasa impuesto: {tasa_impuesto}")
    st.write(f"- Saldo neto (post-impuestos): {fmt_money_page(st.session_state.get('saldo_neto'))}")
    st.write(f"- Impuesto estimado: {fmt_money_page(monto_impuesto)}")
    st.write(f"- Ganancia antes de impuestos: {fmt_money_page(ganancia)}")

    st.markdown("**Módulo B2 — Pensión (vista rápida)**")
    try:
        st.write(f"- Tasa retorno anual: {tasa_retorno*100:.2f}%")
    except Exception:
        st.write(f"- Tasa retorno anual: {tasa_retorno}")
    st.write(f"- Años de retiro: {años_retiro}")
    st.write(f"- Pensión mensual estimada: {fmt_money_page(pension_mensual)}")
    st.write(f"- Total neto estimado recibido: {fmt_money_page(total_recibido)}")

    st.markdown("**Módulo C — Bonos (vista rápida)**")
    st.write(f"- Valor nominal: {fmt_money_page(bono_params.get('valor_nominal'))}")
    st.write(f"- Cupón anual: {bono_params.get('tasa_cupon')}%")
    st.write(f"- Frecuencia: {bono_params.get('frecuencia')}")
    st.write(f"- TEA (bono): {bono_params.get('tasa_tea')}%")
    st.write(f"- Valor presente (bono): {fmt_money_page(bono_vp)}")

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io

        def fmt_money(x):
            try:
                return f"${x:,.2f}"
            except Exception:
                return str(x)

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(72, height - 72, "Reporte consolidado - Simulador de Jubilación")

        y = height - 100

        # Helper para escribir líneas y manejar salto de página
        def write_line(text, bold=False, size=10, indent=0):
            nonlocal y
            font = "Helvetica-Bold" if bold else "Helvetica"
            c.setFont(font, size)
            c.drawString(72 + indent, y, text)
            y -= (size + 6)
            if y < 72:
                c.showPage()
                y = height - 72

        # Helper: insertar una línea en blanco para separar módulos (más simple)
        def insert_blank():
            nonlocal y
            y -= 12
            if y < 72:
                c.showPage()
                y = height - 72

        # Módulo A - entradas y resultados en líneas separadas
        insert_blank()
        write_line("Módulo A - Crecimiento de cartera:", bold=True, size=12)
        write_line(f"- Monto inicial: {fmt_money(monto_inicial)}", size=10, indent=10)
        write_line(f"- Aporte periódico: {fmt_money(aporte_periodico)}", size=10, indent=10)
        write_line(f"- Frecuencia: {frecuencia_aporte}", size=10, indent=10)
        write_line(f"- TEA: {tea}%", size=10, indent=10)
        write_line("Resultados:", bold=True, size=11)
        write_line(f"Saldo bruto (final): {fmt_money(saldo_bruto)}", size=10, indent=10)
        write_line(f"Total aportado: {fmt_money(total_aportado)}", size=10, indent=10)
        write_line(f"Intereses: {fmt_money(interes_total)}", size=10, indent=10)
        write_line(" ", size=6)

        # Módulo B1
        insert_blank()
        write_line("Módulo B1 - Impuestos:", bold=True, size=12)
        write_line(f"- Tipo inversión: {tipo_inversion}", size=10, indent=10)
        write_line(f"- Tasa impuesto: {tasa_impuesto*100:.1f}%", size=10, indent=10)
        write_line("Resultados:", bold=True, size=11)
        write_line(f"Saldo neto (post-impuestos): {fmt_money(st.session_state.get('saldo_neto'))}", size=10, indent=10)
        write_line(f"Impuesto estimado: {fmt_money(monto_impuesto)}", size=10, indent=10)
        write_line(f"Ganancia antes de impuestos: {fmt_money(ganancia)}", size=10, indent=10)
        write_line(" ", size=6)

        # Módulo B2
        insert_blank()
        write_line("Módulo B2 - Pensión:", bold=True, size=12)
        write_line(f"- Tasa retorno anual: {tasa_retorno*100:.2f}%", size=10, indent=10)
        write_line(f"- Años de retiro: {años_retiro}", size=10, indent=10)
        write_line("Resultados:", bold=True, size=11)
        write_line(f"Pensión mensual estimada: {fmt_money(pension_mensual)}", size=10, indent=10)
        write_line(f"Total neto estimado recibido: {fmt_money(total_recibido)}", size=10, indent=10)
        write_line(" ", size=6)

        # Módulo C
        insert_blank()
        write_line("Módulo C - Bonos:", bold=True, size=12)
        write_line(f"- Valor nominal: {fmt_money(bono_params.get('valor_nominal'))}", size=10, indent=10)
        write_line(f"- Cupón anual: {bono_params.get('tasa_cupon')}%", size=10, indent=10)
        write_line(f"- Frecuencia: {bono_params.get('frecuencia')}", size=10, indent=10)
        write_line(f"- TEA (bono): {bono_params.get('tasa_tea')}%", size=10, indent=10)
        write_line("Resultados:", bold=True, size=11)
        write_line(f"Valor presente (bono): {fmt_money(bono_vp)}", size=10, indent=10)
        write_line(" ", size=6)


        c.showPage()
        c.save()
        buffer.seek(0)

        pdf_bytes = buffer.getvalue()

        # Botón que descarga directamente el PDF cuando el usuario hace clic
        st.download_button("Generar reporte PDF", data=pdf_bytes, file_name="reporte_simulador.pdf", mime="application/pdf")

    except Exception as e:
        st.error("No se pudo generar el PDF porque falta la librería 'reportlab' o ocurrió un error. Instálala con: pip install reportlab")
        st.exception(e)

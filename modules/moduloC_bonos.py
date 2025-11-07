import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt


def mostrar_moduloC():
    """
    Muestra la calculadora de Valor Presente de un bono como función
    para poder invocarla desde otras páginas.
    """
    st.subheader("💰 Módulo C – Calculadora de Valor Presente de un Bono")

    opciones_frecuencia = {
        "Anual": 1,
        "Semestral": 2,
        "Cuatrimestral": 3,
        "Trimestral": 4,
        "Bimestral": 6,
        "Mensual": 12
    }

    valor_nominal = st.number_input(
                        "Valor nominal del bono", 
                        value=1000.0, 
                        min_value=0.0,
                        step=100.0,
                        help="Valor al que se emitió el bono."
                    )
    tasa_cupon = st.number_input(
                        "Tasa de cupón anual (%)", 
                        value=5.0, 
                        min_value=0.0,
                        step=0.5,
                        help="Tasa de interés anual que paga el bono."
                        )
    frecuencia_nombre = st.selectbox(
                        "Frecuencia de pago", 
                        list(opciones_frecuencia.keys()),
                        help="Frecuencia con la que se pagan los cupones."
                        )

    tasa_tea = st.number_input(
                        "Tasa de retorno esperada (TEA %)", 
                        value=6.0, 
                        min_value=0.0,
                        step=0.5,
                        help="Tasa de retorno anual esperada por el inversionista.")
    
    anios = st.number_input(
                        "Años al vencimiento", 
                        value=5, 
                        min_value=1,
                        step=1,
                        help="Número de años hasta que el bono vence.")

    frecuencia = opciones_frecuencia[frecuencia_nombre]

    # ============ VALIDACIONES ============
    if valor_nominal == 0 or tasa_cupon == 0 or tasa_tea == 0:
        st.warning("⚠️ Debes ingresar todos los datos para realizar el cálculo.")

    else:
        if st.button("📉 Calcular valor presente"):
            cupon = valor_nominal * (tasa_cupon / 100) / frecuencia
            tasa_periodica = (1 + tasa_tea / 100) ** (1 / frecuencia) - 1
            n_periodos = int(anios * frecuencia)
    
            flujos = []
            valores_descontados = []
    
            for i in range(1, n_periodos + 1):
                flujo = cupon
                if i == n_periodos:
                    flujo += valor_nominal
                # Asegurar que los valores sean finitos
                flujo = float(flujo)
                if not math.isfinite(flujo):
                    flujo = 0.0
                flujos.append(flujo)
                # calcular valor presente y garantizar finito
                try:
                    valor_presente = float(flujo) / ((1 + float(tasa_periodica)) ** i)
                except Exception:
                    valor_presente = 0.0
                if not math.isfinite(valor_presente):
                    valor_presente = 0.0
                valores_descontados.append(valor_presente)
    
            df = pd.DataFrame({
                "Periodo": range(1, n_periodos + 1),
                "Flujo": flujos,
                "Valor descontado": valores_descontados
            })

            # Limpiar posibles infinitos/NaN antes de almacenar y mostrar
            df = df.replace([np.inf, -np.inf], np.nan)
            df["Flujo"] = pd.to_numeric(df["Flujo"], errors='coerce').fillna(0.0)
            df["Valor descontado"] = pd.to_numeric(df["Valor descontado"], errors='coerce').fillna(0.0)
    
            valor_presente_total = sum(valores_descontados)

            # Guardar resultados en session_state para que el app principal pueda usarlos
            st.session_state['bono_vp'] = float(valor_presente_total)
            st.session_state['bono_params'] = {
                'valor_nominal': float(valor_nominal),
                'tasa_cupon': float(tasa_cupon),
                'frecuencia': frecuencia_nombre,
                'tasa_tea': float(tasa_tea),
                'anios': int(anios)
            }
            st.session_state['bono_df'] = df

    
            st.subheader("📊 Tabla de flujos descontados")
            st.dataframe(df.style.format({"Flujo": "{:,.2f}", "Valor descontado": "{:,.2f}"}))

            st.markdown(f"### 💵 Valor Presente Total (PV): **${valor_presente_total:,.2f}**")

            st.subheader("📈 Valor presente de cada flujo")
            # Usar serie limpia para gráfico (evitar inf/nan que generan advertencias en Vega)
            serie_vp = df.set_index("Periodo")["Valor descontado"].astype(float).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            # Dibujar con matplotlib (evitar Vega/Altair para prevenir advertencias en consola)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(serie_vp.index.astype(str), serie_vp.values, color='#2b8cbe')
            ax.set_xlabel('Periodo')
            ax.set_ylabel('Valor descontado')
            ax.set_title('Valor presente de cada flujo')
            plt.tight_layout()
            st.pyplot(fig)


if __name__ == "__main__":
    mostrar_moduloC()

import streamlit as st
import pandas as pd


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
                flujos.append(flujo)
                valor_presente = flujo / ((1 + tasa_periodica) ** i)
                valores_descontados.append(valor_presente)
    
            df = pd.DataFrame({
                "Periodo": range(1, n_periodos + 1),
                "Flujo": flujos,
                "Valor descontado": valores_descontados
            })
    
            valor_presente_total = sum(valores_descontados)
    
            st.subheader("📊 Tabla de flujos descontados")
            st.dataframe(df.style.format({"Flujo": "{:,.2f}", "Valor descontado": "{:,.2f}"}))
    
            st.markdown(f"### 💵 Valor Presente Total (PV): **${valor_presente_total:,.2f}**")
    
            st.subheader("📈 Valor presente de cada flujo")
            st.bar_chart(df.set_index("Periodo")["Valor descontado"])


if __name__ == "__main__":
    mostrar_moduloC()

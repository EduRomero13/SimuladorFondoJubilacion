import streamlit as st

# Importar las funciones de cada módulo desde la carpeta modules
from modules.moduloA_cartera import mostrar_moduloA
from modules.moduloB1_jubilacion import mostrar_moduloB1
from modules.moduloC_bonos import mostrar_moduloC
from modules.moduloB2_pension import mostrar_moduloB2

# Oculta el listado automático de páginas (Streamlit Pages) que aparece arriba
# del sidebar. Esto no borra los archivos en `pages/` pero oculta la sección.
st.markdown(
	"""
	<style>
	/* Oculta la navegación automática de Streamlit Pages en el sidebar */
	div[data-testid="stSidebarNav"] { display: none; }
	</style>
	""",
	unsafe_allow_html=True,
)


def main():
	st.set_page_config(page_title="Simulador - Todos los Módulos", layout="wide")

	# Sidebar simple
	with st.sidebar:
		st.title("Navegación")
		st.write("Selecciona el módulo a mostrar:")
		opcion = st.radio("", ["Módulo A - Cartera", "Módulo B1 - Jubilación", "Módulo B2 - Pensión", "Módulo C - Bonos"], index=0)
		st.markdown("---")
		st.markdown("Hecho para integrar y visualizar todos los módulos en una sola página.")

	# Área principal
	st.header("Simulador de Fondo de Jubilación")

	if opcion == "Módulo A - Cartera":
		mostrar_moduloA()
	elif opcion == "Módulo B1 - Jubilación":
		# mostrar_moduloB1 intenta leer valores de st.session_state si no se pasan parámetros
		mostrar_moduloB1()
	elif opcion == "Módulo B2 - Pensión":
		mostrar_moduloB2()
	elif opcion == "Módulo C - Bonos":
		mostrar_moduloC()



if __name__ == "__main__":
	main()


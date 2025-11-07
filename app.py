import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página (debe hacerse antes de cualquier UI)
st.set_page_config(page_title="Simulador - Todos los Módulos", layout="wide")

# Oculta la navegación automática de Streamlit Pages en el sidebar
st.markdown(
    """
    <style>
    div[data-testid="stSidebarNav"] { display: none; }
    /* Scroll suave a nivel de documento */
    html, body { scroll-behavior: smooth; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Importar las funciones de cada módulo desde la carpeta modules
from modules.moduloA_cartera import mostrar_moduloA
from modules.moduloB1_jubilacion import mostrar_moduloB1
from modules.moduloC_bonos import mostrar_moduloC
from modules.moduloB2_pension import mostrar_moduloB2


# Navegación del sidebar se implementa con HTML/JS para hacer scroll sin recarga


def main():
    # Sidebar con enlaces que hacen scroll dentro de la misma página
    with st.sidebar:
        st.title("Navegación")
        st.write("Selecciona el módulo a mostrar:")
        st.markdown("<a href='#modIntro'>• Introducción</a>", unsafe_allow_html=True)
        st.markdown("<a href='#modA'>• Módulo A - Cartera</a>", unsafe_allow_html=True)
        st.markdown("<a href='#modB1'>• Módulo B1 - Jubilación</a>", unsafe_allow_html=True)
        st.markdown("<a href='#modB2'>• Módulo B2 - Pensión</a>", unsafe_allow_html=True)
        st.markdown("<a href='#modC'>• Módulo C - Bonos</a>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("Navega entre módulos rápidamente haciendo click en estas opciones.")

    # Área principal: renderizamos TODOS los módulos en orden, con anclas HTML
    st.header("Simulador de Fondo de Jubilación")

    # Introducción/Resumen arriba de Módulo A
    st.markdown('<div id="modIntro"></div>', unsafe_allow_html=True)
    st.markdown("## 📘 Introducción al Simulador", unsafe_allow_html=True)
    st.markdown(
        (
            "Este simulador muestra tres módulos principales: **Crecimiento de Cartera (A)**, "
            "**Impuestos y Saldo Neto (B1)**, **Proyección de Pensión (B2)** y **Bonos (C)**. "
            "Usa los controles del sidebar para saltar a cada sección. Cada módulo mantiene "
            "su propia interfaz: calcula proyecciones, aplica impuestos y permite analizar "
            "escenarios financieros.\n\n"
            "Puedes ejecutar el cálculo en el Módulo A para obtener resultados que se usan "
            "en los módulos B1 y B2, pero también puedes introducir valores manualmente si lo prefieres."
        )
    )
    st.markdown("---")

    # Ancla y Módulo A
    st.markdown('<div id="modA"></div>', unsafe_allow_html=True)
    st.markdown("## Módulo A – Crecimiento de Cartera")
    mostrar_moduloA()

    st.markdown("---")

    # Ancla y Módulo B1
    st.markdown('<div id="modB1"></div>', unsafe_allow_html=True)
    st.markdown("## Módulo B1 – Impuestos y Saldo Neto")
    mostrar_moduloB1()

    st.markdown("---")

    # Ancla y Módulo B2
    st.markdown('<div id="modB2"></div>', unsafe_allow_html=True)
    st.markdown("## Módulo B2 – Proyección de Pensión")
    mostrar_moduloB2()

    st.markdown("---")

    # Ancla y Módulo C
    st.markdown('<div id="modC"></div>', unsafe_allow_html=True)
    st.markdown("## Módulo C – Bonos")
    mostrar_moduloC()

    # No usamos query params; el comportamiento de scroll se logra con enlaces hash

    # Inyectar script para interceptar clicks en enlaces hash y hacer scroll
    # sin cambiar la URL (evita que Streamlit haga manejo interno de query params)
    scroll_js = """
    <script>
    document.addEventListener('click', function(e){
        try{
            const target = e.target;
            if(!target) return;
            if(target.tagName === 'A' && target.getAttribute('href') && target.getAttribute('href').startsWith('#mod')){
                e.preventDefault();
                const id = target.getAttribute('href').substring(1);
                const el = document.getElementById(id);
                if(el){ el.scrollIntoView({behavior:'smooth', block:'start'}); }
                // remove any hash so Streamlit doesn't react to it
                history.replaceState(null, '', window.location.pathname + window.location.search);
            }
        }catch(err){console.log(err)}
    });
    </script>
    """
    st.markdown(scroll_js, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
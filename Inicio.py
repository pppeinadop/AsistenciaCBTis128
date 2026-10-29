import streamlit as st

from demo_data import DEMO_GROUPS, DEMO_STUDENTS


st.set_page_config(
    page_title="Asistencia CBTis 128",
    page_icon="📚",
    layout="wide",
)

st.title("Inicio")
st.subheader("Asistencia escolar | CBTis 128")
st.write(
    "Una herramienta para organizar la asistencia escolar. "
    "Esta versión inicial funciona con información de demostración."
)

st.info(
    "Usa el menú de navegación para tomar asistencia, consultar alumnos, "
    "probar la importación de Excel o revisar los reportes."
)

col1, col2, col3 = st.columns(3)
col1.metric("Alumnos de ejemplo", len(DEMO_STUDENTS))
col2.metric("Grupos disponibles", len(DEMO_GROUPS))
col3.metric("Almacenamiento de asistencia", "Supabase")

st.subheader("Acerca de esta versión")
st.markdown(
    """
    - **Tomar asistencia:** inicia sesión, marca a cada alumno y guarda el pase de lista en Supabase.
    - **Alumnos:** consulta una lista ficticia de ejemplo.
    - **Importar Excel:** carga un archivo para ver una vista previa, sin guardarlo.
    - **Reportes:** muestra indicadores ilustrativos basados en los datos de ejemplo.
    """
)
st.warning(
    "La lista es ficticia. Configura Supabase y carga un padrón autorizado antes "
    "de usar datos reales de estudiantes."
)

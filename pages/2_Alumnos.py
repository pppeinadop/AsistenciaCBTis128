import pandas as pd
import streamlit as st

from demo_data import DEMO_STUDENTS


st.set_page_config(page_title="Alumnos | CBTis 128", page_icon="👩‍🎓", layout="wide")
st.title("Alumnos")
st.write("Consulta el listado ficticio incluido para esta demostración.")
st.info("La lista no contiene datos reales y todavía no se conecta a una base de datos.")

students = pd.DataFrame(DEMO_STUDENTS).rename(
    columns={"matricula": "Matrícula", "nombre": "Nombre", "grupo": "Grupo"}
)
st.dataframe(students, hide_index=True, use_container_width=True)

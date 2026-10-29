from datetime import date

import streamlit as st

from demo_data import DEMO_STUDENTS


st.set_page_config(page_title="Tomar asistencia | CBTis 128", page_icon="📝", layout="wide")
st.title("Tomar asistencia")
st.caption("Marca el estado de cada alumno para la fecha seleccionada.")
st.warning(
    "Datos de demostración: los cambios solo se mantienen temporalmente en esta "
    "sesión de Streamlit. No se guardan en una base de datos."
)

col_date, col_group = st.columns(2)
selected_date = col_date.date_input("Fecha", value=date.today())
selected_group = col_group.selectbox("Grupo", ["2A"])
session_key = f"asistencia_{selected_date.isoformat()}_{selected_group}"

if session_key not in st.session_state:
    st.session_state[session_key] = {}

st.divider()
present_count = sum(
    status == "Presente" for status in st.session_state[session_key].values()
)
absent_count = sum(
    status == "Falta" for status in st.session_state[session_key].values()
)
metric_present, metric_absent = st.columns(2)
metric_present.metric("Presentes", present_count)
metric_absent.metric("Faltas", absent_count)

for student in DEMO_STUDENTS:
    row = st.columns([3, 1, 1, 1])
    row[0].write(f"**{student['nombre']}**  \n`{student['matricula']}`")
    current_status = st.session_state[session_key].get(student["matricula"], "Sin marcar")
    row[1].write(f"Estado: **{current_status}**")
    if row[2].button("Presente", key=f"presente_{session_key}_{student['matricula']}"):
        st.session_state[session_key][student["matricula"]] = "Presente"
        st.rerun()
    if row[3].button("Falta", key=f"falta_{session_key}_{student['matricula']}"):
        st.session_state[session_key][student["matricula"]] = "Falta"
        st.rerun()

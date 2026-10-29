import pandas as pd
import streamlit as st

from demo_data import DEMO_STUDENTS


st.set_page_config(page_title="Reportes | CBTis 128", page_icon="📊", layout="wide")
st.title("Reportes")
st.write("Indicadores ilustrativos para mostrar la estructura inicial de los reportes.")
st.info("Estos resultados son ficticios y no representan asistencia real.")

total_students = len(DEMO_STUDENTS)
present_students = 4
absent_students = total_students - present_students
attendance_rate = round(present_students / total_students * 100)

col_total, col_present, col_absent, col_rate = st.columns(4)
col_total.metric("Alumnos", total_students)
col_present.metric("Presentes", present_students)
col_absent.metric("Faltas", absent_students)
col_rate.metric("Asistencia de ejemplo", f"{attendance_rate}%")

report = pd.DataFrame(
    {
        "Grupo": ["2A"],
        "Presentes": [present_students],
        "Faltas": [absent_students],
        "Porcentaje de asistencia": [attendance_rate],
    }
)
st.subheader("Resumen por grupo")
st.dataframe(report, hide_index=True, use_container_width=True)

from datetime import date

import httpx
import streamlit as st
from postgrest.exceptions import APIError
from supabase_auth.errors import AuthApiError

from attendance_store import (
    DatabaseConfigurationError,
    create_supabase_client,
    load_attendance,
    save_attendance,
)
from demo_data import DEMO_GROUPS, DEMO_STUDENTS


st.set_page_config(page_title="Tomar asistencia | CBTis 128", page_icon="📝", layout="wide")
st.title("Tomar asistencia")
st.caption("Pase de lista individual. Usa los botones de abajo para avanzar o regresar.")
st.warning(
    "La lista contiene alumnos ficticios de demostración. No captures información "
    "real hasta contar con el padrón autorizado."
)


def sign_in() -> None:
    try:
        client = create_supabase_client()
    except DatabaseConfigurationError as error:
        st.error(str(error))
        st.info(
            "El administrador debe configurar SUPABASE_URL y SUPABASE_ANON_KEY "
            "en Streamlit Cloud antes de iniciar sesión."
        )
        return

    with st.form("attendance_login"):
        email = st.text_input("Correo autorizado", autocomplete="email")
        password = st.text_input("Contraseña", type="password", autocomplete="current-password")
        submitted = st.form_submit_button("Iniciar sesión", type="primary")

    if submitted:
        try:
            response = client.auth.sign_in_with_password(
                {"email": email.strip(), "password": password}
            )
        except AuthApiError:
            st.error("No se pudo iniciar sesión. Verifica tus datos e inténtalo de nuevo.")
            return
        except httpx.HTTPError as error:
            st.error(f"No se pudo conectar con Supabase: {error}")
            return

        st.session_state["attendance_client"] = client
        st.session_state["attendance_user_email"] = response.user.email
        st.rerun()


if "attendance_client" not in st.session_state:
    st.subheader("Acceso para personal autorizado")
    st.write("Inicia sesión con una cuenta creada por el administrador para tomar asistencia.")
    sign_in()
    st.stop()

client = st.session_state["attendance_client"]
header_col, logout_col = st.columns([4, 1])
header_col.caption(f"Sesión iniciada: {st.session_state['attendance_user_email']}")
if logout_col.button("Cerrar sesión", use_container_width=True):
    try:
        client.auth.sign_out()
    except (AuthApiError, httpx.HTTPError) as error:
        st.error(f"No se pudo cerrar la sesión con Supabase: {error}")
        st.stop()
    del st.session_state["attendance_client"]
    del st.session_state["attendance_user_email"]
    st.session_state.pop("attendance_active_key", None)
    st.rerun()

date_col, group_col, start_col = st.columns([2, 2, 1])
selected_date = date_col.date_input("Fecha", value=date.today())
selected_group = group_col.selectbox("Grupo", DEMO_GROUPS)
start_clicked = start_col.button("Iniciar lista", type="primary", use_container_width=True)

session_key = f"{selected_date.isoformat()}_{selected_group}"
students = [student for student in DEMO_STUDENTS if student["grupo"] == selected_group]
progress_key = f"attendance_progress_{session_key}"

if start_clicked:
    try:
        saved_records = load_attendance(client, selected_date, selected_group)
    except (APIError, httpx.HTTPError) as error:
        st.error(f"No se pudo cargar la asistencia guardada: {error}")
        st.stop()

    st.session_state[progress_key] = {
        "index": 0,
        "statuses": {
            record["student_registration"]: record["status"]
            for record in saved_records
        },
        "finished": False,
    }
    st.session_state["attendance_active_key"] = session_key
    st.rerun()

if st.session_state.get("attendance_active_key") != session_key:
    st.info("Selecciona la fecha y el grupo, luego pulsa «Iniciar lista».")
    st.stop()

progress = st.session_state[progress_key]
if progress["finished"]:
    present_count = sum(status == "Presente" for status in progress["statuses"].values())
    absent_count = sum(status == "Falta" for status in progress["statuses"].values())
    st.success("La asistencia se guardó correctamente en la base de datos.")
    present_col, absent_col = st.columns(2)
    present_col.metric("Presentes", present_count)
    absent_col.metric("Faltas", absent_count)
    if st.button("Iniciar otra lista"):
        st.session_state.pop(progress_key, None)
        st.session_state.pop("attendance_active_key", None)
        st.rerun()
    st.stop()

student_index = progress["index"]
student = students[student_index]
student_status = progress["statuses"].get(student["matricula"], "Sin marcar")

st.progress((student_index + 1) / len(students))
st.caption(f"Alumno {student_index + 1} de {len(students)}")
st.markdown(f"# {student['nombre']}")
st.markdown(f"### Matrícula: `{student['matricula']}` · Grupo {selected_group}")

if student_status == "Presente":
    st.success("Estado actual: Presente")
elif student_status == "Falta":
    st.error("Estado actual: Falta")
else:
    st.info("Estado actual: Sin marcar")

st.markdown(
    """
    <style>
    .st-key-attendance-actions button {
        min-height: 5rem;
        font-size: 1.35rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
with st.container(key="attendance-actions"):
    present_col, absent_col = st.columns(2)
    if present_col.button("✓  PRESENTE", type="primary", use_container_width=True):
        progress["statuses"][student["matricula"]] = "Presente"
        st.rerun()
    if absent_col.button("✕  FALTA", use_container_width=True):
        progress["statuses"][student["matricula"]] = "Falta"
        st.rerun()

st.divider()
back_col, next_col = st.columns(2)
if back_col.button(
    "←  Regresar",
    disabled=student_index == 0,
    use_container_width=True,
):
    progress["index"] -= 1
    st.rerun()

if student_index < len(students) - 1:
    if next_col.button("Avanzar  →", type="primary", use_container_width=True):
        progress["index"] += 1
        st.rerun()
else:
    unmarked_count = sum(
        student["matricula"] not in progress["statuses"] for student in students
    )
    if unmarked_count:
        st.warning(
            f"Faltan {unmarked_count} alumno(s) por marcar. Regresa y completa "
            "la lista antes de finalizar."
        )
    if next_col.button(
        "Finalizar y guardar",
        type="primary",
        disabled=unmarked_count > 0,
        use_container_width=True,
    ):
        try:
            save_attendance(
                client,
                selected_date,
                selected_group,
                students,
                progress["statuses"],
            )
        except (APIError, httpx.HTTPError) as error:
            st.error(f"No se pudo guardar la asistencia. No se confirmó el guardado: {error}")
        else:
            progress["finished"] = True
            st.rerun()

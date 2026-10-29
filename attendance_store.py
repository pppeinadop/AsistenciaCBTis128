from datetime import date

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from supabase import Client, create_client


class DatabaseConfigurationError(RuntimeError):
    pass


def create_supabase_client() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        anon_key = st.secrets["SUPABASE_ANON_KEY"]
    except (KeyError, StreamlitSecretNotFoundError) as error:
        raise DatabaseConfigurationError(
            "La conexión segura con Supabase todavía no está configurada."
        ) from error

    if not url or not anon_key:
        raise DatabaseConfigurationError(
            "SUPABASE_URL y SUPABASE_ANON_KEY deben tener valores en Streamlit Secrets."
        )

    return create_client(url, anon_key)


def load_attendance(client: Client, attendance_date: date, group_name: str) -> list[dict]:
    response = (
        client.table("attendance_records")
        .select("student_registration,status")
        .eq("attendance_date", attendance_date.isoformat())
        .eq("group_name", group_name)
        .execute()
    )
    return response.data


def save_attendance(
    client: Client,
    attendance_date: date,
    group_name: str,
    students: list[dict],
    statuses: dict[str, str],
) -> list[dict]:
    records = [
        {
            "attendance_date": attendance_date.isoformat(),
            "group_name": group_name,
            "student_registration": student["matricula"],
            "student_name": student["nombre"],
            "status": statuses[student["matricula"]],
        }
        for student in students
    ]
    response = (
        client.table("attendance_records")
        .upsert(
            records,
            on_conflict="attendance_date,group_name,student_registration",
        )
        .execute()
    )
    return response.data

import pandas as pd
import streamlit as st


st.set_page_config(page_title="Importar Excel | CBTis 128", page_icon="📥", layout="wide")
st.title("Importar Excel")
st.write("Carga un archivo `.xlsx` para revisar una vista previa de su contenido.")
st.warning(
    "La carga es solo de demostración: el archivo no se guarda ni se importa "
    "permanentemente. Evita usar información personal real."
)

uploaded_file = st.file_uploader("Selecciona un archivo Excel", type=["xlsx"])
if uploaded_file is not None:
    try:
        spreadsheet = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Hoja", spreadsheet.sheet_names)
        preview = pd.read_excel(spreadsheet, sheet_name=sheet_name)
    except (ValueError, OSError, ImportError) as error:
        st.error(f"No se pudo leer el archivo. Verifica que sea un Excel válido. ({error})")
    else:
        st.success(f"Vista previa de la hoja «{sheet_name}»")
        st.caption(
            f"{len(preview)} filas y {len(preview.columns)} columnas. "
            "Este contenido solo está disponible mientras dure la sesión."
        )
        st.dataframe(preview.head(20), hide_index=True, use_container_width=True)

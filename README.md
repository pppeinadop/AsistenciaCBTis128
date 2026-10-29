# Asistencia CBTis 128

Aplicación web inicial de asistencia escolar construida con Python y Streamlit.
La interfaz está en español y todas las personas y cifras que aparecen son
ficticias. Esta versión no usa base de datos ni guarda información de forma
permanente.

## Requisitos

- Python 3.9 o posterior
- pip

## Ejecutar localmente

En Windows, abre PowerShell desde la carpeta del proyecto y ejecuta:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run Inicio.py
```

Streamlit abrirá la aplicación en el navegador; normalmente estará disponible
en <http://localhost:8501>. Si PowerShell bloquea la activación del entorno,
puedes ejecutar `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
y luego `.\.venv\Scripts\python.exe -m streamlit run Inicio.py`.

## Páginas

- **Inicio:** resumen de la aplicación y sus limitaciones actuales.
- **Tomar asistencia:** botones para marcar presente o falta con datos de ejemplo.
  Los cambios viven temporalmente en la sesión de Streamlit y no se guardan en
  una base de datos.
- **Alumnos:** listado ficticio de ejemplo.
- **Importar Excel:** vista previa de un archivo `.xlsx`, sin almacenamiento
  permanente.
- **Reportes:** resumen ilustrativo basado en datos ficticios.

La navegación entre páginas aparece en el menú lateral de Streamlit. No cargues
información personal real ni secretos en esta versión.
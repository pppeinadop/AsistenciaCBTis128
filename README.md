# Asistencia CBTis 128

Aplicación web de asistencia escolar construida con Python y Streamlit. La
interfaz está en español; el padrón incluido es ficticio y solo sirve para
probar el flujo.

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
  Requiere iniciar sesión con una cuenta autorizada de Supabase. Se muestra un
  alumno a la vez; permite avanzar, regresar y corregir marcas antes de
  finalizar. Al finalizar se guardan todos los registros del grupo y fecha en
  Supabase. Se puede volver a iniciar esa lista y corregir registros guardados.
- **Alumnos:** listado ficticio de ejemplo.
- **Importar Excel:** vista previa de un archivo `.xlsx`, sin almacenamiento
  permanente.
- **Reportes:** resumen ilustrativo basado en datos ficticios.

La navegación entre páginas aparece en el menú lateral de Streamlit. No uses
datos reales de estudiantes hasta cargar un padrón autorizado y configurar los
controles de acceso de la institución.

## Configurar Supabase para guardar asistencias

1. Crea un proyecto en [Supabase](https://supabase.com/) y abre **SQL Editor**.
2. Ejecuta el contenido de `supabase_setup.sql` para crear la tabla y sus
   políticas. Solo usuarios autenticados podrán consultar o modificar
   asistencias.
3. En Supabase, crea una cuenta de acceso para cada integrante autorizado del
   personal desde **Authentication → Users**.
4. Copia la URL del proyecto y la clave **anon/public** desde **Project
   Settings → API**. No uses ni compartas la clave `service_role`.
5. En Streamlit Community Cloud, abre la app **Manage app → Settings → Secrets**
   y agrega:

   ```toml
   SUPABASE_URL = "https://tu-proyecto.supabase.co"
   SUPABASE_ANON_KEY = "tu-clave-anon"
   ```

6. Guarda los secretos y reinicia la app. Las cuentas creadas en Supabase
   podrán iniciar sesión en la página **Tomar asistencia**.

El inicio de sesión protege la página de asistencia; las demás páginas de
demostración siguen siendo públicas.

Para desarrollo local, crea `.streamlit/secrets.toml` con las mismas dos claves;
este archivo está ignorado por Git y no debe compartirse.
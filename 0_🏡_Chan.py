"""Página de inicio para el proyecto "Uëzi yo dyaxü"."""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Uëzi yo dyaxü",
    page_icon="📖",
    layout="centered",
)


# ---------------------------------------------------------------------------
# Contenido de la Home
# ---------------------------------------------------------------------------

st.title("📖 Uëzi yo dyaxü")

st.markdown("""
Bienvenido a la plataforma interactiva del libro **"Uëzi yo dyaxü"** para la enseñanza de la lengua mazahua de **Ana Elvia Paulino Escamilla**.

Este espacio está diseñado para complementar la lectura del libro y ayudar en el aprendizaje de la lengua a través de actividades interactivas.
""")

st.image("img/portada.png")

st.divider()

st.subheader("🧙🏼‍♀️ Explora el sitio")

st.markdown("""
En el menú lateral, encontrarás diferentes secciones. Por ahora, puedes probar:

- **Sopita**: Un juego interactivo para practicar el vocabulario y reconocer las letras y grafías de la lengua.
""")

st.info("💡 ¡Utiliza el menú de la izquierda para navegar entre las páginas!")

# Puedes agregar más información aquí, como una descripción del libro,
# objetivos del proyecto, o enlaces externos.
st.caption(f"Hecho con :heart: por [Comunidad Elotl](https://elotl.mx)")

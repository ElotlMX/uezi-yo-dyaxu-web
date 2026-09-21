"""Página de inicio para el proyecto "Uëzi yo dyaxü"."""

import streamlit as st

st.set_page_config(
    page_title="Uëzi yo dyaxü jñatrjo",
    page_icon="📖",
    layout="centered",
)

st.title("📖 Uëzi yo dyaxü jñatrjo")

st.markdown("""
Bienvenido a la plataforma interactiva del libro **"Uëzi yo dyaxü jñatrjo"** para la enseñanza de la lengua mazahua de **Ana Elvia Paulino Escamilla**.

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

st.caption("Hecho con :heart: por [Comunidad Elotl](https://elotl.mx)")

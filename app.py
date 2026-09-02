"""Sopa de letras (word search) — página interactiva para el libro
"Uëzi yo dyaxü".

Para ejecutarla localmente:
    uv run streamlit run app.py
"""

from __future__ import annotations

import random
import string
from dataclasses import dataclass

import streamlit as st

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Sopa de letras — Uëzi yo dyaxü",
    page_icon="📖",
    layout="centered",
)

# TODO: Lista de palabras inexitentes. Toca actualizar con palabras reales
# Elegir palabras cortas para que quepan bien en el tablero.
DEFAULT_WORDS: list[str] = [
    "DYAXU",
    "UEZI",
    "TATA",
    "NANA",
    "JIMI",
    "EJE",
    "NI",
    "KUA",
    "ÑU",
    "MBO",
    "JÑU",
    "TSA",
]

GRID_SIZE = 12
# TODO: Agregar letras válidas
LETTERS = string.ascii_uppercase + "Ñ"


# ---------------------------------------------------------------------------
# Generación del tablero
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Placement:
    word: str
    cells: list[tuple[int, int]]  # coordenadas (fila, columna) en orden de lectura

    @property
    def start(self) -> tuple[int, int]:
        return self.cells[0]

    @property
    def end(self) -> tuple[int, int]:
        return self.cells[-1]


# 8 direcciones posibles: (dr, dc)
DIRECTIONS: list[tuple[int, int]] = [
    (0, 1),  # → derecha
    (1, 0),  # ↓ abajo
    (1, 1),  # ↘ diagonal
    (-1, 1),  # ↗ diagonal
    (0, -1),  # ← izquierda
    (1, -1),  # ↙ diagonal
    (-1, 0),  # ↑ arriba
    (-1, -1),  # ↖ diagonal
]


def _fits(grid: list[list[str]], word: str, r: int, c: int, dr: int, dc: int) -> bool:
    """Verifica que `word` cabe en la posición y dirección indicadas."""
    n = len(grid)
    for i, ch in enumerate(word):
        rr, cc = r + dr * i, c + dc * i
        if not (0 <= rr < n and 0 <= cc < n):
            return False
        current = grid[rr][cc]
        if current != "" and current != ch:
            return False
    return True


def generate_grid(
    words: list[str], size: int, rng: random.Random
) -> tuple[list[list[str]], list[Placement], list[str]]:
    """Intenta colocar cada palabra en una posición/dirección aleatoria.

    Las palabras que no quepan se devuelven en `unplaced` para que la UI
    las muestre al usuario.
    """
    grid: list[list[str]] = [["" for _ in range(size)] for _ in range(size)]
    placements: list[Placement] = []
    unplaced: list[str] = []

    # Ordena de más larga a más corta para mejorar el encaje.
    sorted_words = sorted(
        set(w.strip().upper() for w in words if w.strip()), key=len, reverse=True
    )

    for word in sorted_words:
        if not word:
            continue
        # Filtra letras no soportadas para evitar problemas con el tablero.
        if any(ch not in LETTERS for ch in word):
            unplaced.append(word)
            continue

        placed = False
        # Mezcla direcciones y posiciones para variedad.
        directions = DIRECTIONS[:]
        rng.shuffle(directions)
        positions = [(r, c) for r in range(size) for c in range(size)]
        rng.shuffle(positions)

        for dr, dc in directions:
            if placed:
                break
            for r, c in positions:
                if _fits(grid, word, r, c, dr, dc):
                    cells: list[tuple[int, int]] = []
                    for i, ch in enumerate(word):
                        rr, cc = r + dr * i, c + dc * i
                        grid[rr][cc] = ch
                        cells.append((rr, cc))
                    placements.append(Placement(word=word, cells=cells))
                    placed = True
                    break

        if not placed:
            unplaced.append(word)

    # Rellena los huecos vacíos con letras aleatorias.
    for r in range(size):
        for c in range(size):
            if grid[r][c] == "":
                grid[r][c] = rng.choice(string.ascii_uppercase)

    return grid, placements, unplaced


# ---------------------------------------------------------------------------
# Estado de la sesión
# ---------------------------------------------------------------------------


def _new_puzzle(words: list[str], size: int) -> None:
    seed = random.randint(0, 10_000_000)
    rng = random.Random(seed)
    grid, placements, unplaced = generate_grid(words, size, rng)
    st.session_state.grid = grid
    st.session_state.placements = placements
    st.session_state.unplaced = unplaced
    st.session_state.found_words = set()
    st.session_state.selection_start: tuple[int, int] | None = None
    st.session_state.last_click: tuple[int, int] | None = None
    st.session_state.seed = seed


def _ensure_state() -> None:
    if "grid" not in st.session_state:
        _new_puzzle(DEFAULT_WORDS, GRID_SIZE)


_ensure_state()


# ---------------------------------------------------------------------------
# Helpers para consultar colocaciones
# ---------------------------------------------------------------------------


def _is_straight_line(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int] | None:
    """Devuelve (dr, dc) si a→b es una línea recta válida, si no None.

    Acepta horizontales, verticales y diagonales a 45°.
    """
    dr = b[0] - a[0]
    dc = b[1] - a[1]
    n = max(abs(dr), abs(dc))
    if n == 0:
        return None
    if dr == 0:
        return (0, 1 if dc > 0 else -1)
    if dc == 0:
        return (1 if dr > 0 else -1, 0)
    if abs(dr) == abs(dc):
        return (1 if dr > 0 else -1, 1 if dc > 0 else -1)
    return None


def _cells_between(
    a: tuple[int, int], b: tuple[int, int], step: tuple[int, int]
) -> list[tuple[int, int]]:
    dr, dc = step
    cells = []
    r, c = a
    while (r, c) != b:
        cells.append((r, c))
        r += dr
        c += dc
    cells.append(b)
    return cells


def _find_placement(
    cells: list[tuple[int, int]], placements: list[Placement]
) -> Placement | None:
    cell_set = set(cells)
    for p in placements:
        if set(p.cells) == cell_set:
            return p
    return None


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------


st.title("📖 Sopa de letras")
st.caption(
    "Encuentra las palabras escondidas en el tablero. Haz clic en la primera "
    "y última letra de cada palabra. Las palabras pueden ir en horizontal, "
    "vertical o en diagonal."
)

# --- Barra lateral con controles ------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuración")

    custom_words = st.text_area(
        "Palabras (una por línea)",
        value="\n".join(DEFAULT_WORDS),
        height=200,
        help="Edita la lista para usar tu propio vocabulario.",
    )

    if st.button("🔄 Nueva sopa", use_container_width=True):
        words = [w for w in custom_words.splitlines() if w.strip()]
        if not words:
            st.warning("Agrega al menos una palabra.")
        else:
            _new_puzzle(words, GRID_SIZE)
            st.rerun()

    st.divider()
    if st.button("🧹 Limpiar selección", use_container_width=True):
        st.session_state.selection_start = None
        st.session_state.last_click = None
        st.rerun()

    st.divider()
    found = len(st.session_state.found_words)
    total = len(st.session_state.placements)
    st.metric("Palabras encontradas", f"{found} / {total}")

# --- Avisos de palabras no colocadas -------------------------------------------
if st.session_state.unplaced:
    st.warning(
        "Estas palabras no cupieron en el tablero y no aparecen: "
        + ", ".join(st.session_state.unplaced)
    )

# --- Tablero --------------------------------------------------------------------
grid: list[list[str]] = st.session_state.grid
placements: list[Placement] = st.session_state.placements
found_words: set[str] = st.session_state.found_words

# Conjunto de celdas que pertenecen a palabras ya encontradas, para resaltarlas.
found_cells: set[tuple[int, int]] = set()
for p in placements:
    if p.word in found_words:
        found_cells.update(p.cells)

# Selección actual (rango entre el primer clic y el último).
selection_cells: set[tuple[int, int]] = set()
start = st.session_state.selection_start
last = st.session_state.last_click
if start is not None and last is not None and start != last:
    step = _is_straight_line(start, last)
    if step is not None:
        selection_cells = set(_cells_between(start, last, step))


def _cell_label(r: int, c: int) -> str:
    return grid[r][c]


def _cell_help(r: int, c: int) -> str:
    return f"({r + 1},{c + 1})"


def _handle_click(r: int, c: int) -> None:
    pos = (r, c)
    if st.session_state.selection_start is None:
        st.session_state.selection_start = pos
        st.session_state.last_click = pos
        return

    if pos == st.session_state.selection_start:
        # Segundo clic en la misma celda: cancela.
        st.session_state.selection_start = None
        st.session_state.last_click = None
        return

    step = _is_straight_line(st.session_state.selection_start, pos)
    if step is None:
        # No es una línea recta: reinicia la selección desde esta celda.
        st.session_state.selection_start = pos
        st.session_state.last_click = pos
        return

    cells = _cells_between(st.session_state.selection_start, pos, step)
    placement = _find_placement(cells, placements)
    if placement is not None and placement.word not in found_words:
        st.session_state.found_words.add(placement.word)

    # Tras validar, limpiamos para empezar otra palabra.
    st.session_state.selection_start = None
    st.session_state.last_click = None


# Render del tablero como una cuadrícula de botones usando columnas.
size = len(grid)
# Cada fila es un bloque vertical; dentro usamos columnas de ancho 1.
for r in range(size):
    cols = st.columns(size, gap="small")
    for c in range(size):
        is_found = (r, c) in found_cells
        is_selected = (r, c) in selection_cells
        is_start = st.session_state.selection_start == (r, c)

        label = _cell_label(r, c)
        if is_found:
            label = f"✅{label}"
        elif is_selected or is_start:
            label = f"🔎{label}"

        button_type = "primary" if (is_selected or is_start) else "secondary"
        if cols[c].button(
            label,
            key=f"cell-{r}-{c}",
            help=_cell_help(r, c),
            use_container_width=True,
            type=button_type,
        ):
            _handle_click(r, c)
            st.rerun()

st.divider()

# --- Lista de palabras ----------------------------------------------------------
st.subheader("📝 Palabras")

cols = st.columns(3)
for i, p in enumerate(placements):
    with cols[i % 3]:
        mark = "✅" if p.word in found_words else "⬜"
        st.write(f"{mark} **{p.word}**")

if found_words == {p.word for p in placements} and placements:
    st.balloons()
    st.success("🎉 ¡Encontraste todas las palabras!")

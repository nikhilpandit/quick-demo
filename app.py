import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="Conway's Game of Life", page_icon="🟩")

# --- Settings ---
GRID_SIZE = 30
UPDATE_INTERVAL = 0.2  # seconds

# --- Helpers ---
def next_generation(grid):
    neighbors = sum(np.roll(np.roll(grid, i, 0), j, 1)
                    for i in (-1, 0, 1) for j in (-1, 0, 1)
                    if (i != 0 or j != 0))
    return (neighbors == 3) | (grid & (neighbors == 2))

def toggle_cell(grid, row, col):
    grid[row, col] = not grid[row, col]
    return grid

# --- Session State ---
def init_state():
    st.session_state.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    st.session_state.running = False
    st.session_state.generation = 0
    st.session_state.last_update = time.time()

if "grid" not in st.session_state:
    init_state()

# --- UI ---
st.title("🟩 Conway's Game of Life")
st.write("Click on the grid to toggle cells. Press Start to run the simulation.")

col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("Start"):
        st.session_state.running = True
with col2:
    if st.button("Pause"):
        st.session_state.running = False
with col3:
    if st.button("Reset"):
        init_state()

st.write(f"Generation: {st.session_state.generation}")

# --- Interactive Grid ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(st.session_state.grid, cmap="Greys", vmin=0, vmax=1)
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()

# Handle clicks on the grid
if not st.session_state.running:
    # Get click coordinates from Streamlit
    click_data = st.pyplot(fig, use_container_width=True)
    if click_data and isinstance(click_data, dict) and "x" in click_data and "y" in click_data:
        # Convert click coordinates to grid coordinates
        x = int(click_data["x"] * GRID_SIZE)
        y = int(click_data["y"] * GRID_SIZE)
        if 0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE:
            st.session_state.grid = toggle_cell(st.session_state.grid, y, x)
            st.rerun()
else:
    st.pyplot(fig, use_container_width=True)

# --- Simulation Loop ---
if st.session_state.running:
    now = time.time()
    if now - st.session_state.last_update > UPDATE_INTERVAL:
        st.session_state.grid = next_generation(st.session_state.grid)
        st.session_state.generation += 1
        st.session_state.last_update = now
        st.rerun()

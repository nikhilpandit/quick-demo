import streamlit as st
import numpy as np
import random
import time
from matplotlib import pyplot as plt
from streamlit_keyup import keyup

st.set_page_config(page_title="Snake Game", page_icon="🐍")

# Game settings
BOARD_SIZE = 15
INITIAL_SNAKE = [(7, 7), (7, 6), (7, 5)]
INITIAL_DIRECTION = 'RIGHT'
DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

# Initialize session state
if 'snake' not in st.session_state:
    st.session_state.snake = INITIAL_SNAKE.copy()
    st.session_state.direction = INITIAL_DIRECTION
    st.session_state.food = (random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1))
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.last_move_time = time.time()

def place_food(snake):
    while True:
        food = (random.randint(0, BOARD_SIZE-1), random.randint(0, BOARD_SIZE-1))
        if food not in snake:
            return food

def move_snake():
    if st.session_state.game_over:
        return
    head = st.session_state.snake[0]
    delta = DIRECTIONS[st.session_state.direction]
    new_head = (head[0] + delta[0], head[1] + delta[1])
    # Check collisions
    if (
        new_head[0] < 0 or new_head[0] >= BOARD_SIZE or
        new_head[1] < 0 or new_head[1] >= BOARD_SIZE or
        new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        return
    st.session_state.snake = [new_head] + st.session_state.snake
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = place_food(st.session_state.snake)
    else:
        st.session_state.snake.pop()

def reset_game():
    st.session_state.snake = INITIAL_SNAKE.copy()
    st.session_state.direction = INITIAL_DIRECTION
    st.session_state.food = place_food(st.session_state.snake)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.last_move_time = time.time()

st.title("🐍 Snake Game")
st.write(f"Score: {st.session_state.score}")

# Keyboard controls
st.markdown(
    """
    <p><b>Tip:</b> Use your arrow keys to control the snake! (Click on the input box below, then use your keyboard.)</p>
    <p>If you haven't installed <code>streamlit-keyup</code>, run <code>pip install streamlit-keyup</code> in your terminal.</p>
    """,
    unsafe_allow_html=True
)
key_event = keyup("Use arrow keys here", key="snake_keypad")
if key_event:
    key = key_event.get("key")
    if key == "ArrowUp" and st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
    elif key == "ArrowDown" and st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
    elif key == "ArrowLeft" and st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
    elif key == "ArrowRight" and st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"

# Fallback: Button controls
col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
with col2:
    if st.button('⬆️', key='up') and st.session_state.direction != 'DOWN':
        st.session_state.direction = 'UP'
with col1:
    if st.button('⬅️', key='left') and st.session_state.direction != 'RIGHT':
        st.session_state.direction = 'LEFT'
with col3:
    if st.button('➡️', key='right') and st.session_state.direction != 'LEFT':
        st.session_state.direction = 'RIGHT'
with col4:
    if st.button('⬇️', key='down') and st.session_state.direction != 'UP':
        st.session_state.direction = 'DOWN'
with col5:
    if st.button('Restart'):
        reset_game()

# Move snake if not game over
if not st.session_state.game_over:
    # Simple timer for auto-move
    now = time.time()
    if now - st.session_state.last_move_time > 0.2:
        move_snake()
        st.session_state.last_move_time = now
        st.experimental_rerun()

# Draw board
board = np.zeros((BOARD_SIZE, BOARD_SIZE, 3), dtype=np.uint8)
for y, x in st.session_state.snake:
    board[y, x] = [0, 255, 0]  # Green for snake
fy, fx = st.session_state.food
board[fy, fx] = [255, 0, 0]    # Red for food

fig, ax = plt.subplots(figsize=(5, 5))
ax.imshow(board, interpolation='nearest')
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()
st.pyplot(fig)

if st.session_state.game_over:
    st.error(f"Game Over! Your score: {st.session_state.score}")
    if st.button('Play Again'):
        reset_game()

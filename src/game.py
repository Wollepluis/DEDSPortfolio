import pygame
import numpy as np
import random
import time

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 15, 15
CELL_SIZE = WIDTH // COLS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (180, 180, 255)

maze = [
    [0,1,0,0,0,1,0,1,0,0,1,0,0,1,0],
    [0,1,0,1,0,1,0,1,0,1,1,0,1,1,0],
    [0,0,0,1,0,0,0,1,0,0,0,0,1,0,0],
    [1,1,1,1,1,1,0,1,1,1,1,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,0,1,1,1,1,0],
    [0,1,0,0,0,0,0,0,1,0,0,0,0,1,0],
    [0,1,0,1,1,1,1,0,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
    [1,1,1,1,1,0,1,1,1,1,1,1,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,0,1,1,1,0],
    [0,1,0,0,0,0,0,0,0,1,0,0,0,1,0],
    [0,1,0,1,1,1,1,1,0,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
]

start = (0, 0)
goal = (14, 14)

actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # UP, DOWN, LEFT, RIGHT
q_table = np.zeros((ROWS, COLS, len(actions)))
alpha = 0.1
gamma = 0.9
epsilon = 0.1
episodes = 200  # verander dit voor langere training

def is_valid(pos):
    r, c = pos
    return 0 <= r < ROWS and 0 <= c < COLS and maze[r][c] == 0

def choose_action(state):
    if random.random() < epsilon:
        return random.randint(0, len(actions) - 1)
    else:
        return np.argmax(q_table[state[0], state[1]])

def draw_maze(screen, agent_pos):
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    pygame.draw.rect(screen, GREEN, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLUE, (agent_pos[1]*CELL_SIZE, agent_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

def draw_episode_path(screen, path):
    for pos in path:
        if pos == start or pos == goal:
            continue
        rect = pygame.Rect(pos[1]*CELL_SIZE, pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREY, rect)
    pygame.draw.rect(screen, GREEN, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.update()

def train(screen):
    for episode in range(episodes):
        state = start
        path = [state]
        while state != goal:
            action_idx = choose_action(state)
            dr, dc = actions[action_idx]
            next_state = (state[0] + dr, state[1] + dc)
            if not is_valid(next_state):
                next_state = state
                reward = -1
            elif next_state == goal:
                reward = 10
            else:
                reward = -0.1

            old_value = q_table[state[0], state[1], action_idx]
            next_max = np.max(q_table[next_state[0], next_state[1]])
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state[0], state[1], action_idx] = new_value

            state = next_state
            path.append(state)

        # Teken pad na elke episode
        draw_maze(screen, state)
        draw_episode_path(screen, path)
        pygame.event.pump()
        pygame.display.set_caption(f"Episode {episode+1}/{episodes}")
        time.sleep(0.5)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Q-Learning Maze Solver")

    train(screen)

    running = True
    state = start
    while running:
        draw_maze(screen, state)
        pygame.event.pump()
        time.sleep(0.2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        action_idx = np.argmax(q_table[state[0], state[1]])
        dr, dc = actions[action_idx]
        next_state = (state[0] + dr, state[1] + dc)
        if not is_valid(next_state):
            next_state = state
        state = next_state

        if state == goal:
            draw_maze(screen, state)
            time.sleep(2)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()

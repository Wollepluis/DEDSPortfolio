import random
import pgzrun 

# Opzetten van de tilemap
TILE_SIZE = 32
WIDTH = TILE_SIZE * 21
HEIGHT = TILE_SIZE * 21 + 120

# Tile types gedefinieerd met de index van de array: 0=empty, 1=muur, 2=goal
tiles = ['empty', 'wall', 'goal']

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Actor die begint op positie (1, 1) in de maze
player = Actor('oelewapper', anchor=(0, 0), pos=(1 * TILE_SIZE, 1 * TILE_SIZE))

# Info om de trainings-data bij te houden
episode = 0
total_reward = 0
last_td_error = 0 # Verschil tussen de verwachte waarde van een actie & de werkelijke waarde na die actie
last_q_value = 0

# Het tekenen van de maze-game inclusief trainingsdata info
def draw():
    screen.clear()
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            x = column * TILE_SIZE
            y = row * TILE_SIZE + 120
            tile = tiles[maze[row][column]]
            screen.blit(tile, (x, y))

    player.draw()

    info = [
        f"Episode: {episode}",
        f"Total reward: {total_reward:.2f}",
        f"TD Error: {last_td_error:.4f}",
        f"Q_value: {last_q_value:.4f}",
        f"Oelewapper pos: ({get_state()})"
    ]

    for i, line in enumerate(info):
        screen.draw.text(line, (10, 10 + i * 20), color="white", fontsize=20)

# huidige positie van de oelewapper opvragen
def get_state():
    return (int(player.y / TILE_SIZE), int(player.x / TILE_SIZE))

# Actie kiezen met ε-greedy startegy
actions = [0, 1, 2, 3]
def choose_action(state):
    if random.random() < epsilon or state not in Q:
        return random.choice(actions)   # willekeurige actie kiezen
    return max(Q[state], key=Q[state].get)  # Kies de beste actie

# Past een actie toe en berekent de beloning
def take_action(state, action):
    row, col = state
    new_row, new_col = row, col

    # Actie uitvoeren
    if action == 0: new_row -= 1     # omhoog
    elif action == 1: new_row += 1   # omlaag
    elif action == 2: new_col -= 1   # links
    elif action == 3: new_col += 1   # rechts

    return calculate_reward(new_row, new_col,state)

# Q-learning implementatie
training = False

epsilon = 0.1   # Kans om een willekeurige actie te kiezen (exploratie). 10% kans om een willekeurige actie te kiezen
alpha = 0.1     # Leersnelheid
gamma = 0.9     # Discount factor (Hoe belangrijk zijn toekomstige beloningen)

Q = {} # Q-tabel, waarin de waarde van elke actie per toestand opslaan

# Beloning berekenen
def calculate_reward(new_row, new_col, old_state):
    if maze[new_row][new_col] == 1:
        return old_state, -5            # Tegen de muur = -5
    elif maze[new_row][new_col] == 2:
        return (new_row, new_col), 10   # Doel bereikt = +10
    else:
        return (new_row, new_col), -1   # Geldige stap = -1
        
def update_q_value(state, action, reward, next_state):
    global last_td_error, last_q_value, total_reward
    if state not in Q:
        Q[state] = {a: 0 for a in actions}
    if next_state not in Q:
        Q[next_state] = {a: 0 for a in actions}

    old_q = Q[state][action]
    best_next = max(Q[next_state].values())
    td_error = reward + gamma * best_next - old_q
    Q[state][action] = old_q + alpha * td_error

    last_td_error = td_error
    last_q_value = Q[state][action]
    total_reward += reward

# current_state = None
# steps = 0
# max_steps = 500

# def train_step():
#     global current_state, episode, steps, total_reward

#     if current_state is None:
#         player.x, player.y = TILE_SIZE, TILE_SIZE
#         current_state = get_state()
#         steps = 0
#         total_reward = 0

#     action = choose_action(current_state)
#     next_state, reward = take_action(current_state, action)
#     update_q_value(current_state, action, reward, next_state)

#     player.x = next_state[1] * TILE_SIZE
#     player.y = next_state[0] * TILE_SIZE + 120
#     current_state = next_state
#     steps += 1

#     # Stop en reset als doel bereikt is of teveel stappen
#     if maze[current_state[0]][current_state[1]] == 2 or steps >= max_steps:
#         episode += 1
#         current_state = None  # Episode opnieuw starten

# clock.schedule_interval(train_step, 0.001)

def train_episode():
    player.x, player.y = TILE_SIZE, TILE_SIZE  # terug naar startpositie
    state = get_state()
    steps = 0
    while steps < 500:  # Na 500 stappen stoppen om vastlopen te voorkomen
        action = choose_action(state)
        next_state, reward = take_action(state, action)
        update_q_value(state, action, reward, next_state)

        player.x = next_state[1] * TILE_SIZE
        player.y = next_state[0] * TILE_SIZE + 120
        state = next_state
        if maze[state[0]][state[1]] == 2:  # Stopt de episode als 'goal' is bereikt
            global episode, total_reward
            episode += 1
            break
        steps += 1

clock.schedule_interval(train_episode, 0.01)

pgzrun.go()
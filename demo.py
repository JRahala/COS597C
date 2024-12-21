import pygame
from random import randint

WIDTH = 1200
HEIGHT = 800

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
RUNNING = True

# Number of tasks
N = 40

# Lower and upper bounds on time
L = 10
U = 50

# Keep track of all tasks
TASKS = []

def create_tasks():
    tasks = []
    for _ in range(N): tasks.append(randint(L, U))
    return tasks

def draw_task(i):
    y = 50 + (700*i/N)
    x = 50
    pygame.draw.line(WINDOW, (000,000,000), (x, y), (x+U, y), width=15)
    pygame.draw.line(WINDOW, (255,255,255), (x, y), (x+TASKS[i], y), width=15)

# Signed
def discrepancy(choices):
    val = 0
    for i in range(N):
        if (choices[i] == 0): val -= TASKS[i]
        else: val += TASKS[i]
    return val

def random_string():
    workers = []
    for _ in range(N): workers.append(randint(0,1))
    return workers


# RLS Algorithm
def rls_step():
    global RLS_choices, RLS_discrepancy
    i = randint(0, N-1)
    if (RLS_choices[i] == 0): new_discrepancy = RLS_discrepancy + 2 * TASKS[i]
    else: new_discrepancy = RLS_discrepancy - 2 * TASKS[i]
    if (abs(new_discrepancy) <= abs(RLS_discrepancy)):
        RLS_choices[i] = (1 - RLS_choices[i])
        RLS_discrepancy = new_discrepancy
        return True, i
    return False, None

# EA Algorithm
def ea_step():
    global EA_choices, EA_discrepancy
    new_choices = []
    new_discrepancy = EA_discrepancy

    for i in range(N):
        flip = randint(1, N)
        if (flip == 1): 
            if (EA_choices[i] == 0): new_discrepancy += 2 * TASKS[i]
            else: new_discrepancy -= 2 * TASKS[i]
            new_choices.append((1 - EA_choices[i]))
        else: new_choices.append(EA_choices[i])
    
    if (abs(new_discrepancy) <= abs(EA_discrepancy)):
        EA_choices = new_choices
        EA_discrepancy = new_discrepancy
        return True, new_choices
    return False, None

# BRUTE Algorithm
def brute_step():
    global BRUTE_choices, BRUTE_discrepancy
    new_choices = random_string()
    new_discrepancy = discrepancy(new_choices)
    if (abs(new_discrepancy) < abs(BRUTE_discrepancy)):
        BRUTE_discrepancy = new_discrepancy
        BRUTE_choices = new_choices
        return True, new_choices
    return False, None

"""
UNCOMMENT ME TO SEE ADVERSARIAL OPPONENT RATHER THAN A RANDOM ONE

# Adversarial move
def adversarial_move():
    # try to find a move that hurts all players - if not we choose a random one to hurt (which must exist)
    # if one doesn't exist we will try generating the data independently
    found = False
    discrepancy_change = 0
    i = 0
    new_size = 0
    max_tries = N * (U-L) * 1.0 # Search space

    while not found and max_tries > 0:
        max_tries -= 1
        i = randint(0, N-1)
        bigger = randint(0, 1)

        if (bigger): new_size = randint(TASKS[i], U)
        else: new_size = randint(L, TASKS[i]) 

        RLS_discrepancy_change = new_size - TASKS[i]
        EA_discrepancy_change = new_size - TASKS[i]

        if (RLS_choices[i] == 0): RLS_discrepancy_change *= -1
        if (EA_choices[i] == 0): EA_discrepancy_change *= -1
        
        if (abs(RLS_discrepancy_change + RLS_discrepancy) <= abs(RLS_discrepancy)): continue
        if (abs(EA_discrepancy_change + EA_discrepancy) <= abs(EA_discrepancy)): continue
        found = True
    

    TASKS[i] = new_size
    return found, i, new_size, RLS_discrepancy_change, EA_discrepancy_change
"""

def random_move():
    global BRUTE_discrepancy, EA_discrepancy, RLS_discrepancy
    i = randint(0, N-1)
    old_size = TASKS[i]
    new_size = randint(L,U)
    TASKS[i] = new_size

    BRUTE_discrepancy = discrepancy(BRUTE_choices)
    EA_discrepancy = discrepancy(EA_choices)
    RLS_discrepancy = discrepancy(RLS_choices)
    return i, old_size, new_size


def draw_choices(choices, start_x = 200, start_y = 50):
    zeros_x = start_x
    ones_x = start_x

    zeros_y = start_y
    ones_y = start_y + 40

    zeros_cols = (255,000,000)
    ones_cols = (000,000,255)
    
    pygame.draw.rect(WINDOW, (000,000,000), (start_x, start_y-10, (U+10) * N, 200))

    for i in range(N):
        if (choices[i] == 0):
            pygame.draw.line(WINDOW, zeros_cols, (zeros_x, zeros_y), (zeros_x+TASKS[i], zeros_y), width=15)
            zeros_x += TASKS[i] + 10
        else:
            pygame.draw.line(WINDOW, ones_cols, (ones_x, ones_y), (ones_x+TASKS[i], ones_y), width=15)
            ones_x += TASKS[i] + 10


def draw_scores(discrepancies, start_x = 200, start_y = 50):
    for i in range(len(discrepancies)):
        normalised_score = abs(discrepancies[i] / (N * (U-L))) * 250
        raw_capped_score = min(abs(discrepancies[i]), 60)
        score = raw_capped_score
        
        pygame.draw.line(WINDOW, (255,255,255), (start_x + i, start_y + 60), (start_x + i, start_y + 60 + score), width=1) 


TASKS = create_tasks()

RLS_choices = random_string()
RLS_discrepancy = discrepancy(RLS_choices)
RLS_scores = [RLS_discrepancy]

EA_choices = random_string()
EA_discrepancy = discrepancy(EA_choices)
EA_scores = [EA_discrepancy]

BRUTE_choices = random_string()
BRUTE_discrepancy = discrepancy(BRUTE_choices)
BRUTE_scores = [BRUTE_discrepancy]

# Code the loop in text then implement with images and graphs
"""
for i in range(100):
    for j in range(1<<7):
        rls_step()
        ea_step()
        print(f"EA: {EA_discrepancy} \t RLS: {RLS_discrepancy}")
    found, index, new_size, discrepancy_change = adversarial_move()
    RLS_discrepancy += discrepancy_change
    EA_discrepancy += discrepancy_change
    print(f"EA: {EA_discrepancy} \t RLS: {RLS_discrepancy} \t {found}")
""" 

# Init
CLOCK = pygame.time.Clock()
for i in range(N): draw_task(i)

FPS = 60

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: RUNNING = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP: FPS += 5; print(f"FPS set to {FPS}")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN: FPS = max(10, FPS-5); print(f"FPS set to {FPS}")
        

    # Brute reset
    BRUTE_choices = random_string()
    BRUTE_discrepancy = discrepancy(BRUTE_choices)

    for j in range(4):
        ea_step()
        draw_choices(EA_choices)
        EA_scores.append(EA_discrepancy)
        draw_scores(EA_scores)

        rls_step()
        draw_choices(RLS_choices, start_y=300)
        RLS_scores.append(RLS_discrepancy)
        draw_scores(RLS_scores, start_y=300)

        brute_step()
        draw_choices(BRUTE_choices, start_y=550)
        BRUTE_scores.append(BRUTE_discrepancy)
        draw_scores(BRUTE_scores, start_y=550)

    pygame.display.update()

    max_scoll_len = 600
    if len(EA_scores) >= max_scoll_len: EA_scores = []
    if len(RLS_scores) >= max_scoll_len: RLS_scores = []
    if len(BRUTE_scores) >= max_scoll_len: BRUTE_scores = []
    
    index, new_size, old_size = random_move()
    draw_task(index)

    CLOCK.tick(max(10, FPS))
    pygame.display.update()

pygame.quit()

"""
import matplotlib.pyplot as plt 

plt.plot(EA_scores)
plt.show()
"""
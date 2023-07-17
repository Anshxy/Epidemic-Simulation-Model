import pygame
import random
import time
import matplotlib.backends.backend_agg as agg\
    
import numpy as np
import matplotlib.pyplot as plt
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 100, 600

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

#Parameters
STARTING_AFFECTED = 1
RECOVERY_RATE = 10 #days (days per second)
TIME_DELAY = 30 #milliseconds
BALL_RADIUS = 4
BALL_COUNT = 100
BALL_SPEED = 4
INFECTION_PROBABILITY = 0.8  # Infection probability (range 0 to 1, where 1 means 100% chance of infection)

#Global stats
susceptible = BALL_COUNT - STARTING_AFFECTED
infected = STARTING_AFFECTED
recovered = 0
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
SIMULATION_WIDTH, SIMULATION_HEIGHT = 600, 600
GRAPH_WIDTH, GRAPH_HEIGHT = SCREEN_WIDTH - SIMULATION_WIDTH, SCREEN_HEIGHT

# Create the screen
screen = pygame.display.set_mode((SIMULATION_WIDTH + GRAPH_WIDTH, max(SIMULATION_HEIGHT, GRAPH_HEIGHT)))
pygame.display.set_caption('Epidemic Simulation')

# 

fig, ax = plt.subplots(figsize=(4.5, 4))



plt.title("SIR graph")
ax.set_xlabel('Days')
ax.set_ylabel('Population')
line_s, = ax.plot([], [], label="Susceptible", color="green")
line_i, = ax.plot([], [], label="Infected", color="red")
line_r, = ax.plot([], [], label="Recovered", color="grey")
ax.set_xlim(0, 90)
ax.set_ylim(0, BALL_COUNT)
ax.legend()

canvas = agg.FigureCanvasAgg(fig)


# 



# Ball class
class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = random.choice([-1, 1]) * BALL_SPEED
        self.dy = random.choice([-1, 1]) * BALL_SPEED
        self.frames_infected = 0  # Number of frames the ball has been infected

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off the edges
        if self.x - self.radius <= 0 or self.x + self.radius >= SIMULATION_WIDTH:
            self.dx *= -1

        if self.y - self.radius <= 0 or self.y + self.radius >= SIMULATION_HEIGHT:
            self.dy *= -1
        
        

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def update_infection_status(self):
        if self.color == RED:
            self.frames_infected += TIME_DELAY/1000
            if self.frames_infected >= RECOVERY_RATE:
                global infected, recovered
                self.color = GREY
                infected -= 1
                recovered += 1
                self.frames_infected = 0  # Reset frames infected
                
        
        


# Create a list to store all the balls
balls = []
for i in range(BALL_COUNT):
    if i < STARTING_AFFECTED:
        color = RED
    else:
        color = GREEN

    x = random.randint(BALL_RADIUS, SIMULATION_WIDTH - BALL_RADIUS)
    y = random.randint(BALL_RADIUS, SIMULATION_HEIGHT - BALL_RADIUS)
    balls.append(Ball(x, y, BALL_RADIUS, color))


# Function to check and handle collisions
def handle_collisions():
    global susceptible, infected

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            dx = balls[j].x - balls[i].x
            dy = balls[j].y - balls[i].y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5

            if distance < (balls[i].radius + balls[j].radius):
                if balls[i].color == GREEN and balls[j].color == RED:
                    if random.random() < INFECTION_PROBABILITY:
                        balls[i].color = RED
                        susceptible -= 1
                        infected += 1

                if balls[j].color == GREEN and balls[i].color == RED:
                    if random.random() < INFECTION_PROBABILITY: 
                        balls[j].color = RED
                        susceptible -= 1
                        infected += 1


# Lists to store data for plotting
days_data = []
susceptible_data = []
infected_data = []
recovered_data = []

def update_graph():
    line_s.set_data(days_data, susceptible_data)
    line_i.set_data(days_data, infected_data)
    line_r.set_data(days_data, recovered_data)
    ax.set_xlim(0, days + 1)


# Game loop
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
time_elapsed = 0
days = 1  # Initialize day counter
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, SIMULATION_WIDTH, SIMULATION_HEIGHT), 2)

    # Move and draw the balls
    for ball in balls:
        ball.move()
        ball.draw()
        ball.update_infection_status()

    # Check for collisions and handle them
    handle_collisions()

    # Calculate the time since the last frame
    dt = clock.tick(60) / 1000  # Get the elapsed time in seconds

    # Update the time_elapsed variable with the elapsed time
    time_elapsed += dt

    # Update the day counter if a day has passed
    if time_elapsed >= 1:
        days += 1
        time_elapsed = 0  # Reset time_elapsed for the next day
        
        days_data.append(days)
        susceptible_data.append(susceptible)
        infected_data.append(infected)
        recovered_data.append(recovered)

        # Update the graph data
        update_graph()
        
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    graph_position = (SCREEN_WIDTH - 400, 125)  # Adjust the position of the graph on the screen
    screen.blit(surf, graph_position)

    
    # Render the day counter title
    day_text = font.render(f"Day {days}, Infected: {infected}, Susceptible: {susceptible}, Recovered: {recovered}", True, (255, 255, 255))
    screen.blit(day_text, (10, 10))

    pygame.display.flip()
import pygame
import random
import time
from graph import SIR


pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

#Parameters
STARTING_AFFECTED = 5
RECOVERY_RATE = 10 #days (days per second)
TIME_DELAY = 30 #milliseconds
BALL_RADIUS = 4
BALL_COUNT = 30
BALL_SPEED = 10
INFECTION_PROBABILITY = 0.8  # Infection probability (range 0 to 1, where 1 means 100% chance of infection)

#Global stats
susceptible = BALL_COUNT - STARTING_AFFECTED
infected = STARTING_AFFECTED
recovered = 0


# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.HWSURFACE | pygame.DOUBLEBUF)

pygame.display.set_caption('Epidemic Simulation')

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
        if self.x - self.radius <= 0 or self.x + self.radius >= SCREEN_WIDTH:
            self.dx *= -1

        if self.y - self.radius <= 0 or self.y + self.radius >= SCREEN_HEIGHT:
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

    x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
    y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
    balls.append(Ball(x, y, BALL_RADIUS, color))


# Function to check and handle collisions
def handle_collisions():
    global susceptible, infected

    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]
            
            dx = ball2.x - ball1.x
            dy = ball2.y - ball1.y
            distance_squared = dx**2 + dy**2
            
            if distance_squared < (2 * BALL_RADIUS) ** 2:  # Check if the balls are within 2 times the diameter (early exit condition)
                if ball1.color == GREEN and ball2.color == RED:
                    if random.random() < INFECTION_PROBABILITY:
                        ball1.color = RED
                        susceptible -= 1
                        infected += 1

                if ball2.color == GREEN and ball1.color == RED:
                    if random.random() < INFECTION_PROBABILITY: 
                        ball2.color = RED
                        susceptible -= 1
                        infected += 1



# Game loop

days_list = [0]
susceptible_list = [susceptible]
infected_list = [0]
recovered_list = [0]


font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
time_elapsed = 0
days = 1  # Initialize day counter
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or infected == 0:
            running = False
        
    screen.fill((0, 0, 0))

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
        time_elapsed = 0 

        days_list.append(days)
        susceptible_list.append(susceptible)
        infected_list.append(infected)
        recovered_list.append(recovered)
         # Reset time_elapsed for the next day

    # Render the day counter title
    day_text = font.render(f"Day {days}, Infected: {infected}, Susceptible: {susceptible}, Recovered: {recovered}", True, (255, 255, 255))
    screen.blit(day_text, (10, 10))

    pygame.display.flip()


SIR(days_list, susceptible_list, infected_list, recovered_list)
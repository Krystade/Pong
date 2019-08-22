import pygame
import random
import sys
pygame.init()


# Dimensions of window
width = 800
height = 500
screen = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
# score[0] = left score[1] = right
font = pygame.font.SysFont(None, 50)
score = [0, 0]

class Paddle():
    def __init__ (self, pos):
        self.pos = pos
        #how quickly the will be moving up or down
        self.speed = 0
        #-1 direction is up +1 direction is down
        self.direction = -1
        self.width = 20
        self.height = 100

        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def move(self, speed):
        self.speed = speed * self.direction
        self.pos = (self.pos[0], self.speed + self.pos[1])

    def display(self):
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        pygame.draw.rect(screen, (255, 255, 255), self.hitbox, 0)

class Ball():
    def __init__ (self):
        self.pos = [int(width/2), int(height/2)]
        #Two while loops to handle 0 speed in x and y directions
        self.velocity = [random.randint(-10,10), random.randint(-10,10)]
        while self.velocity[0] == 0:
            self.velocity = [random.randint(-10, 10), self.velocity[1]]
        while self.velocity[1] == 0:
            self.velocity = [self.velocity[0], random.randint(-10, 10)]

        self.radius = 10
        self.hitbox = pygame.Rect(self.pos[0] - self.radius, self.pos[1] + self.radius, self.radius * 2, self.radius * 2)


    def move(self):
        self.pos = (self.velocity[0] + self.pos[0], self.velocity[1] + self.pos[1])

    def display(self):
        pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 1)
        pygame.draw.circle(screen, (255, 255, 255), self.pos, self.radius, 0)
        self.hitbox = pygame.Rect(self.pos[0] - self.radius, self.pos[1] + self.radius, self.radius * 2, self.radius * 2)


paddleLeft = Paddle((50, 250))
paddleRight = Paddle((width - 50, 250))
ball = Ball()





while True:

    # If the red X in the window is clicked close the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    # Update the screen as well as make it black
    pygame.display.update()
    screen.fill((0, 0, 0))

    # Speed of the game
    clock.tick(60)

    # Check for keypress to see if the user wants to change direction
    key = pygame.key.get_pressed()
    # UP
    if key[pygame.K_UP] or key[pygame.K_w]:
        paddleRight.move(10)
    # DOWN
    elif key[pygame.K_DOWN] or key[pygame.K_s]:
        paddleRight.move(-10)

    # Make sure the paddle doesn't go off screen
    if paddleRight.pos[1] <= 0:
        paddleRight.pos = (paddleRight.pos[0], 0)
    if paddleRight.pos[1] >= height - paddleRight.height:
        paddleRight.pos = (paddleRight.pos[0], height - paddleRight.height)

    # Bounce the left paddle
    if paddleLeft.pos[1] >= height - paddleLeft.height and paddleLeft.direction == 1:
        paddleLeft.direction = -1
    elif paddleLeft.pos[1] <= 0 and paddleLeft.direction == -1:
        paddleLeft.direction = 1

    # Reset the ball if it goes off screen
    if ball.pos[0] > width + ball.radius or ball.pos[0] < -ball.radius:
        print(score)
        if ball.pos[0] < 0:
            score[0] = score[0] + 1
        elif ball.pos[0] > width:
            score[1] = score[1] + 1
        ball.pos = [int(width / 2), int(height / 2)]
        # Two while loops to handle 0 speed in x and y directions
        ball.velocity = [random.randint(-10, 10), random.randint(-10, 10)]
        while ball.velocity[0] == 0:
            ball.velocity = [random.randint(-10, 10), ball.velocity[1]]
        while ball.velocity[1] == 0:
            ball.velocity = [ball.velocity[0], random.randint(-10, 10)]

    # Bounce the ball off the ceiling
    if ball.pos[1] > height - ball.radius:
        ball.pos = (ball.pos[0], height - ball.radius)
        ball.velocity = (ball.velocity[0], -ball.velocity[1])
    if ball.pos[1] < ball.radius:
        ball.pos = (ball.pos[0], ball.radius)
        ball.velocity = (ball.velocity[0], -ball.velocity[1])

    # Bounce the ball off the right paddles
    if paddleRight.hitbox.colliderect(ball.hitbox):
        ball.pos = (paddleRight.pos[0] - ball.radius, ball.pos[1])
        ball.velocity = (-ball.velocity[0], ball.velocity[1])
        print("Hits right paddle")
        # Bounce the ball off the left paddles
    if paddleLeft.hitbox.colliderect(ball.hitbox):
        ball.pos = (paddleLeft.pos[0] + ball.radius + paddleLeft.width, ball.pos[1])
        ball.velocity = (-ball.velocity[0], ball.velocity[1])
        print("Hits left paddle")

    # Printing the scores
    # Left paddle's score
    text = font.render("Score: " + str(score[1]), True, (255, 255, 255), (0, 0, 0))
    screen.blit(text, (10,0))
    # Right paddle's score
    text = font.render("Score: " + str(score[0]), True, (255, 255, 255), (0, 0, 0))
    screen.blit(text, (width - text.get_rect()[2] - 10,0))
    
    # Displaying the paddles and the ball
    ball.display()
    paddleLeft.display()
    paddleRight.display()

    # Moving the paddles and the ball
    ball.move()
    paddleLeft.move(10)

import pygame
import math
import random as r


SCR_WIDTH = 900
SCR_HEIGHT = 600
BG_COLOR = (50, 100, 210)


class Organism:
    
    def __init__(self):
        self.x = r.randrange(10, SCR_WIDTH)
        self.y = r.randrange(10, SCR_HEIGHT // 2)
        self.direction = r.randrange(360)
        
        self.size = 10
                
    def update(self):
        self.x += math.cos(self.direction * (math.pi / 180))
        self.y += math.sin(self.direction * (math.pi / 180))
        
        self.direction = self.direction + r.randint(-10, 10)
        
        # go in opposite direction if a wall is hit
        if self.x - self.size <= 0 or self.x + self.size >= SCR_WIDTH:
            self.direction = self.direction - 180
        if self.y - self.size <= 0 or self.y + self.size >= SCR_HEIGHT:
            self.direction = self.direction - 180
    
    def draw(self, screen):
        pygame.draw.circle(screen, (200,100,100), (int(self.x), int(self.y)), self.size)
        
        


def run():
    # Initialize game and create screen object.
    pygame.init()
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption('Predators and Evolving Prey')
    
    running = True
    
    organisms = [Organism() for x in range(20)]
    
    
    # Start the main loop for the game.
    while running:
        
        screen.fill(BG_COLOR)
        
        for organism in organisms:
            organism.update()
            organism.draw(screen)
    
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

run()

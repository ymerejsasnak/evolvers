import pygame
import math
import random as r


SCR_WIDTH = 900
SCR_HEIGHT = 600
BG_COLOR = (50, 100, 210)


class Organism:
    
    def __init__(self):
        pass
                
    def move(self):
        self.x += math.cos(self.direction * (math.pi / 180))
        self.y += math.sin(self.direction * (math.pi / 180))
        
        self.direction = self.direction + r.randint(-self.direction_rate, self.direction_rate)
        
        # go in opposite direction if a wall is hit
        if self.x - self.size <= 0:
            self.x = self.size            
            self.direction = self.direction - 180            
        elif self.x + self.size >= SCR_WIDTH:
            self.x = SCR_WIDTH - self.size
            self.direction = self.direction - 180
        if self.y - self.size <= 0:
            self.y = self.size
            self.direction = self.direction - 180        
        elif self.y + self.size >= SCR_HEIGHT:
            self.y = SCR_HEIGHT - self.size
            self.direction = self.direction - 180
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


class Predator(Organism):
    
    def __init__(self):
        self.size = 15
        self.color = (200, 100, 100)
        
        self.x = r.randrange(self.size, SCR_WIDTH - self.size)
        self.y = r.randrange(self.size, SCR_HEIGHT // 2 - self.size)
        
        self.direction = r.randrange(360)
        self.direction_rate = r.randint(5, 25)
    
    def eat(self, preys):
        for prey in preys:
            distance = ((self.x - prey.x) ** 2 + (self.y - prey.y) ** 2) ** 0.5
            if distance < self.size + prey.size - 1:
                prey.alive = False
        
        
class Prey(Organism):
    
    def __init__(self):
        self.size = 5
        self.color = (100, 200, 100)
        self.alive = True
        
        self.x = r.randrange(self.size, SCR_WIDTH - self.size)
        self.y = r.randrange(SCR_HEIGHT // 2 + self.size, SCR_HEIGHT - self.size)
        
        self.direction = r.randrange(360)
        self.direction_rate = r.randint(5, 25)
        
        #traits to possibly inherit:
        # speed, size, direction change rate, reproduction frequency, reproduction brood size, avoidance? (radius around them)
    
    
        


def run():
    # Initialize game and create screen object.
    pygame.init()
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption('Predators and Evolving Prey')
    
    running = True
    
    predators = [Predator() for x in range(10)]
    preys = [Prey() for x in range(100)]
    
    
    # Start the main loop for the game.
    while running:
        
        screen.fill(BG_COLOR)
        
        for predator in predators:
            predator.move()
            predator.eat(preys)
            predator.draw(screen)
        
        # delete any prey that were eaten
        preys = [prey for prey in preys if prey.alive]
            
        for prey in preys:
            prey.move()
            prey.draw(screen)
    
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

run()

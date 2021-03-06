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
        self.x += math.cos(self.direction * (math.pi / 180)) * self.speed
        self.y += math.sin(self.direction * (math.pi / 180)) * self.speed
        
        self.direction = self.direction + r.randint(-self.direction_change, self.direction_change)
        
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
        self.size = r.randint(20, 25)
        self.color = (r.randint(180, 220), r.randint(50, 90), r.randint(50, 90))
                
        self.x = r.randrange(self.size, SCR_WIDTH - self.size)
        self.y = r.randrange(self.size, SCR_HEIGHT // 2 - self.size)
        
        self.speed = r.uniform(0.7,1.1)
        self.direction = r.randrange(360)
        self.direction_randomness = r.randint(15, 35)
        
        self.hunger = 20
        
        self.target = None
        
        self.alive = True
        
        
    
    def eat(self, preys):
        if len(preys) > 10:  # won't eat remaining prey if too few to sustain further population
            
            for prey in preys:
                distance = ((self.x - prey.x) ** 2 + (self.y - prey.y) ** 2) ** 0.5
                if distance < self.size + prey.size - 1:
                    prey.alive = False
                    self.hunger -= 2
            
    
    def move(self, preys):
        if not self.target or not self.target.alive:
            self.target = r.choice(preys)
        
        self.hunger += .04
        if self.hunger >= 100:
            self.alive = False

        self.x += math.cos(self.direction * (math.pi / 180)) * self.speed
        self.y += math.sin(self.direction * (math.pi / 180)) * self.speed
        
        self.direction = math.atan2(self.target.y - self.y, self.target.x - self.x) * (180 / math.pi)
        
        self.direction += self.direction_randomness
        
        # don't think I need to check for wall collision because target will not be out of bounds
    
    def split(self, predators):
        if self.hunger <= 0:
            self.hunger = 40
            child = Predator()
            child.x = self.x
            child.y = self.y
            predators.append(child)
            
        
class Prey(Organism):
    
    def __init__(self):
        self.size = r.randint(5, 15)
        self.color = (r.randint(0,50), r.randint(10, 250), r.randint(10, 250))
        self.alive = True
        
        self.x = r.randrange(self.size, SCR_WIDTH - self.size)
        self.y = r.randrange(SCR_HEIGHT // 2 + self.size, SCR_HEIGHT - self.size)
        
        self.direction = r.randrange(360)
        self.direction_change = r.randint(5, 25)
        
        self.speed = r.uniform(.9, 1.3)
        
        self.split_frequency = r.randint(800, 1000)
        #self.split_children = r.randint(2, 3)
        self.split_counter = 0
        
        
    def split(self, preys):
        self.split_counter = (self.split_counter + 1) % self.split_frequency
        
        if self.split_counter == 0:
            child = Prey()
            child.x = self.x
            child.y = self.y
            
            # inherited traits:
            child.color = self.color
            child.size = self.size + r.randint(-1, 1)
            if child.size < 2:
                child.size = 2
            child.speed = self.speed + r.uniform(-.1, .1)
            child.direction_change = self.direction_change + r.randint(-1, 1)
            if child.direction_change <= 0:
                child.direction_change = 1
            child.split_frequency = self.split_frequency + r.randint(-1, 10)
            if child.split_frequency < 200:
                child.split_frequency = 200
            
            preys.append(child)          


def run():
    # Initialize game and create screen object.
    pygame.init()
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    pygame.display.set_caption('Predators and Evolving Prey')
    
    running = True
    
    predators = [Predator() for x in range(2)]
    preys = [Prey() for x in range(50)]
    
    
    # Start the main loop for the game.
    while running:
        
        screen.fill(BG_COLOR)
        
        for predator in predators:
            predator.move(preys)
            predator.eat(preys)
            if len(predators) < 16:  #population limit on predators 
                predator.split(predators)
            predator.draw(screen)
        
        # delete any prey that were eaten and predators that starved
        preys = [prey for prey in preys if prey.alive]
        predators = [predator for predator in predators if predator.alive]
            
        for prey in preys:
            prey.move()
            if len(preys) < 2000:  # population limit (to keep computer from slowing to crawl)
                prey.split(preys)
            prey.draw(screen)
    
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
        
        # Make the most recently drawn screen visible
        pygame.display.flip()

run()

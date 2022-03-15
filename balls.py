import pygame
from random import random, randint, choice, randrange

BACKGROUND_COLOR = (255, 255, 255)

SCREEN_WIDTH = 700 
SCREEN_HEIGHT = 500

class Ball:

    def __init__(self, x, y, radius = None): 
        self.x = self.x = x
        self.y = y
        self.radius = radius if radius is not None else randint(10,75) 
        self.randomize()
        self._minmax()


    def _minmax(self):
        self.min_x = self.min_y = self.radius 
        self.max_x = SCREEN_WIDTH - self.radius 
        self.max_y = SCREEN_HEIGHT - self.radius


    def randomize(self):
        self.colour = randrange(0, 255), randrange(0, 255), randrange(0, 255) 
        self.dx = randint(-3,3)
        self.dy = randint(-3,3)


    def move(self):
        self.x = constrain(self.min_x, self.x + self.dx, self.max_x) 
        self.y = constrain(self.min_y, self.y + self.dy, self.max_y) 
        if self.x in (self.min_x, self.max_x):
            self.dx = -self.dx
        if self.y in (self.min_y, self.max_y):
            self.dy = -self.dy


    def draw(self, screen):
        self.screen = screen 
        pygame.draw.circle(self.screen, self.colour,
                                (self.x, self.y), self.radius)


class SpecialBall(Ball):
    
    radius = 8
    colour = 255, 0, 255


    def __init__(self, x, y): 
        self.x, self.y = x, y 
        self._direction() 
        self.sleeping = 1 
        self._minmax()


    def _direction(self): 
        speed = randint(4, 6) 
        self.dx = choice((-1, 1)) * speed
        self.dy = choice((-1, 1)) * speed


    def move(self):
        if self.sleeping > 0:
           self.sleeping -= 1
        if self.sleeping == 0:
            self._direction()
        else:
            super().move()
        
        if random() < 0.01:
            self.sleeping = 100
            
class Player(Ball):
        
    def __init__(self):
        super().__init__(350, 250, 15)
        self.dx = 0
        self.dy = 0
        self.colour = 0, 0, 0
        
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.y += 2
        if keys[pygame.K_UP]:
            self.y -= 2
        if keys[pygame.K_RIGHT]:
            self.x += 2
        if keys[pygame.K_LEFT]:
            self.x -= 2
        self.x = constrain(self.min_x, self.x + self.dx, self.max_x)
        self.y = constrain(self.min_y, self.y + self.dy, self.max_y)
        
        
def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Balls")
    clock = pygame.time.Clock()
    balls = []
    for i in range(1, 5):
        balls.append(Ball(100*i, 100*i))
                          
    player = Player()
    done = False
    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_r:
                    choice(balls).randomize() 
                elif event.key == pygame.K_a:
                    new_ball = Ball(400, 100)
                    balls.append(new_ball)
                elif event.key == pygame.K_s:
                    new_ball = SpecialBall(150,200)
                    balls.append(new_ball)
                    
        screen.fill(BACKGROUND_COLOR)
        player.draw(screen)
        
        for ball in balls:
            ball.draw(screen)
            ball.move()
            
        player.draw(screen)
        player.move()
        pygame.display.flip()
    pygame.quit()
    
    
def constrain(small, value, big):
    return min(max(value, small), big)
    
    
if __name__ == "__main__":
    main()

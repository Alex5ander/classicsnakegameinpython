import pygame, sys, random, map, os
from pygame.locals import *
os.environ["SDL_VIDEO_CENTERED"] = '1'
pygame.init()
mainClock = pygame.time.Clock()
WIDTH = 480
HEIGHT = 480
tileSize = 24
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Classic Snake Game")
font = pygame.font.SysFont("Impact", tileSize)
grass = pygame.transform.scale(pygame.image.load("grass.png"), (tileSize, tileSize))
stone = pygame.transform.scale(pygame.image.load("stone.png"), (tileSize, tileSize))
background = pygame.Surface((WIDTH, HEIGHT))
y = 0
while y < len(map.levelMap):
    x = 0
    while x < len(map.levelMap[0]):
        tile = map.levelMap
        if tile[y][x] == 0:
            background.blit(grass, (x * tileSize, y * tileSize))
        elif tile[y][x] == 1:
            background.blit(stone, (x * tileSize, y * tileSize))
        x += 1
    y += 1
class Snake:
    def __init__(self):
        self.size = tileSize
        self.dir = pygame.Vector2(1, 0)
        self.gotTheApple = 4
        self.time = 0
        self.body = [pygame.Vector2(self.size, self.size), pygame.Vector2(self.size, self.size * 2), pygame.Vector2(self.size, self.size * 3)]
    def draw(self):
        for i, p in enumerate(self.body):
            c = 255 - (i * 10)
            if c < 0:
                color = (0, 0, 0)
            else:
                color = (0, c, c)
            if i == 0:
                color = (0, 200, 200)
                pygame.draw.rect(screen, color, (int(p.x), int(p.y), int(self.size), int(self.size)))
            else:
                pygame.draw.rect(screen, color, (int(p.x), int(p.y), int(self.size), int(self.size)))
            if self.gotTheApple == i:
                pygame.draw.circle(screen, color, (int(p.x + self.size/2), int(p.y+self.size/2)), self.size)
    def move(self, x, y):
        if x != 0 and self.dir.y != 0:
            self.dir.x = x
            self.dir.y = 0
            self.time = 3
        elif y != 0 and self.dir.x != 0:
            self.dir.x = 0
            self.dir.y = y
            self.time = 3
    def growUp(self):
        tail = self.body[len(self.body) - 1]
        parts = pygame.Vector2(tail.x, tail.y)
        self.body.append(parts)
    def update(self):
        if self.time >= 4:
            self.time = 0
            if self.gotTheApple < len(self.body):
                self.gotTheApple += 1
            nextX = self.body[0].x + self.dir.x * self.size
            nextY = self.body[0].y + self.dir.y * self.size
            for p in self.body:
                currentX = p.x
                currentY = p.y
                
                p.x = nextX
                p.y = nextY
                
                nextX = currentX
                nextY = currentY
            if self.body[0].x > WIDTH:
                self.body[0].x = 0
            elif self.body[0].x < 0:
                self.body[0].x = WIDTH
            elif self.body[0].y > HEIGHT:
                self.body[0].y = 0
            elif self.body[0].y < 0:
                self.body[0].y = HEIGHT
        else:
            self.time += 1
class Fruit:
    def __init__(self):
        self.size = 8
        self.pos = None
        self.randopos()
    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.size)
    def randopos(self):
        x = random.randint(0, 19)
        y = random.randint(0, 19) 
        while map.levelMap[y][x] == 1:
            x = random.randint(0, 19)
            y = random.randint(0, 19)
        self.pos = pygame.Vector2((x * tileSize) + tileSize / 2, (y * tileSize) + tileSize / 2)
class Game:
    def __init__(self):
        self.score = 0
        self.gameState = 0
        self.pause = False
        self.player = Snake()
        self.fruit = Fruit()
    def drawText(self, text, coords, color):
        textsurface = font.render(text, False, color)
        textrect = textsurface.get_rect(center=coords)
        screen.blit(textsurface, textrect)
    def render(self):
        screen.blit(background, (0, 0))
        self.player.draw()
        self.fruit.draw()
        if self.gameState == 0:
            self.drawText("PRESS SPACE BAR TO PLAY", (int(WIDTH / 2), int(HEIGHT / 2)), (0, 255, 0))
        elif self.gameState == 1:
            self.drawText("SCORE: "+str(self.score), (int(WIDTH / 2), tileSize), (255, 255, 255))
            self.drawText("FPS: "+str(int(mainClock.get_fps())), (int(tileSize * 2), tileSize), (255, 255, 255))
            if self.pause:
                self.drawText("PAUSE", (int(WIDTH / 2), int(HEIGHT / 2)), (255, 0, 0))
        elif self.gameState == 2:
            self.drawText("GAME OVER", (int(WIDTH / 2), int(HEIGHT / 2)), (255, 0, 0))
    def update(self):
        if self.gameState == 1 and self.pause == False:
            self.player.update()
            head = self.player.body[0]
            for i,b in enumerate(self.player.body):
                if i != 0 and i > 2:
                    hx = int(head.x / tileSize) % 20
                    hy = int(head.y / tileSize) % 20
                    
                    bx = int(b.x / tileSize) % 20
                    by = int(b.y / tileSize) % 20
                    
                    if hx == bx and hy == by and head.x > 0 and head.x < WIDTH and head.y > 0 and head.y < HEIGHT:
                        self.gameState = 2
            nx = int(head.x / tileSize) % 20
            ny = int(head.y / tileSize) % 20
            if map.levelMap[ny][nx] == 1:
                self.gameState = 2
            vectordistance = pygame.Vector2((head.x + self.player.size / 2) - self.fruit.pos.x, (head.y + self.player.size / 2) - self.fruit.pos.y)
            distance = vectordistance.magnitude()
            if distance < self.fruit.size:
                self.player.gotTheApple = 0
                self.fruit.randopos()
                self.score += 1
                self.player.growUp()
    def keydown(self, key):
        if self.gameState == 0:
            if key == K_SPACE:
                self.gameState = 1
        elif self.gameState == 1:
            if key == K_LEFT:
                self.player.move(-1, 0)
            elif key == K_RIGHT:
                self.player.move(1, 0)
            elif key == K_UP:
                self.player.move(0, -1)
            elif key == K_DOWN:
                self.player.move(0, 1)
            elif key == K_SPACE:
                self.pause = False if self.pause == True else True
        elif self.gameState == 2:
            if key == K_SPACE:
                self.resete()
    def resete(self):
        self.gameState = 0
        self.score = 0
        self.pause = False
        self.player = Snake()
        self.fruit = Fruit()
g = Game()
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            g.keydown(event.key)
    g.update()
    g.render()
    mainClock.tick(30)
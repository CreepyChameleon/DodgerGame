# imports
import pygame
import sys
import random

pygame.font.init()
pygame.init()

HEIGHT = 900
WIDTH = 1200

# variables
delay = 0
timer = 0
game_time = 0
playerx = 0
roundd = 0
lives = 10
score = 0
run_menu = True
run_game = False

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 155, 0)
PURPLE = (200, 0, 255)

# images
SPACE_BAK_IMG = pygame.image.load("resources\\space_bak.png")
TITLE_IMG = pygame.image.load("resources\\title.png")

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger!")
clock = pygame.time.Clock()

FONT_SANS = pygame.font.SysFont("comicsans", 30)

enemies = []


class Player:
    def __init__(self):
        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False
        self.lives = lives

        self.surf = pygame.surface.Surface((50, 50))
        self.rect = self.surf.get_rect(midbottom=(WIDTH / 2, 500))
        self.surf.fill(WHITE)

    def event(self):
        self.moveRight = False
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.moveRight = True
        if keys[pygame.K_LEFT]:
            self.moveLeft = True
        if keys[pygame.K_UP]:
            self.moveUp = True
        if keys[pygame.K_DOWN]:
            self.moveDown = True

    def collisions(self, enemy):
        if self.rect.colliderect(enemy.rect):
            self.lives -= 1
            return True
        else:
            return False

    def move(self):
        global delay
        global playerx

        if delay >= 0:
            delay = 0

            if self.moveRight:
                self.moveRight = False
                if self.rect.x <= WIDTH - 50:
                    self.rect.x += 4
                    playerx = self.rect.x

            if self.moveLeft:
                self.moveLeft = False
                if self.rect.x >= 0:
                    self.rect.x -= 4
                    playerx = self.rect.x

            if self.moveUp:
                self.moveUp = False
                if self.rect.y >= 0:
                    self.rect.y -= 4

            if self.moveDown:
                self.moveDown = False
                if self.rect.y <= HEIGHT - 50:
                    self.rect.y += 4
        else:
            delay += 1

    def draw(self):
        WINDOW.blit(self.surf, self.rect)


class Enemy:
    def __init__(self, x, speed):
        self.x = x
        self.y = 10
        self.speed = speed
        self.direc = 0
        self.surf = pygame.surface.Surface((20, 20))
        self.rect = self.surf.get_rect(midbottom=(self.x, self.y))
        self.surf.fill(GREEN)

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self):
        WINDOW.blit(self.surf, self.rect)


class EnemyTrace:
    def __init__(self, x, speed, tracespeed):
        self.x = x
        self.y = 10
        self.speed = speed
        self.tracespeed = tracespeed
        self.surf = pygame.surface.Surface((20, 20))
        self.rect = self.surf.get_rect(midbottom=(self.x, self.y))
        self.surf.fill(BLUE)

    def move(self, direc):
        self.y += self.speed
        self.rect.y = self.y
        self.x += direc
        self.rect.x = self.x

    def event(self):
        if self.x < playerx:
            direc = self.tracespeed * 1
        elif self.x > playerx:
            direc = self.tracespeed * -1
        else:
            direc = 0

        self.move(direc)

    def draw(self):
        WINDOW.blit(self.surf, self.rect)


class EnemyWave:
    def __init__(self, x, speed, xspeed, max_xspeed):
        self.x = x
        self.y = 10
        self.speed = speed
        self.xspeed = xspeed
        self.max_xspeed = max_xspeed
        self.direc = 1
        self.surf = pygame.surface.Surface((20, 20))
        self.rect = self.surf.get_rect(midbottom=(self.x, self.y))
        self.surf.fill(PURPLE)

    def event(self):
        if self.xspeed >= self.max_xspeed:
            self.direc = -1
        elif self.xspeed <= self.max_xspeed * -1:
            self.direc = 1

        self.xspeed += .1 * self.direc
        self.move()

    def move(self):
        self.y += self.speed
        self.rect.y = self.y
        self.rect.x += self.xspeed

    def draw(self):
        WINDOW.blit(self.surf, self.rect)


def spawn_enemy_normal():
    rand_x = random.randint(0, WIDTH)
    rand_speed = random.randint(1, 3)
    enemies.append(Enemy(rand_x, rand_speed))


def spawn_enemy_trace():
    rand_x = random.randint(0, WIDTH)
    rand_speed = random.randint(1, 2)
    rand_trace_speed = random.randint(1, 3)
    enemies_trace.append(EnemyTrace(rand_x, rand_speed, rand_trace_speed))


def spawn_enemy_wave():
    rand_x = random.randint(0, WIDTH)
    rand_speed = random.randint(2, 6)
    rand_xspeed = rand_speed + random.randint(0, 4)
    rand_max_xspeed = rand_xspeed
    enemies_wave.append(EnemyWave(rand_x, rand_speed, rand_xspeed, rand_max_xspeed))


# naming classes


player = Player()
enemies = []
enemies_trace = []
enemies_wave = []

while True:
    while run_menu:
        WINDOW.blit(TITLE_IMG, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            run_game = True
            break

        # stats board


        pygame.display.update()

    while run_game:
        run_menu = False
        clock.tick(60)
        WINDOW.blit(SPACE_BAK_IMG, (0, 0))

        # quit functionality
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_time += 100

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            run_menu = True
            run_game = False

        # timers
        game_time += 1
        game_time = round(game_time)

        if game_time > 1000:
            roundd = (round(game_time / 1000))
            if game_time > 2000:
                if game_time > 3000:
                    if game_time > 4000:
                        if timer >= (100 - (game_time / 1000) * 10):
                            select = random.randint(1, 10)
                            if select == 1:
                                spawn_enemy_trace()
                            elif 1 < select <= 5:
                                spawn_enemy_wave()
                            else:
                                spawn_enemy_normal()
                            timer = 0
                        else:
                            timer += 1
                    else:
                        if timer >= 50:
                            select = random.randint(1, 10)
                            if 1 <= select <= 5:
                                spawn_enemy_wave()
                            else:
                                spawn_enemy_normal()
                            timer = 0
                        else:
                            timer += 1

                else:
                    if timer >= 45:
                        spawn_enemy_trace()
                        timer = 0
                    else:
                        timer += 1

            else:
                if timer >= 35:
                    spawn_enemy_wave()
                    timer = 0
                else:
                    timer += 1

        else:
            if timer >= 30:
                spawn_enemy_normal()
                timer = 0
            else:
                timer += 1

        # event controls
        player.draw()
        player.move()
        player.event()
        for enemy in enemies:
            if enemy.y >= HEIGHT or player.collisions(enemy):
                indx = enemies.index(enemy)
                enemies.pop(indx)
                score += 1
            enemy.move()
            enemy.draw()

        for enemy in enemies_trace:
            if enemy.y >= HEIGHT or player.collisions(enemy):
                indx = enemies_trace.index(enemy)
                enemies_trace.pop(indx)
                score += 1
            enemy.event()
            enemy.draw()

        for enemy in enemies_wave:
            if enemy.y >= HEIGHT or player.collisions(enemy):
                indx = enemies_wave.index(enemy)
                enemies_wave.pop(indx)
                score += 1
            enemy.event()
            enemy.draw()

        round_text = FONT_SANS.render(f'Round: {roundd + 1}', True, WHITE)
        lives_text = FONT_SANS.render(f'Lives: {player.lives}', True, WHITE)
        score_text = FONT_SANS.render(f'Score: {score}', True, WHITE)

        # screen text
        WINDOW.blit(score_text, (WIDTH / 2 - 40, 20))
        WINDOW.blit(round_text, (20, 20))
        WINDOW.blit(lives_text, (WIDTH - 100, 20))

        num_enemies = len(enemies) + len(enemies_wave) + len(enemies_trace)
        pygame.display.update()



        pygame.display.update()
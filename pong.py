import pygame

WIDHT = 800
HEIGHT = 500

RAQUETE_W = 20
RAQUETE_H = 80
SPEED = 0.5

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDHT, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.player = Player(30, HEIGHT // 2 - RAQUETE_H // 2)
        self.ball = Ball(WIDHT // 2 - 25 // 2, HEIGHT // 2 - 25 // 2)
        self.enemy = Enemy(WIDHT - 45, HEIGHT // 2 - RAQUETE_H // 2)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            self.player.move(keys)
            self.ball.move(self.player, self.enemy)
            self.enemy.move(self.ball.rect, self.ball.dx, self.ball.dy)

            self.screen.fill("black")

            self.enemy.draw(self.screen)
            self.player.draw(self.screen)
            self.ball.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, RAQUETE_W, RAQUETE_H)
        self.speed = 3

    def move(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.dx = -3
        self.dy = -3

    def move(self, player, enemy):
        self.rect.y += self.dy
        self.rect.x += self.dx

        if self.rect.top <= 0:
            self.dy = -self.dy

        if self.rect.bottom >= HEIGHT:
            self.dy = -self.dy

        if self.rect.left <= 0 or self.rect.right >= WIDHT:
            self.dx = 3
            self.dy = 3
            self.rect.x = WIDHT // 2 - self.rect.width // 2
            self.rect.y = HEIGHT // 2 - self.rect.height // 2
            self.dx = -self.dx

        if self.rect.colliderect(player):
            self.dx = -self.dx
            self.dx *= 1.05
            self.dy *= 1.05
        
        if self.rect.colliderect(enemy):
            self.dx = -self.dx
            self.dx *= 1.05
            self.dy *= 1.05

    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.rect)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, RAQUETE_W, RAQUETE_H)
        self.speed = 5
        self.locked = False

    def move(self, ball: pygame.Rect, ball_dx, ball_dy):

        if self.rect.colliderect(ball):
            self.locked = True

        if self.locked:
            if self.rect.centery < HEIGHT // 2:
                self.rect.y += self.speed   # sobe
            elif self.rect.centery > HEIGHT // 2:
                self.rect.y -= self.speed   # desce
            

        if ball.centerx >= WIDHT// 2 and not self.locked:
            if ball_dx > 0:
                if ball_dy > 0 and self.rect.centery < ball.centery:
                    self.rect.y += self.speed
                elif ball_dy < 0 and self.rect.centery > ball.centery:
                    self.rect.y -= self.speed
        
        if ball.centerx < WIDHT // 2:
            self.locked = False


    def draw(self, screen):
        pygame.draw.rect(screen, "white", self.rect)

game = Game()
game.run()
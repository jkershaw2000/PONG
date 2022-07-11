import random

import pygame

from constants import *
from hand_tracking import HandDetector


class Pong:

    def __init__(self, maxScore=MAX_SCORE):
        self.p1Score = -1
        self.p2Score = 0
        self.maxScore = maxScore

        self.handTracking = HandDetector()

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])

        # Create Sprites for game
        self.p1 = Paddle(PADDLE_OFFSET)
        self.p2 = Paddle(WIDTH-PADDLE_OFFSET-PADDLE_WIDTH)
        self.players = (self.p1, self.p2)
        self.ball = Ball(WIDTH//2, HEIGHT // 2)

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.p1)
        self.sprites.add(self.p2)
        self.sprites.add(self.ball)

    def play(self) -> bool:
        close = False
        while (self.p1Score < self.maxScore and self.p2Score < self.maxScore) or close:
            # Allow game to quite
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close = True

            # Movement
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_w]:
            #     self.moveDown(0)
            # if keys[pygame.K_s]:
            #     self.moveUp(0)

            # if keys[pygame.K_UP]:
            #     self.moveDown(1)
            # if keys[pygame.K_DOWN]:
            #     self.moveUp(1)

            p1, p2 = self.handTracking.getNewPositions()
            self.p1.newPaddlePos(HEIGHT*p1)
            self.p2.newPaddlePos(HEIGHT*p2)

            # Check if ball hit the paddle
            if pygame.sprite.collide_mask(self.ball, self.p1) or pygame.sprite.collide_mask(self.ball, self.p2):
                self.ball.dirX *= -1
                self.ball.speed = [random.randint(4, 8), random.randint(-8, 8)]
            else:
                if self.ball.getPosition()[0] <= 0:
                    self.p1Score += 1
                elif self.ball.getPosition()[0] >= WIDTH:
                    self.p2Score += 1
            self.sprites.update()

            # NET
            pygame.draw.line(self.screen, WHITE, [WIDTH//2, 0], [WIDTH//2, 500], 10)

            # Draw Scene
            self.screen.fill(BLACK)

            self.sprites.draw(self.screen)

            font = pygame.font.Font(None, 74)
            text = font.render(str(self.p1Score), 1, WHITE)
            self.screen.blit(text, (WIDTH//4, 15))
            text = font.render(str(self.p2Score), 1, WHITE)
            self.screen.blit(text, (WIDTH//4 * 3, 15))

            pygame.display.flip()
            self.clock.tick(60)

    def moveUp(self, player: int) -> None:
        self.players[player].newPaddlePos(self.players[player].rect.y+PADDLE_SPEED)

    def moveDown(self, player: int) -> None:
        self.players[player].newPaddlePos(self.players[player].rect.y-PADDLE_SPEED)


class Paddle(pygame.sprite.Sprite):

    def __init__(self, posX: int) -> None:
        super().__init__()

        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_LENGTH])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, WHITE, [0, 0, PADDLE_WIDTH, PADDLE_LENGTH])
        self.rect = self.image.get_rect()
        self.rect.x = posX
        self.rect.y = HEIGHT//2

    def newPaddlePos(self, posY) -> None:
        self.rect.y = posY
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > HEIGHT-PADDLE_LENGTH:
            self.rect.y = HEIGHT - PADDLE_LENGTH


class Ball(pygame.sprite.Sprite):

    def __init__(self, posX: int, posY: int) -> None:
        super().__init__()

        self.dirX: int = 1
        self.dirY: int = 1

        self.image = pygame.Surface([BALL_WIDTH, BALL_WIDTH])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.rect(self.image, WHITE, [0, 0, BALL_WIDTH, BALL_WIDTH])
        self.speed = [random.randint(4, 8), random.randint(4, 8)]

        self.rect = self.image.get_rect()

    def getPosition(self) -> tuple[int, int]:
        return self.rect.x, self.rect.y

    def update(self) -> None:
        self.rect.x += self.speed[0] * self.dirX
        self.rect.y += self.speed[1] * self.dirY
        self.isCollision()

    def isCollision(self) -> None:
        # If hit top or bottom change y direction
        if self.rect.y <= 0 or self.rect.y >= HEIGHT:
            self.dirY *= -1

        # If hit left or right change x direction
        if self.rect.x <= 0 or self.rect.x >= WIDTH:
            self.dirX *= -1


if __name__ == "__main__":
    game = Pong()
    game.play()

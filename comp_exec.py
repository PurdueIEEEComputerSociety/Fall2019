import pygame
from random import randint
from paddle import Paddle
from ball import Ball
import ai


class Game():
    def __init__(self, fA, fB, user):
        self.fA = fA        # First program's "getAction" function
        self.fB = fB        # Second program's " "
        self.user = user    # Boolean indicating whether or not to get user input

    def runComp(self):
        self.reset()
        
        pygame.init()
        pygame.display.set_caption("Pong Competition")
        
        while not self.done:
            self.step()
        pygame.quit()
        print("%s wins!" % self.winner)

        pygame.quit()

    def step(self):        
        self.reward = 0

        # PYGAME
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                  self.done = True # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                         self.done=True

        if self.scoreA == 21 or self.scoreB == 21:
            self.winner = "Player A" if self.scoreA == 21 else "Player B"
            self.done = True

        # Getting screen pixels
        rgbarray = pygame.surfarray.array3d(pygame.display.get_surface())

        # Compiling useful information
        info = [rgbarray, self.paddleA.rect, self.paddleB.rect, self.ball.rect, self.reward, self.done]

        # Sending info to first function to get action
        actionA = self.fA(*info)
        self.paddleA.moveUp(actionA)

        # If indicated that user is providing input
        if self.user:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.paddleB.moveUp(10)
            if keys[pygame.K_DOWN]:
                self.paddleB.moveDown(10)
        # If two programs playing against each other
        else:
            actionB = self.fB(info)
            self.paddleB.moveUp(actionB)
            #print(actionB)

        # PYGAME
        if self.paddleB.rect.y > 600 or self.paddleB.rect.y < 100:
            self.paddleB.rect.y = 600 if self.paddleB.rect.y > 600 else 100
        if self.paddleA.rect.y > 600 or self.paddleA.rect.y < 100:
            self.paddleA.rect.y = 600 if self.paddleA.rect.y > 600 else 100
        

        # PYGAME
        self.all_sprites_list.update()
        if self.ball.rect.y>685 or self.ball.rect.y<100:
            self.ball.rect.y = 100 if self.ball.rect.y < 100 else 685
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.x>=490:
            self.scoreA+=1
            self.reward = -1
            self.ball.rect.x = 250
            self.ball.rect.y = 300
            self.ball.velocity = [2 if randint(0, 1) == 0 else -2, 2 if randint(0, 1) == 0 else -2]
        if self.ball.rect.x<=0:
            self.scoreB+=1
            self.reward = 1
            self.ball.rect.x = 250
            self.ball.rect.y = 300
            self.ball.velocity = [2 if randint(0, 1) == 0 else -2, 2 if randint(0, 1) == 0 else -2]
        #Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(self.ball, self.paddleA) or pygame.sprite.collide_mask(self.ball, self.paddleB):
            self.ball.bounce()
        # --- Drawing code should go here
        # First, clear the screen to BLACK.
        self.screen.fill(self.BLACK)
        #Draw the net
        pygame.draw.line(self.screen, self.WHITE, [0, 100], [500, 100], 10)
        #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        self.all_sprites_list.draw(self.screen)
        #Display scores:
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.scoreA), 1, self.WHITE)
        self.screen.blit(text, (125,10))
        text = font.render(str(self.scoreB), 1, self.WHITE)
        self.screen.blit(text, (375,10))

        pygame.display.flip()
        return info

    def reset(self):
        self.size = (500, 700)

        self.BLACK = (144,0,0)
        self.WHITE = (255,255,255)
        self.screen = pygame.display.set_mode(self.size)
        self.paddleA = Paddle(self.WHITE, 10, 100)
        self.paddleA.rect.x = 30
        self.paddleA.rect.y = 300
        self.paddleB = Paddle(self.WHITE, 10, 100)
        self.paddleB.rect.x = 470
        self.paddleB.rect.y = 300
        self.ball = Ball(self.WHITE,20,20)
        self.ball.rect.x = 250
        self.ball.rect.y = 300
        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.paddleA)
        self.all_sprites_list.add(self.paddleB)
        self.all_sprites_list.add(self.ball)
        self.winner = "No one yet"

        self.done = False
        self.scoreA = 0
        self.scoreB = 0

        rgbarray = pygame.surfarray.array3d(pygame.display.get_surface())
        info = [rgbarray, self.paddleA.rect, self.paddleB.rect, self.ball.rect, 0, self.done]

        


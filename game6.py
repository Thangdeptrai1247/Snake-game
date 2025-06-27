import pygame
import random
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 20

WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLACK = (0,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Snake game')

clock = pygame.time.Clock()
FPS = 10
high_score= 0

class Snake:
    def __init__(self):
        self.body = [[100,100],[80,100],[60,100]]
        self.direction = 'RIGHT'

    def change_direction(self,new_dir):
        opposites = {'UP':'DOWN','DOWN':'UP','LEFT':'RIGHT','RIGHT':'LEFT',}
        if new_dir != opposites.get(self.direction):
            self.direction = new_dir

    def move(self):
        x,y = self.body[0]
        if self.direction == 'RIGHT':
            x += BLOCK_SIZE
        elif self.direction == 'LEFT':
            x -= BLOCK_SIZE
        elif self.direction == 'UP':
            y -= BLOCK_SIZE
        elif self.direction == 'DOWN':
            y += BLOCK_SIZE

        x %= SCREEN_WIDTH
        y %= SCREEN_HEIGHT
        
        new_head = [x,y]
        self.body.insert(0, new_head)
        self.body.pop()
    
    def grow(self):
        self.body.append(self.body[-1])
    
    def draw(self, surface):
        for block in self.body:
            pygame.draw.rect(surface, GREEN, (*block, BLOCK_SIZE,BLOCK_SIZE))
    def chance_direction(self, new_dir):
        opposites = {'UP':'"DOWN', 'DOWN':"UP", "LEFT":"RIGHT","RIGHT":"LEFT"}        
        if new_dir != opposites.get(self.direction):
            self.direction = new_dir
    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:] 

class Food:
    def __init__(self,  snake_body,big = False):
        self.big = big   
        self.position = self.random_position(snake_body)
    
    def random_position(self, snake_body):
        while True:
            x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE)// BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE)// BLOCK_SIZE) * BLOCK_SIZE
            pos = [x,y]
            if pos not in snake_body:
                return pos

    def draw(self, surface):
        size = BLOCK_SIZE if not self.big else  int(BLOCK_SIZE*1.5)
        color = RED if not self.big else (255,165,000)
        
        if not self.big:
            rect = pygame.Rect(*self.position, size, size)
        else:
            offset = (size - BLOCK_SIZE)//2
            rect = pygame.Rect( self.position[0] - offset, self.position[1] - offset, size, size)
    
        pygame.draw.rect(surface, color, rect)
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.running = True
        self.score = 0
        self.font = pygame.font.SysFont(None,36)
        self.small_apple_eaten = 0
        self.big_food_active = False
        self.food = Food(self.snake.body)
        

    def process_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.snake.change_direction('UP')
        elif keys[pygame.K_DOWN]:
            self.snake.change_direction('DOWN')
        elif keys[pygame.K_LEFT]:
            self.snake.change_direction('LEFT')
        elif keys[pygame.K_RIGHT]:
            self.snake.change_direction('RIGHT')
    def update(self):
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            if self.food.big:
                self.score += 2
                self.big_food_active = False
                self.small_apple_eaten = 0
            else:
                self.score += 1
                self.small_apple_eaten += 1

            if self.small_apple_eaten >= 5:
                self.food = Food(self.snake.body, big=True)
            else:

                self.food = Food(self.snake.body, big=False)


        if self.snake.check_collision():
            self.running = False

    def draw(self, hight_score):
        screen.fill(BLACK)
        self.snake.draw(screen)
        self.food.draw(screen)
        score_text = f'Score: {self.score} Hight score:{hight_score}'
        score_surface = self.font.render(score_text,True,WHITE)
        screen.blit(score_surface, (10,10))
        pygame.display.update()
       

def show_game_over(score, high_score):
    screen.fill(BLACK)
    game_over_font = pygame.font.SysFont(None, 50)
    msg1 = game_over_font.render("Game over!", True,RED)
    msg2 = game_over_font.render('Press space to play again', True, RED)
    msg3 = game_over_font.render(f'Score{score} High score{high_score}',True, WHITE)
    screen.blit(msg1, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT//2 - 40))
    screen.blit(msg2, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT//2 + 10))
    screen.blit(msg3, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT//2 + 40))
    pygame.display.update()

def wait_for_restart():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False



def main():
    global high_score
    while True:
        game = Game()
        while game.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            game.process_input()
            game.update()
            game.draw(high_score)
            clock.tick(FPS)
        if game.score > high_score:
            high_score = game.score

        show_game_over(game.score, high_score)
        wait_for_restart()


if __name__ == '__main__':
    main()

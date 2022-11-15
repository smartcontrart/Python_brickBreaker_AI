import pygame
import time
import os
import random
import sys
import neat

# Import other classes
sys.path.append("./")
from pad import Pad
from ball import Ball
from brick import Brick



WIN_WIDTH = 800
WIN_HEIGHT = 600

BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background.jpg')),(WIN_WIDTH, WIN_HEIGHT))

PAD_LENGTH = 65
PAD_WIDTH = 15
PAD_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'pad.png')),(PAD_LENGTH, PAD_WIDTH))

BALL_LENGTH = 15
BALL_WIDTH = 15
BALL_IMG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'ball.png')),(BALL_LENGTH, BALL_WIDTH))

BRICK_LENGTH = 50
BRICK_WIDTH = 15
BRICK_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_tile_broken.png')),(BRICK_LENGTH, BRICK_WIDTH)), \
                    pygame.transform.scale(pygame.image.load(os.path.join('assets', 'blue_tile.png')),(BRICK_LENGTH, BRICK_WIDTH)), \
                    pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_tile_broken.png')),(BRICK_LENGTH, BRICK_WIDTH)), \
                    pygame.transform.scale(pygame.image.load(os.path.join('assets', 'red_tile.png')), (BRICK_LENGTH, BRICK_WIDTH))]


LEVEL = [
    [[4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2]],
    [[2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4]],
    [[4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2]],
    [[2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4]],
    [[4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2], [4], [2]]
    ]

def draw_window(win, pads, balls, walls):
    win.blit(BG, (0,0))
    for pad in pads:
        pad.draw(win)
    for ball in balls:
        ball.draw(win)
    for wall in walls:
        for brick in wall:
            if brick.life_points > 0:
                brick.draw(win) 
    pygame.display.update()

def main(genomes, config):

    nets = []
    ge = []
    pads = []
    balls = []
    walls = []
    deaths = len(genomes)

    # print('length genomes')
    # print(len(genomes))
    # print('........')
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    # pad = Pad(300,550, PAD_LENGTH, PAD_WIDTH, PAD_IMG)
    # ball = Ball(300, 350, BALL_LENGTH, BALL_WIDTH, BALL_IMG)
    wall = []
    for row_index, row in enumerate(LEVEL):
        for column_index, column in enumerate(row):
            brick = Brick((column_index + 1) * BRICK_LENGTH, (row_index + 1) * BRICK_WIDTH, column[0], BRICK_LENGTH, BRICK_WIDTH, BRICK_IMGS)
            wall.append(brick)

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        pads.append(Pad(300,550, PAD_LENGTH, PAD_WIDTH, PAD_IMG))
        balls.append(Ball(300, 350, BALL_LENGTH, BALL_WIDTH, BALL_IMG))
        walls.append(wall)
        genome.fitness = 0
        ge.append(genome)
    

    
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for index, ball in enumerate(balls):
            move = ball.move(pads, walls, ge, nets, balls.index(ball))
            if move == 'lost':
                # print(index )
                # deaths += 1
                ge[balls.index(ball)].fitness -= 1
                pads.pop(balls.index(ball))
                walls.pop(balls.index(ball))
                nets.pop(balls.index(ball))
                ge.pop(balls.index(ball))
                balls.pop(balls.index(ball))
        # ball.move(pads, wall, ge, nets)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        if len(pads) <=0:
            run = False
            break 

        for index, pad in enumerate(pads):
            output = nets[index].activate((pad.x, balls[index].x, balls[index].angle))
            if output[0] >= 0:
                pad.move_left()
            if output[0] < 0:
                pad.move_right()
            # if output[0]== 0:
            #     pass

        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_LEFT]:
            # pad.move_left()
        # elif keys[pygame.K_RIGHT]:
            # pad.move_right()

        draw_window(win, pads, balls, walls)
    



def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir =  os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
    


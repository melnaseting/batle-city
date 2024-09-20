from settings import TILE
from classes import Block
import pygame
pygame.init()

txt_map = [
    "111111111111111111111111111111",
    "100001000000000000000000000001",
    "100001000000000000000001100001",
    "100001000000110000100000000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "100000000100000000100011000001",
    "100000000000000000000000000001",
    "100000000000000000000000000001",
    "100001000100000010000000000001",
    "100001000000000010000100000001",
    "100000000000000000000000000001",   
    "100000000001100000000000000001",
    "100000000000000000000000000001",
    "111111111111111111111111111111"
]

def draw_map():
    y,x=0,0
    blocks = pygame.sprite.Group()
    for row in txt_map:
        for char in row:
            if char == "1":
                block = Block("img/block.png",x * TILE,y * TILE,TILE,TILE)
                blocks.add(block)
            x+=1
        x=0
        y+=1
    return blocks
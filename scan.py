import pygame
import numpy as np
from dataclasses import dataclass

pygame.init()

WHITE_THRESHOLD = 400 # max is 440
LOADED_FILE = "images/infared.jpeg"
FONT = pygame.font.SysFont(None,24)
RED = (255,0,0)
TEXT = FONT.render("Target", True, RED)

@dataclass(unsafe_hash=True)
class Bounds:
    min_x: int
    max_x: int
    min_y: int
    max_y: int

WHITE = (255, 255, 255, 255)

def get_color_at_coord(surface: pygame.Surface, x: int, y: int):
    return pygame.Surface.get_at(surface, (x, y))

def find_white_object_bound(surface: pygame.Surface, x, y):
    try:
        color = list(get_color_at_coord(surface, x, y))
    except:
        return []

    color.pop()
        
    if np.linalg.norm(color) < WHITE_THRESHOLD:
        return []
    
    surface.set_at([x,y], (0, 255, 0))
    
    return [[x, y]] + find_white_object_bound(surface, x-1, y) + find_white_object_bound(surface, x+1, y) + find_white_object_bound(surface, x, y-1) + find_white_object_bound(surface, x, y+1) + find_white_object_bound(surface, x-1, y-1) + find_white_object_bound(surface, x+1, y+1) + find_white_object_bound(surface, x-1, y+1) + find_white_object_bound(surface, x+1, y-1)

def get_pixels_bounds(pixels):
    return Bounds(min(pixels, key=lambda x: x[0])[0], max(pixels, key=lambda x: x[0])[0],
        min(pixels, key=lambda y: y[1])[1], max(pixels, key=lambda y: y[1])[1])

def find_white_objects_bounds(surface: pygame.Surface) -> list[tuple[int, int, int, int]]:
    bounds = set()
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            color = get_color_at_coord(surface, x, y)
            if color == WHITE:
                white_pixels = find_white_object_bound(surface, x, y)
                bounds.add(get_pixels_bounds(white_pixels))
    
    return bounds

def draw_red_boxes(surface, bounds: list[Bounds]):
    for bound in bounds:
        pygame.draw.circle(surface, (255, 0, 0), ((bound.max_x+bound.min_x)//2, (bound.max_y+bound.min_y)//2), 5, 3)
        surface.blit(TEXT, (bound.min_x, bound.min_y-10))
        

def main():
    pygame.init()
    image = pygame.image.load(LOADED_FILE)
    SCREEN_WIDTH = image.get_width()
    SCREEN_HEIGHT = image.get_height()
    display_surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    display_surface.blit(image, (0,0))
    bounds = find_white_objects_bounds(display_surface)
    display_surface.blit(image, (0,0))
    draw_red_boxes(display_surface, bounds)

    pygame.image.save(display_surface, "marked_target.png")

if __name__ == "__main__":
    main()
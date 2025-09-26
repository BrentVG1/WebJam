import pygame
from components.collisionObject import CollisionObject
from components.ingredient import Ingredient, IngredientType
from constants import *


class HamburgerStation(CollisionObject):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        super().__init__(x, y, width, height)
        
        self.active = False
        self.progress = 0

        # Load the sprite
        self.sprite = pygame.image.load("sprites/AssemblyTafel2.0.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (width, height))
        
        self.hamburgerItems = {
            "bun": {"present": False, "ingredient": Ingredient(self.x + (self.width / 6) * 1, self.y + self.height / 2, IngredientType.BUN)},
            "patty": {"present": False, "ingredient": Ingredient(self.x + (self.width / 6) * 2, self.y + self.height / 2, IngredientType.PATTY)},
            "lettuce": {"present": False, "ingredient": Ingredient(self.x + (self.width / 6) * 3, self.y + self.height / 2, IngredientType.LETTUCE)},
            "tomato": {"present": False, "ingredient": Ingredient(self.x + (self.width / 6) * 4, self.y + self.height / 2, IngredientType.TOMATO)},
            "cheese": {"present": False, "ingredient": Ingredient(self.x + (self.width / 6) * 5, self.y + self.height / 2, IngredientType.CHEESE)},
        }
        self.hamburgerItems["patty"]["ingredient"].processed = True
        self.hamburgerItems["lettuce"]["ingredient"].processed = True
        self.hamburgerItems["tomato"]["ingredient"].processed = True
        self.hamburger = Ingredient(self.x + self.width / 2, self.y + self.height / 2, IngredientType.HAMBURGER)
        
    def deliverable(self):
        return all(self.hamburgerItems[item]["present"] for item in self.hamburgerItems)
        
    def draw(self, screen, player_x, player_y, vision_radius):
        # Draw the sprite instead of the green rectangle
        screen.blit(self.sprite, (self.x, self.y))
        
        if self.deliverable():
            self.hamburger.draw(screen, player_x, player_y, vision_radius)
        else:
            for item in self.hamburgerItems:
                if self.hamburgerItems[item]["present"]:
                    self.hamburgerItems[item]["ingredient"].draw(screen, player_x, player_y, vision_radius)
            
        # Draw progress if active
        if self.active and self.progress > 0:
            pygame.draw.rect(screen, GREEN, (self.x, self.y + self.height - 10, self.width * (self.progress / 100), 10))
            
    def clear(self):
        for item in self.hamburgerItems:
            self.hamburgerItems[item]["present"] = False

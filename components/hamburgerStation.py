

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
        
        self.hamburgerItems = {
            "bun": {"present": False, "ingredient": Ingredient(self.x + (self.width / 6) * 1, self.y + self.height / 2, IngredientType.BUN)},
            "patty": {"present": True, "ingredient": Ingredient(self.x + (self.width / 6) * 2, self.y + self.height / 2, IngredientType.PATTY)},
            "lettuce": {"present": True, "ingredient": Ingredient(self.x + (self.width / 6) * 3, self.y + self.height / 2, IngredientType.LETTUCE)},
            "tomato": {"present": True, "ingredient": Ingredient(self.x + (self.width / 6) * 4, self.y + self.height / 2, IngredientType.TOMATO)},
            "cheese": {"present": True, "ingredient": Ingredient(self.x + (self.width / 6) * 5, self.y + self.height / 2, IngredientType.CHEESE)},
        }
        self.hamburgerItems["patty"]["ingredient"].processed = True
        self.hamburgerItems["lettuce"]["ingredient"].processed = True
        self.hamburgerItems["tomato"]["ingredient"].processed = True
        self.hamburger = Ingredient(self.x + self.width / 2, self.y + self.height / 2, IngredientType.HAMBURGER)
        
    def deliverable(self):
        return all(self.hamburgerItems[item]["present"] for item in self.hamburgerItems)
        
    def draw(self, screen, player_x, player_y, vision_radius):
        # Draw station background
        color = GREEN
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, LIGHT_GRAY, (self.x, self.y, self.width, self.height), 2)
        
        # Draw station label
        font = pygame.font.SysFont(None, 30)
        text = font.render("Hamburger", True, WHITE)
        screen.blit(text, (self.x + 10, self.y + 10))
        
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
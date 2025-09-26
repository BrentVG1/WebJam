import pygame
from components.collisionObject import CollisionObject
from components.ingredient import IngredientType

class ItemStation(CollisionObject):
    INGREDIENT_IMAGES = {
        IngredientType.LETTUCE: "sprites/Slatafel.png",
        IngredientType.TOMATO: "sprites/tomatentafel.png",
        IngredientType.CHEESE: "sprites/kaastafel.png",
        IngredientType.PATTY: "sprites/Pattytafel.png",
        IngredientType.BUN: "sprites/Bunstafel.png",
    }

    def __init__(self, x, y, width, height, ingredient):
        super().__init__(x, y, width, height)
        self.ingredient = ingredient
        self.active = False
        self.progress = 0

        # Load the ingredient image
        self.image = None
        image_path = self.INGREDIENT_IMAGES.get(self.ingredient.type)
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            except Exception as e:
                print(f"Failed to load image {image_path}: {e}")

    def draw(self, screen, player_x=None, player_y=None, vision_radius=None):
        # Always draw the image if loaded
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # fallback if image not found
            pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height), 2)

        # draw progress bar if active
        if self.active and self.progress > 0:
            pygame.draw.rect(screen, (0, 255, 0),
                             (self.x, self.y + self.height - 10,
                              int(self.width * (self.progress / 100)), 10))

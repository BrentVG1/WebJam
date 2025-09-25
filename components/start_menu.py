# components/start_menu.py
import pygame
import constants


class StartMenu:
    """
    Simple start menu that renders a title + instructions
    and tells the caller when to start/quit.
    """
    def __init__(self):
        # You can keep fonts local to the menu or pass them in from main
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_small = pygame.font.SysFont(None, 36)

    def handle_event(self, event) -> str | None:
        """
        Returns one of:
          - "start"  -> switch to PLAYING
          - "quit"   -> exit the game
          - None     -> no change
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start"
            if event.key == pygame.K_ESCAPE:
                return "quit"
        elif event.type == pygame.QUIT:
            return "quit"
        return None

    def draw(self, screen: pygame.Surface):
        screen.fill(constants.BLACK)

        title = self.font_large.render("HAUNTED KITCHEN", True, constants.GREEN)
        screen.blit(title, (constants.SCREEN_WIDTH // 2 - title.get_width() // 2, 200))

        instructions = [
            "Cook and serve dishes before the kitchen becomes too haunted!",
            "Move with WASD or Arrow Keys",
            "Collect ingredients and take them to stations",
            "Use SPACE at stations to prepare food",
            "Avoid ghosts that follow your footprints",
            "You can only see things in your immediate vicinity",
            "",
            "Press ENTER to start",
            "Press ESC to quit",
            "Press F during game to toggle visibility (debug)",
        ]

        y = 350
        for line in instructions:
            text = self.font_small.render(line, True, constants.WHITE)
            screen.blit(text, (constants.SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 40

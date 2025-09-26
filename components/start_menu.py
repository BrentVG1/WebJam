# components/start_menu.py
import pygame
import constants

class StartMenu:
    """
    Clean start menu that renders the logo and essential instructions.
    """
    def __init__(self):
        # Better font
        self.font_small = pygame.font.SysFont("timesnewroman", 28, bold=True)
        
        # Load the logo
        self.logo = pygame.image.load("sprites/Logo.png").convert_alpha()
        self.logo = pygame.transform.smoothscale(self.logo, (350, 350))

        # Load background image
        self.bg_image = pygame.image.load("sprites/title_screen_bg.png").convert()
        self.bg_image = pygame.transform.smoothscale(
            self.bg_image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )

        # Text styling
        self.instruction_color = (245, 222, 179)  # beige
        self.spacing = 10  # spacing between instructions
        self.text_padding = 10  # padding inside the black background box
        self.corner_radius = 15  # rounded corners

        # Essential instructions
        self.instructions = [
            "Move with WASD or Arrow Keys",
            "Collect ingredients and take them to stations",
            "Use SPACE at stations to prepare food",
            "",
            "Press ENTER to start",
            "Press ESC to quit",
        ]

    def handle_event(self, event) -> str | None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start"
            if event.key == pygame.K_ESCAPE:
                return "quit"
        elif event.type == pygame.QUIT:
            return "quit"
        return None

    def draw(self, screen: pygame.Surface):
        # Draw background image
        screen.blit(self.bg_image, (0, 0))

        # Draw logo centered at top
        logo_x = constants.SCREEN_WIDTH // 2 - self.logo.get_width() // 2
        screen.blit(self.logo, (logo_x, 20))  # keep logo near top

        # Prepare text surfaces
        text_surfaces = [self.font_small.render(line, True, self.instruction_color)
                         for line in self.instructions]

        # Calculate rectangle size that fits text exactly
        max_width = max(surf.get_width() for surf in text_surfaces)
        total_height = sum(surf.get_height() + self.spacing for surf in text_surfaces) - self.spacing

        # Top-left corner fixed offset
        rect_x = 20
        rect_y = 20  # strictly top-left now
        rect_width = max_width + self.text_padding * 2
        rect_height = total_height + self.text_padding * 2

        # Draw rounded rectangle
        pygame.draw.rect(screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height), border_radius=self.corner_radius)

        # Draw each line of text inside the rectangle
        text_y = rect_y + self.text_padding
        for surf in text_surfaces:
            screen.blit(surf, (rect_x + self.text_padding, text_y))
            text_y += surf.get_height() + self.spacing

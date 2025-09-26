# components/start_menu.py
import pygame
import constants

class StartMenu:
    """
    Start menu with logo centered at top.
    Non-control instructions in top-left, control instructions in bottom-right.
    """
    def __init__(self):
        pygame.font.init()
        self.font_small = pygame.font.SysFont("timesnewroman", 28, bold=True)

        # Load the logo
        self.logo = pygame.image.load("sprites/Logo.png").convert_alpha()
        self.logo = pygame.transform.smoothscale(self.logo, (350, 350))  # center top

        # Load background image
        self.bg_image = pygame.image.load("sprites/title_screen_bg.png").convert()
        self.bg_image = pygame.transform.smoothscale(
            self.bg_image, (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )

        # Text styling
        self.instruction_color = (245, 222, 179)  # beige
        self.text_padding = 20
        self.corner_radius = 20
        self.line_spacing = 10

        # Top-left: gameplay info (non-controls)
        self.top_instructions = [
            "Red ghosts follow your footsteps",
            "Blue ghosts patrol the stations",
            "If your burger is ready,",
            "deliver it to the customers",
            "in the safe zone!"
        ]

        # Bottom-right: controls
        self.bottom_instructions = [
            "Move with WASD or Arrow Keys",
            "Hold SHIFT to hide your footsteps",
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

    def draw_box(self, screen, instructions, pos_x, pos_y):
        """Helper to draw a single stylish box with instructions."""
        text_surfaces = [self.font_small.render(line, True, self.instruction_color) for line in instructions]
        max_width = max(surf.get_width() for surf in text_surfaces)
        total_height = sum(surf.get_height() + self.line_spacing for surf in text_surfaces) - self.line_spacing
        box_width = max_width + self.text_padding * 2
        box_height = total_height + self.text_padding * 2

        # Draw semi-transparent box
        s = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(s, (30, 30, 30, 220), (0, 0, box_width, box_height), border_radius=self.corner_radius)
        pygame.draw.rect(s, (245, 222, 179, 200), (2, 2, box_width-4, box_height-4), width=2, border_radius=self.corner_radius)
        screen.blit(s, (pos_x, pos_y))

        # Draw text inside box
        text_y = pos_y + self.text_padding
        for surf in text_surfaces:
            screen.blit(surf, (pos_x + self.text_padding, text_y))
            text_y += surf.get_height() + self.line_spacing

    def draw(self, screen: pygame.Surface):
        # Draw background
        screen.blit(self.bg_image, (0, 0))

        # Draw logo centered at top
        logo_x = constants.SCREEN_WIDTH // 2 - self.logo.get_width() // 2
        logo_y = 40
        screen.blit(self.logo, (logo_x, logo_y))

        # Draw top-left box (non-control instructions)
        self.draw_box(screen, self.top_instructions, 40, 40)

        # Draw bottom-right box (controls)
        bottom_margin = 40
        right_margin = 40
        # Calculate box dimensions
        text_surfaces = [self.font_small.render(line, True, self.instruction_color) for line in self.bottom_instructions]
        max_width = max(surf.get_width() for surf in text_surfaces)
        total_height = sum(surf.get_height() + self.line_spacing for surf in text_surfaces) - self.line_spacing
        box_width = max_width + self.text_padding * 2
        box_height = total_height + self.text_padding * 2
        box_x = constants.SCREEN_WIDTH - box_width - right_margin
        box_y = constants.SCREEN_HEIGHT - box_height - bottom_margin
        self.draw_box(screen, self.bottom_instructions, box_x, box_y)

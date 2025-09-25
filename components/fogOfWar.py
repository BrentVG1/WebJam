import pygame


class FogOfWar:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fog_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.clear_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        self.clear_surface.fill((0, 0, 0, 255))  # Fully opaque black
        
        # Create a vision circle for the player
        self.vision_radius = 250
        self.vision_surface = pygame.Surface((self.vision_radius * 2, self.vision_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.vision_surface, (0, 0, 0, 0), (self.vision_radius, self.vision_radius), self.vision_radius)
        
        # Memory of revealed areas (for persistent visibility of stations)
        self.revealed_areas = set()
        self.station_memory_radius = 100  # How much area around stations stays revealed
        
    def update(self, player_x, player_y, stations):
        # Clear the fog surface
        self.fog_surface.blit(self.clear_surface, (0, 0))
        
        # Add permanently revealed areas around stations
        for station in stations:
            station_pos = (station.x + station.width//2, station.y + station.height//2)
            self.revealed_areas.add(station_pos)
            
            # Create a circle around the station that stays revealed
            station_surface = pygame.Surface((self.station_memory_radius * 2, self.station_memory_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(station_surface, (0, 0, 0, 0), 
                             (self.station_memory_radius, self.station_memory_radius), 
                             self.station_memory_radius)
            
            # Apply the station's revealed area
            self.fog_surface.blit(station_surface, 
                                (station_pos[0] - self.station_memory_radius, 
                                 station_pos[1] - self.station_memory_radius), 
                                special_flags=pygame.BLEND_RGBA_MIN)
        
        # Apply player's current vision
        self.fog_surface.blit(self.vision_surface, 
                            (player_x - self.vision_radius, 
                             player_y - self.vision_radius), 
                            special_flags=pygame.BLEND_RGBA_MIN)
    
    def draw(self, screen):
        screen.blit(self.fog_surface, (0, 0))

import pygame

def play_music():
    pygame.mixer.music.load("Assets\Walen - Vampire Dracula (freetouse.com).mp3")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
import pygame
import random

def play_music():
    music_list = [
        "Assets\\Walen - Vampire Dracula (freetouse.com).mp3",
        "Assets\\Aylex - Arrival (freetouse.com).mp3",
        "Assets\\Aylex - Tension Rising (freetouse.com).mp3",
        "Assets\\Project Ex - Area 16 (freetouse.com).mp3",
        "Assets\\Pufino - Arbiters Trial (freetouse.com).mp3"
    ]

    pygame.mixer.music.load(music_list[random.randint(0, 4)])
    pygame.mixer.music.play(loops=0, start=0.0, fade_ms=0)

    print("Playing a new track!")
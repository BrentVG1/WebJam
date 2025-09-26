import pygame

def play_soundeffect(sound):
    soundeffect_dict = {"step": "Assets\\footsteps-male-362053.mp3",
                        "scream": "Assets\\male-death-scream-horror-352706.mp3"}

    pygame.mixer.Sound(soundeffect_dict[sound]).play()
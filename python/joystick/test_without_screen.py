import os
import time
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()
pygame.joystick.init()
joyController = pygame.joystick.Joystick(0)
joyController.init()

while True:
	for event in pygame.event.get():
		print(event)
	"""
	for i in range(joyController.get_numaxes()):
        	print(f'Axis {i}: {joyController.get_axis(i)}')
	"""

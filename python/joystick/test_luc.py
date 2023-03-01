import pygame

# Initialisation de pygame
pygame.init()

# Récupération de la liste des joysticks connectés
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("Aucun joystick n'est connecté à votre ordinateur")
    quit()

# Récupération du premier joystick de la liste
joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Le joystick '{}' est connecté à votre ordinateur".format(joystick.get_name()))

# Boucle principale
while True:
    # Traitement des événements
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            print("Le joystick a été bougé")

    # Mise à jour de l'affichage
    pygame.display.update()

# Terminaison de pygame
pygame.quit()

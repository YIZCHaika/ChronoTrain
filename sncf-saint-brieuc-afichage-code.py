import pygame
import time
import requests

# --- Configuration API SNCF ---
API_KEY = "0fbf3cad-2179-4195-bd01-8ad080fe453b"
URL = "https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:SNCF:87473009/departures"

def get_departures():
    try:
        response = requests.get(URL, auth=(API_KEY, ""))
        data = response.json()
        trains = []
        for dep in data["departures"][:6]:
            heure = dep["stop_date_time"]["departure_date_time"][9:13]
            heure = heure[:2] + ":" + heure[2:]
            destination = dep["display_informations"]["direction"]
            num = dep["display_informations"]["headsign"]
            trains.append((heure, num, destination))
        return trains
    except Exception as e:
        print("Erreur récupération données:", e)
        return []

# --- Initialisation Pygame ---
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Départs Saint-Brieuc")

background = pygame.image.load("image_sncf_2.jpg")
background = pygame.transform.scale(background, (1920, 1080))

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

font_titre = pygame.font.SysFont("Arial", 40, bold=True)
font = pygame.font.SysFont("Arial", 32)

running = True
last_update = 0
trains = []

# --- Boucle principale ---
while running:
    # Mise à jour des données toutes les 30 secondes
    if time.time() - last_update > 30:
        trains = get_departures()
        last_update = time.time()

    # Fond
    screen.blit(background, (0, 0))

    # Titre
    titre = font_titre.render("Prochains départs - Saint-Brieuc", True, NOIR)
    screen.blit(titre, (550, 20))

    # --- Tableau dynamique ---
    if trains:
        top_y = 100
        line_height = 100
        lignes = [f"{h}   {num}   {dest}   " for h, num, dest in trains]

        # Trouver la largeur max du texte
        largeurs = [font.size(ligne)[0] for ligne in lignes]
        max_width = max(largeurs) + 125  # +40 px de marge

        # Calculer hauteur totale
        box_height = len(lignes) * line_height + 60
        # Dessiner rectangle arrondi
        rect = pygame.Rect(450, top_y, max_width, box_height)
        pygame.draw.rect(screen, BLANC, rect, border_radius=20)

        # Afficher les lignes
        y = top_y + 60
        for ligne in lignes:
            texte = font.render(ligne, True, NOIR)
            screen.blit(texte, (500, y))
            y += line_height

    else:
        # Aucun départ
        msg = "Aucun départ disponible"
        largeur = font.size(msg)[0] + 40
        rect = pygame.Rect(40, 110, largeur, 80)
        pygame.draw.rect(screen, BLANC, rect, border_radius=20)
        texte = font.render(msg, True, NOIR)
        screen.blit(texte, (50, 120))

    # Rafraîchir l’écran
    pygame.display.flip()

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    time.sleep(1)

pygame.quit()
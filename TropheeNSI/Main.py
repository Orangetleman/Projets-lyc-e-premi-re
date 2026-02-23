import pyxel
from collections import namedtuple

# =============================================================================
# CONSTANTES ET PARAMÈTRES DU JEU
# =============================================================================
SPEED = 3                     # Vitesse de déplacement des joueurs
BULLET_SPEED = 7              # Vitesse des balles tirées
RESPAWN_TIME = 5 * 30         # Temps de réapparition (5 seondes à 30 fps)
TILE_SIZE = 40                # Taille d'une case de territoire
GAME_DURATION = 180 * 30      # Durée de la partie en frames (3 minutes à 30 fps)

# =============================================================================
# STRUCTURES DE DONNÉES
# =============================================================================
# Structure représentant un joueur
Player = namedtuple("Player", ["x", "y", "width", "height", "keyset", "direction",
                               "respawn_timer", "spawn_x", "spawn_y", "sprite", "team"])
# Structure représentant une balle
Bullet = namedtuple("Bullet", ["x", "y", "width", "height", "direction", "owner", "color"])
# Structure représentant un obstacle
Obstacle = namedtuple("Obstacle", ["x", "y", "width", "height"])
# Structure pour la zone de protection autour des spawns
SpawnProtection = namedtuple("SpawnProtection", ["x", "y", "width", "height", "team"])

# =============================================================================
# VARIABLES GLOBALES
# =============================================================================
game_timer = GAME_DURATION   # Timer de la partie (en frames)
game_over = False            # Indique si la partie est terminée (pause avec interface)
score_blue = 0               # Score de l'équipe bleue (team 5)
score_red = 0                # Score de l'équipe rouge (team 8)
grid_state = {}              # Etat du territoire (clé: (col, row), valeur: team)

players = []     # Liste des joueurs
bullets = []     # Liste des balles tirées
obstacles = []   # Liste des obstacles de la carte
spawn_protections = []  # Zones de protection autour des spawns

# =============================================================================
# FONCTION DE RÉINITIALISATION DU JEU
# Réinitialise toutes les variables pour démarrer une nouvelle partie
# =============================================================================
def reset_game():
    global game_timer, game_over, score_blue, score_red, grid_state, players, bullets, obstacles, spawn_protections

    game_timer = GAME_DURATION
    game_over = False
    score_blue = 0
    score_red = 0
    grid_state = {}

    # Définition des obstacles fixes sur la map
    obstacles = [
        Obstacle(0, 0, 1000, 40),
        Obstacle(0, 0, 40, 520),
        Obstacle(960, 0, 40, 520),
        Obstacle(0, 480, 1000, 40),
        Obstacle(200, 0, 40, 200),
        Obstacle(760, 320, 40, 200),
        Obstacle(560, 240, 40, 120),
        Obstacle(400, 160, 40, 120),
        Obstacle(560, 240, 80, 40),
        Obstacle(360, 240, 80, 40),
        Obstacle(240, 320, 80, 40),
        Obstacle(280, 400, 200, 40),
        Obstacle(280, 360, 40, 40),
        Obstacle(440, 360, 40, 40),
        Obstacle(680, 160, 80, 40),
        Obstacle(520, 80, 200, 40),
        Obstacle(520, 120, 40, 40),
        Obstacle(680, 120, 40, 40),
    ]

    # Initialisation des joueurs avec leurs positions de spawn, touches et sprites
    players = [
        Player(100, 100, 32, 32,
               {"left": pyxel.KEY_Q, "right": pyxel.KEY_D,
                "up": pyxel.KEY_Z, "down": pyxel.KEY_S, "shoot": pyxel.KEY_E},
               "right", 0, 100, 100,
               {"img": 0, "u": 0, "v": 0, "w": 32, "h": 32}, 5),
        Player(100, 380, 32, 32,
               {"left": pyxel.KEY_F, "right": pyxel.KEY_H,
                "up": pyxel.KEY_T, "down": pyxel.KEY_G, "shoot": pyxel.KEY_Y},
               "right", 0, 100, 380,
               {"img": 0, "u": 32, "v": 0, "w": 32, "h": 32}, 5),
        Player(860, 380, 32, 32,
               {"left": pyxel.KEY_J, "right": pyxel.KEY_L,
                "up": pyxel.KEY_I, "down": pyxel.KEY_K, "shoot": pyxel.KEY_O},
               "left", 0, 860, 380,
               {"img": 0, "u": 64, "v": 0, "w": 32, "h": 32}, 8),
        Player(860, 100, 32, 32,
               {"left": pyxel.KEY_LEFT, "right": pyxel.KEY_RIGHT,
                "up": pyxel.KEY_UP, "down": pyxel.KEY_DOWN, "shoot": pyxel.KEY_RSHIFT},
               "left", 0, 860, 100,
               {"img": 0, "u": 96, "v": 0, "w": 32, "h": 32}, 8)
    ]

    # Réinitialisation de la liste des balles
    bullets = []

    # Calcul des zones de protection des spawns pour éviter de tirer directement dessus
    spawn_protections = [SpawnProtection(p.spawn_x - p.width, p.spawn_y - p.height,
                                          p.width * 3 + 2, p.height * 3 + 2, p.team)
                         for p in players]

# =============================================================================
# INITIALISATION DE PYXEL
# =============================================================================
pyxel.init(1000, 520, "Bobs", display_scale=1)
pyxel.load('Skins.pyxres')
reset_game()

# Introduction de la musique de fond
pyxel.playm(0,None,True)

# =============================================================================
# FONCTION DE DÉTECTION DE COLLISION
# Renvoie True si les deux objets se chevauchent, sinon False
# =============================================================================
def check_collision(obj1, obj2):
    return not (obj1.x + obj1.width <= obj2.x or
                obj1.x >= obj2.x + obj2.width or
                obj1.y + obj1.height <= obj2.y or
                obj1.y >= obj2.y + obj2.height)

# =============================================================================
# FONCTION DE MISE À JOUR DE L'ÉTAT DU JEU
# Gère les entrées, les mouvements, la capture du territoire, le tir,
# la gestion du timer et l'interface de fin de partie en pause.
# =============================================================================
def update():
    global players, bullets, obstacles, grid_state, game_timer, game_over, score_blue, score_red

    # Permet de quitter le jeu à tout moment avec la touche ESCAPE
    if pyxel.btnp(pyxel.KEY_ESCAPE):
        pyxel.quit()

    # Si la partie est terminée (en pause), on gère les actions de fin de partie
    if game_over:
        # Touche "W" pour recommencer la partie
        if pyxel.btnp(pyxel.KEY_W):
            reset_game()
        # Touche "X" pour fermer le jeu
        elif pyxel.btnp(pyxel.KEY_X):
            pyxel.quit()
        return

    # -------------------------------------------------------------------------
    # MISE À JOUR DU TIMER DE JEU
    # -------------------------------------------------------------------------
    game_timer -= 1
    if game_timer <= 0:
        game_over = True

    # -------------------------------------------------------------------------
    # MISE À JOUR DES JOUEURS
    # -------------------------------------------------------------------------
    new_players = []
    for player in players:
        # Si le joueur est en période de respawn, on décrémente son timer
        if player.respawn_timer > 0:
            new_players.append(player._replace(respawn_timer=player.respawn_timer - 1))
            continue

        new_x, new_y = player.x, player.y
        # Détection des touches de déplacement et mise à jour de la direction
        if pyxel.btn(player.keyset['left']):
            new_x -= SPEED
            direction = "left"
        elif pyxel.btn(player.keyset['right']):
            new_x += SPEED
            direction = "right"
        elif pyxel.btn(player.keyset['up']):
            new_y -= SPEED
            direction = "up"
        elif pyxel.btn(player.keyset['down']):
            new_y += SPEED
            direction = "down"
        else:
            direction = player.direction

        # Vérification de collision avec les obstacles ou autres joueurs
        if not any(check_collision(player._replace(x=new_x, y=new_y), obs)
                   for obs in obstacles + [p for p in players if p != player]):
            player = player._replace(x=new_x, y=new_y, direction=direction)
        new_players.append(player)

        # ---------------------------------------------------------------------
        # CAPTURE DU TERRITOIRE
        # Pour chaque joueur, on vérifie les cases couvertes par sa hitbox
        # et on met à jour le score :
        #   - Si la case est neutre, +1 pour l'équipe.
        #   - Si la case appartient à l'adversaire, +1 pour l'équipe et -1 pour l'adversaire.
        # ---------------------------------------------------------------------
        covered_tiles = set()  # Évite de compter plusieurs fois la même case
        corners = [
            (new_x, new_y),                           # coin supérieur gauche
            (new_x + player.width, new_y),            # coin supérieur droit
            (new_x, new_y + player.height),           # coin inférieur gauche
            (new_x + player.width, new_y + player.height)  # coin inférieur droit
        ]
        for cx, cy in corners:
            grid_col = int(cx // TILE_SIZE)
            grid_row = int(cy // TILE_SIZE)
            tile = (grid_col, grid_row)
            if 0 <= grid_col < 25 and 0 <= grid_row < 13 and tile not in covered_tiles:
                covered_tiles.add(tile)
                prev_owner = grid_state.get(tile, None)
                if prev_owner != player.team:
                    grid_state[tile] = player.team
                    if prev_owner is None:
                        # Capture d'une case neutre
                        if player.team == 5:
                            score_blue += 1
                        else:
                            score_red += 1
                    else:
                        # Capture sur une case adverse
                        if player.team == 5:
                            score_blue += 1
                            score_red -= 1
                        else:
                            score_red += 1
                            score_blue -= 1

        # ---------------------------------------------------------------------
        # GESTION DU TIR
        # Calcul de la position de départ de la balle selon la direction et
        # ajout de la balle si la touche de tir est pressée.
        # ---------------------------------------------------------------------
        if pyxel.btnp(player.keyset['shoot']):
            if direction == "right":
                bullet_x = player.x + player.width
                bullet_y = player.y + (player.height - 5) // 2
                bullets.append(Bullet(bullet_x, bullet_y, 10, 5, direction, player, player.team))
            elif direction == "left":
                bullet_x = player.x - 10
                bullet_y = player.y + (player.height - 5) // 2
                bullets.append(Bullet(bullet_x, bullet_y, 10, 5, direction, player, player.team))
            elif direction == "up":
                bullet_x = player.x + (player.width - 5) // 2
                bullet_y = player.y - 10
                bullets.append(Bullet(bullet_x, bullet_y, 5, 10, direction, player, player.team))
            elif direction == "down":
                bullet_x = player.x + (player.width - 5) // 2
                bullet_y = player.y + player.height
                bullets.append(Bullet(bullet_x, bullet_y, 5, 10, direction, player, player.team))
    players = new_players

    # -------------------------------------------------------------------------
    # MISE À JOUR DES BALLES
    # Déplacement, détection de collision avec obstacles, zones de protection
    # et joueurs. En cas d'impact sur un joueur adverse, le joueur touché est
    # transformé en obstacle et son respawn est activé.
    # -------------------------------------------------------------------------
    new_bullets = []
    for bullet in bullets:
        new_x, new_y = bullet.x, bullet.y
        if bullet.direction == "left":
            new_x -= BULLET_SPEED
        elif bullet.direction == "right":
            new_x += BULLET_SPEED
        elif bullet.direction == "up":
            new_y -= BULLET_SPEED
        elif bullet.direction == "down":
            new_y += BULLET_SPEED
        new_bullet = bullet._replace(x=new_x, y=new_y)
        if any(check_collision(new_bullet, sp) for sp in spawn_protections):
            continue
        if any(check_collision(new_bullet, obs) for obs in obstacles):
            continue
        hit_players = [p for p in players if p != bullet.owner and check_collision(new_bullet, p)]
        if hit_players:
            for p in hit_players:
                obstacles.append(Obstacle(p.x, p.y, p.width, p.height))
                players[:] = [pl._replace(respawn_timer=RESPAWN_TIME, x=pl.spawn_x, y=pl.spawn_y)
                              if pl == p else pl for pl in players]
            continue
        new_bullets.append(new_bullet)
    bullets = new_bullets
    

# =============================================================================
# FONCTION D'AFFICHAGE (DRAW)
# Affiche le jeu, l'interface in-game et, en fin de partie, l'interface
# de pause avec les scores, le vainqueur et les instructions pour reprendre ou
# quitter.
# =============================================================================
def draw():
    # Efface l'écran avec la couleur neutre (11)
    pyxel.cls(11)

    # -------------------------------------------------------------------------
    # SI LA PARTIE EST EN COURS, AFFICHAGE DU JEU ET DE L'INTERFACE IN-GAME
    # -------------------------------------------------------------------------
    if not game_over:
        # Affichage de la grille de territoire
        for grid_col in range(25):
            for grid_row in range(13):
                x = grid_col * TILE_SIZE
                y = grid_row * TILE_SIZE
                color = grid_state.get((grid_col, grid_row), 11)  # 11 = neutre
                pyxel.rect(x, y, TILE_SIZE, TILE_SIZE, color)
        # Dessin du quadrillage
        for x in range(0, 1000, TILE_SIZE):
            pyxel.line(x, 0, x, 520, 3)
        for y in range(0, 520, TILE_SIZE):
            pyxel.line(0, y, 1000, y, 3)
        # Affichage des zones de protection des spawns
        for protection in spawn_protections:
            col = 1 if protection.team == 5 else 2
            pyxel.rectb(protection.x, protection.y, protection.width, protection.height, col)
        # Affichage des obstacles
        for obstacle in obstacles:
            pyxel.rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height, 3)
        # Affichage des joueurs avec rotation selon leur direction
        for player in players:
            if player.respawn_timer == 0:
                if player.direction == "left":
                    pyxel.blt(player.x, player.y,
                              player.sprite["img"],
                              player.sprite["u"],
                              player.sprite["v"],
                              -player.sprite["w"],
                              player.sprite["h"],
                              colkey=11)
                elif player.direction == "up":
                    pyxel.blt(player.x, player.y,
                              player.sprite["img"],
                              player.sprite["u"],
                              player.sprite["v"],
                              player.sprite["w"],
                              -player.sprite["h"],
                              colkey=11)
                else:
                    pyxel.blt(player.x, player.y,
                              player.sprite["img"],
                              player.sprite["u"],
                              player.sprite["v"],
                              player.sprite["w"],
                              player.sprite["h"],
                              colkey=11)
        # Affichage des balles
        for bullet in bullets:
            pyxel.rect(bullet.x, bullet.y, bullet.width, bullet.height, bullet.color)

        # ---------------------------------------------------------------------
        # INTERFACE IN-GAME : affichage d'un overlay pour le timer et les scores
        # ---------------------------------------------------------------------
        # Fond semi-transparent pour l'interface (zone en haut à gauche)

        pyxel.rectb(300, 10, 2, 6, 5)
        pyxel.rectb(300, 10, 2, 6, 5)
        pyxel.rectb(300, 10, 2, 6, 5)
        # Affichage du timer en secondes
        seconds = game_timer // 30
        pyxel.text(500, 20, f"Timer: {seconds:3d} sec", 7)
        # Affichage des scores
        pyxel.text(400, 20, f"Score Bleu : {score_blue}", 5)
        pyxel.text(600, 20, f"Score Rouge: {score_red}", 8)
    else:
        # ---------------------------------------------------------------------
        # INTERFACE DE FIN DE PARTIE
        # Affiche les scores finaux, le vainqueur et les instructions pour
        # recommencer ou quitter.
        # ---------------------------------------------------------------------
        pyxel.cls(1)  # Fond sombre pour l'interface de pause
        # Boîte de dialogue centrale
        pyxel.rect(300, 150, 400, 250, 7)
        pyxel.rectb(300, 150, 400, 250, 0)
        pyxel.text(380, 170, "Fin de la partie", 0)
        pyxel.text(320, 200, f"Score Bleu : {score_blue}", 5)
        pyxel.text(320, 220, f"Score Rouge: {score_red}", 8)
        # Détermination du vainqueur
        if score_blue > score_red:
            winner = "Bleu"
        elif score_red > score_blue:
            winner = "Rouge"
        else:
            winner = "Egalité"
        pyxel.text(320, 250, f"Vainqueur: {winner}", 0)
        # Instructions
        pyxel.text(320, 280, "Appuyez sur W pour recommencer", 0)
        pyxel.text(320, 300, "ou sur X pour quitter", 0)

# =============================================================================
# BOUCLE PRINCIPALE DU JEU
# =============================================================================
pyxel.run(update, draw)

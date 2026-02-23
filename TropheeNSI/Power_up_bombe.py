
POWER_UP_TIME = 300
PowerUpBombe = namedtuple("PowerUpBombe", ["x", "y", "timer"])
power_up_bombe = None

def create_power_up():
    import random
    x = random.randint(100, 900)
    y = random.randint(100, 400)
    return PowerUpBombe(x, y, POWER_UP_TIME)

def update_power_up_bombe(players):
    global power_up_bombe

    if power_up_bombe is None:
        power_up_bombe = create_power_up()

    if power_up_bombe.timer > 0:
        power_up_bombe = power_up_bombe._replace(timer=power_up_bombe.timer - 1)
    else:
        power_up_bombe = None

    for player in players:
        if power_up_bombe and check_collision(player, power_up_bombe):
            players = [pl._replace(respawn_timer=RESPAWN_TIME, x=pl.spawn_x, y=pl.spawn_y) if pl == p else pl for pl in players] #j ai pas capte comment ca marche pour ce truc
            power_up_bombe = None


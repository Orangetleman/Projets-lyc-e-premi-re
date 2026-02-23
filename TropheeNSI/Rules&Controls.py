import pyxel
import subprocess

pyxel.init(1000, 520, "Bobs", display_scale=1)

def update():

    visible = True
    pyxel.mouse(visible)
    # Fermer le programme
    if pyxel.btnp(pyxel.KEY_ESCAPE):
        pyxel.quit()

#=================================================
#|   Création de l'interaction avec le bouton    |
#=================================================
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 10 <= pyxel.mouse_x <= 110 and 480 <= pyxel.mouse_y <= 510:
        subprocess.run(["python", "Start.py"])
        pyxel.quit()

#====================================
#|   Création visuel des boutons    |
#====================================
def draw():
    pyxel.cls(11)
    pyxel.text(10,10,"The objective is to color as much squares in the color of your team as possible before the end of the timer. You cen kill the opponent team by firing a bullet.", 3)
    pyxel.text(10,25,"You will be given 3 minutes. Killing an opponent turns them into stone. You cannot fire bullets within the spawn shield nor be killed in it.", 3)
    pyxel.text(10,45,"CONTROLS :", 3)
    pyxel.text(10,60,"Paint : left = Q, right = D, up = Z, down = S, shoot = E", 3)
    pyxel.text(10,75,"Sculpture : left = F, right = H, up = T, down = G, shoot = Y", 3)
    pyxel.text(10,90,"Music : left = J, right = L, up = I, down = K, shoot = O", 3)
    pyxel.text(10,105,"Cinema : left = ARROWLEFT, right = ARROWRIGHT, up = ARROWUP, down = ARRROWDOWN, shoot = RIGHTSHIFT", 3)
    pyxel.rect(10,480,100,30,3)
    pyxel.text(30,490,"<=  Back",11)

pyxel.run(update,draw)
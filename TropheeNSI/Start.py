import pyxel
import subprocess

pyxel.init(1000, 520, "Bobs", display_scale=1)

def update():

    visible = True
    pyxel.mouse(visible)
    # Fermer le programme
    if pyxel.btnp(pyxel.KEY_ESCAPE):
        pyxel.quit()
#===================================================
#|   Création des interactions avec les boutons    |
#===================================================
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 350 <= pyxel.mouse_x <= 650 and 50 <= pyxel.mouse_y <= 130:
        subprocess.run(["python", "Main.py"]) # Redirection vers un autre fichier
        pyxel.quit()

    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 350 <= pyxel.mouse_x <= 650 and 150 <= pyxel.mouse_y <= 230:
        subprocess.run(["python", "Rules&Controls.py"]) # Redirection vers un autre fichier
        pyxel.quit()

    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 350 <= pyxel.mouse_x <= 650 and 250 <= pyxel.mouse_y <= 330:
        subprocess.run(["python", "Credits.py"]) # Redirection vers un autre fichier
        pyxel.quit()

#====================================
#|   Création visuel des boutons    |
#====================================
def draw():
    pyxel.cls(11)
    pyxel.rect(350,50,300,80,3)
    pyxel.text(400,70,"Start",11)
    pyxel.rect(350,150,300,80,3)
    pyxel.text(400,170,"Rules & Controls",11)
    pyxel.rect(350,250,300,80,3)
    pyxel.text(400,270,"Credits",11)

pyxel.run(update,draw)
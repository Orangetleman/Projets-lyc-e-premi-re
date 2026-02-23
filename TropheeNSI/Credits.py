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
    pyxel.text(10,10,"Thank you to our CEO, project manager, secondary programmer, secondary graphist, manager and coach Eva !", 3)
    pyxel.text(10,25,"Thank you to our main programmer and employee of the month Christophe !", 3)
    pyxel.text(10,40,"Thank you to our third programmer, graphist assistant and employee Gabriel !", 3)
    pyxel.text(10,55,"And last but not least, thank you to our main graphist, programmer assistant, secondary coach and best intern Adam!", 3)
    pyxel.text(10,75,"We would also like to give a round of applause to our teacher, who was always here to answer our questions (even in the darkest nights) and present us new projects and challenges", 3)
    pyxel.rect(10,480,100,30,3)
    pyxel.text(30,490,"<=  Back",11)

pyxel.run(update,draw)
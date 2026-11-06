
from tkinter import *
import time

# Variables globales
timer_started = False
start_time = 0

# Texte à recopier
sample_text = "Python is a powerful programming language. It is easy to learn and fun to use."


# 1. Fonction pour démarrer le timer
def start_timer(event):
    global timer_started, start_time

    if not timer_started:
        start_time = time.time()
        timer_started = True
        update_timer()


# 2. Fonction pour actualiser le timer
def update_timer():
    if timer_started:
        elapsed_time = time.time() - start_time

        seconds = int(elapsed_time)

        timer_label.config(text=f"Time: {seconds} seconds")

        # Actualiser après une seconde
        window.after(1000, update_timer)


# 3. Fonction pour vérifier le texte
def check_text():
    typed_text = user_input.get("1.0", END).strip()

    if not timer_started:
        result_label.config(text="Please start typing first!")
        return

    if typed_text == sample_text:
        end_time = time.time()

        elapsed_time = end_time - start_time
        minutes = elapsed_time / 60

        words = len(typed_text.split())
        wpm = words / minutes

        result_label.config(
            text=f"Your typing speed: {wpm:.2f} WPM"
        )

    else:
        result_label.config(
            text="You made some mistakes. Please check your text."
        )

# 4. Fonction pour recommencer le test
def restart_test():
    global timer_started, start_time

    user_input.delete("1.0", END)

    timer_started = False
    start_time = 0

    timer_label.config(text="Time: 0 seconds")
    result_label.config(text="Start typing the text!")


# 5. Création de la fenêtre
window = Tk()
window.title("Typing Speed Test")
window.geometry("650x450")
window.config(padx=20, pady=20)


# 6. Titre
title_label = Label(
    window,
    text="Typing Speed Test",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=10)


# 7. Affichage du timer
timer_label = Label(
    window,
    text="Time: 0 seconds",
    font=("Arial", 14, "bold")
)
timer_label.pack(pady=10)


# 8. Texte à recopier
sample_label = Label(
    window,
    text=sample_text,
    wraplength=550,
    font=("Arial", 12)
)
sample_label.pack(pady=15)


# 9. Zone de saisie
user_input = Text(
    window,
    height=5,
    width=65,
    font=("Arial", 12)
)
user_input.pack(pady=10)


# Détecter la première frappe
user_input.bind("<KeyPress>", start_timer)


# 10. Bouton pour vérifier la vitesse
check_button = Button(
    window,
    text="Check my speed",
    command=check_text
)
check_button.pack(pady=10)


# 11. Affichage du résultat
result_label = Label(
    window,
    text="Start typing the text!",
    font=("Arial", 12, "bold")
)
result_label.pack(pady=10)


# 12. Bouton pour recommencer
restart_button = Button(
    window,
    text="Restart",
    command=restart_test
)
restart_button.pack(pady=5)


# Lancer l'application
window.mainloop()

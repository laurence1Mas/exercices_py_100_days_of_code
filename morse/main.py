code_morse ={
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--.."
}
# fonction pour convertir le texte en code morse
def morse_code(text):
    """
    Convertit un texte en code morse.

    """
    text = input("entrer un mot: ").upper()
    morse_text = ""
    for chat in text:
        if chat in code_morse:
            #-- QUE Fait cette ligne ? --#
            # Cette ligne ajoute le code morse correspondant à la lettre actuelle (chat)
            #  à la variable morse_text, suivi d'un espace pour séparer les lettres en code morse.
            morse_text += code_morse[chat] + " "
        else:
            morse_text += " "
    return morse_text

morse_text = morse_code("")
print(morse_text)

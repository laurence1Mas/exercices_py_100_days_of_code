
from pathlib import Path

from PIL import Image, ImageDraw

script_dir = Path(__file__).resolve().parent

# 1. Ouvrir une image
image = Image.open(script_dir / "laure-img.jpg")

# 2. Créer un objet pour dessiner sur l'image
draw = ImageDraw.Draw(image)

# 3. Ajouter un texte sur l'image
draw.text((200, 100), "Laurence-Mak", fill="white")

# 4. Enregistrer la nouvelle image
image.save(script_dir / "watermarked_photo.jpg")

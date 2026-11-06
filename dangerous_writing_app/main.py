
from tkinter import *

# Create the main window
window = Tk()
window.title("Dangerous Writing App")
window.geometry("800x600")
window.config(padx=30, pady=30)

# Application title
title_label = Label(
    window,
    text="The Most Dangerous Writing App",
    font=("Arial", 20, "bold")
)
title_label.pack(pady=15)

# Timer label
timer_label = Label(
    window,
    text="Start writing...",
    font=("Arial", 14)
)
timer_label.pack(pady=10)

# Text area
text_area = Text(
    window,
    width=80,
    height=20,
    font=("Arial", 12),
    wrap="word"
)
text_area.pack(pady=15)

window.mainloop()

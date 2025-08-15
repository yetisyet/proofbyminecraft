import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Proof by Minecraft")

# Load the redstone block image for the banner
image = tk.PhotoImage(file=r"H:\My Drive\Uni\Other\Computer Science\Hackathons\2025\redstone_lamp.png")

tk.Label(root, image=image).pack()

# Input frame
input_frame = tk.Frame(root, width=1000, height=400, bg="skyblue")
input_frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)
tk.Label(
    input_frame,
    text="Input",
    bg="skyblue",
).pack(padx=5, pady=5)
thumbnail_image = image.subsample(5, 5)

# Add a Text widget for user input within the input_frame
input_text = tk.Text(input_frame, height=10, width=25)
input_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# 1 Statement evaluation / 2 Statement evaluation mode switch tab
notebook = ttk.Notebook(input_frame)
notebook.pack(expand=True, fill="both")

statements_tab = tk.Frame(notebook, bg="lightblue")
statements_var = tk.StringVar(value="None")
for tool in ["1 Statement Evaluation", "2 Statement Evaluation/Comparison"]:
    tk.Radiobutton(
        statements_tab,
        text=tool,
        variable=statements_var,
        value=tool,
        bg="lightblue",
    ).pack(anchor="w", padx=5, pady=5)

arguments_tab = tk.Frame(notebook, bg="lightgreen")
arguments_var = tk.StringVar(value="None")
for argument in ["Placeholder 1", "Placeholder 2"]:
    tk.Radiobutton(
        arguments_tab,
        text=argument,
        variable=arguments_var,
        value=argument,
        bg="lightgreen",
    ).pack(anchor="w", padx=5, pady=5)

notebook.add(statements_tab, text="Logic Statements")
notebook.add(arguments_tab, text="Logical Arguments")

# Image frame
image_frame = tk.Frame(root, width=400, height=400, bg="grey")
image_frame.pack(padx=5, pady=5, side=tk.RIGHT)
display_image = image.subsample(2, 2)
tk.Label(
    image_frame,
    text="Output",
    bg="grey",
    fg="white",
).pack(padx=5, pady=5)
tk.Label(image_frame, image = tk.PhotoImage(file=r"H:\My Drive\Uni\Other\Computer Science\Hackathons\2025\redstone_lamp.png")).pack(padx=5, pady=5)

root.mainloop()

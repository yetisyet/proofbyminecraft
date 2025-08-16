import customtkinter as ctk
import tkinter as tk
from PIL import Image
import threading
import time
from test import process_input

# Set the initial appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize the main window
root = ctk.CTk()
root.title("Proof by Minecraft")
root.geometry("1000x800")
root.minsize(700, 500)

# Configure grid to make the window resizable
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# --- Virtual Keyboard Pop-up ---
def open_keyboard_popup():
    """Creates and displays a virtual keyboard pop-up window."""
    keyboard_window = ctk.CTkToplevel(root)
    keyboard_window.title("Virtual Keyboard")
    keyboard_window.geometry("300x200")
    keyboard_window.resizable(False, False)
    
    # Position the pop-up relative to the main window
    main_window_x = root.winfo_x()
    main_window_y = root.winfo_y()
    keyboard_window.geometry(f"+{main_window_x + 50}+{main_window_y + 50}")

    def insert_char(char):
        """Inserts a character into the main input text box."""
        input_text.insert("insert", char)

    key_frame = ctk.CTkFrame(keyboard_window)
    key_frame.pack(padx=10, pady=10, expand=True)
    key_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    for i, char in enumerate(keys):
        key_button = ctk.CTkButton(key_frame, text=char, width=40, height=40,
                                   command=lambda c=char: insert_char(c))
        key_button.grid(row=i // 5, column=i % 5, padx=5, pady=5)
    
    close_button = ctk.CTkButton(keyboard_window, text="Done", command=keyboard_window.destroy)
    close_button.pack(pady=10)


# --- Theme Icon and Animation Logic ---
try:
    icon_size = 40
    light_mode_icon_path = "GUI/light_mode.png"
    dark_mode_icon_path = "GUI/dark_mode.png"

    pil_light_mode_icon = Image.open(light_mode_icon_path)
    pil_dark_mode_icon = Image.open(dark_mode_icon_path)

    light_mode_icon = ctk.CTkImage(light_image=pil_light_mode_icon, size=(icon_size, icon_size))
    dark_mode_icon = ctk.CTkImage(light_image=pil_dark_mode_icon, size=(icon_size, icon_size))
except FileNotFoundError:
    print("Error: light_mode.png or dark_mode.png not found. Using placeholder.")
    light_mode_icon = None
    dark_mode_icon = None

def toggle_appearance_mode():
    """Toggles the appearance mode and the icon."""
    if ctk.get_appearance_mode() == "Dark":
        ctk.set_appearance_mode("Light")
        if dark_mode_icon:
            theme_icon.configure(image=dark_mode_icon)
    else:
        ctk.set_appearance_mode("Dark")
        if light_mode_icon:
            theme_icon.configure(image=light_mode_icon)
            
    def animate_pop():
        theme_icon.configure(width=icon_size + 4, height=icon_size + 4)
        time.sleep(0.05)
        theme_icon.configure(width=icon_size, height=icon_size)
    
    animation_thread = threading.Thread(target=animate_pop)
    animation_thread.start()

# --- GUI Layout ---

# Clickable icon for theme switching
theme_icon = ctk.CTkLabel(root, text="", cursor="hand2")
if light_mode_icon and dark_mode_icon:
    theme_icon.configure(image=light_mode_icon)
else:
    theme_icon.configure(text="Theme")
theme_icon.bind("<Button-1>", lambda event: toggle_appearance_mode())
theme_icon.place(relx=0.98, rely=0.02, anchor="ne")

# Main banner image frame at the very top
image_frame_top = ctk.CTkFrame(root, fg_color="transparent")
image_frame_top.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

try:
    image_path = "GUI/redstone_lamp.png"
    pil_main_image = Image.open(image_path)
    main_image = ctk.CTkImage(light_image=pil_main_image, size=pil_main_image.size)
    main_label = ctk.CTkLabel(image_frame_top, image=main_image, text="")
    main_label.pack(expand=True, fill="both")
except FileNotFoundError:
    print(f"Error: Image file not found at {image_path}. Displaying a placeholder.")
    ctk.CTkLabel(image_frame_top, text="Proof by Minecraft", font=("Minecraft", 32, "bold")).pack()


# Main content frames for input and output
input_frame = ctk.CTkFrame(root)
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
input_frame.grid_columnconfigure(0, weight=1)
input_frame.grid_rowconfigure(3, weight=1)

ctk.CTkLabel(input_frame, text="Input", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=5)

# Text widget for user input
input_text = ctk.CTkTextbox(input_frame, height=200)
input_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# --- Keyboard Button ---
keyboard_button = ctk.CTkButton(input_frame, text="Open Keyboard", command=open_keyboard_popup)
keyboard_button.grid(row=2, column=0, padx=10, pady=5)

# --- Submit Button ---
def submit_button_action():
    user_input = input_text.get("0.0", "end-1c")
    processed_output = process_input(user_input)
    output_text.delete("0.0", "end")
    output_text.insert("0.0", processed_output)

submit_button = ctk.CTkButton(input_frame, text="Submit", command=submit_button_action)
submit_button.grid(row=3, column=0, padx=10, pady=5)

# Mode switch tab view
tabview = ctk.CTkTabview(input_frame)
tabview.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

statements_tab = tabview.add("Logic Statements")
statements_tab.grid_columnconfigure(0, weight=1)

statements_var = ctk.StringVar(value="None")
ctk.CTkRadioButton(statements_tab, text="1 Statement Evaluation", variable=statements_var, value="1 Statement Evaluation").pack(anchor="w", padx=10, pady=5)
ctk.CTkRadioButton(statements_tab, text="2 Statement Evaluation/Comparison", variable=statements_var, value="2 Statement Evaluation/Comparison").pack(anchor="w", padx=10, pady=5)

arguments_tab = tabview.add("Logical Arguments")
arguments_tab.grid_columnconfigure(0, weight=1)

arguments_var = ctk.StringVar(value="None")
ctk.CTkRadioButton(arguments_tab, text="Placeholder 1", variable=arguments_var, value="Placeholder 1").pack(anchor="w", padx=10, pady=5)
ctk.CTkRadioButton(arguments_tab, text="Placeholder 2", variable=arguments_var, value="Placeholder 2").pack(anchor="w", padx=10, pady=5)

# Output frame (now contains a textbox)
output_frame = ctk.CTkFrame(root)
output_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
output_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_rowconfigure(1, weight=1)

ctk.CTkLabel(output_frame, text="Output", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=5)

# The output is now a text box
output_text = ctk.CTkTextbox(output_frame, height=200, width=400)
output_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
output_text.insert("0.0", "Your output will be displayed here.")


root.mainloop()

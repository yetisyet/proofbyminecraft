import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from test import process_input

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize the main window
root = ctk.CTk()
root.title("Proof by Minecraft")
root.geometry("1000x800")

# Configure grid to make the window resizable
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)  # Added a new row for the main content frames

# --- 1) Move the image to the top and make the output a text box ---

# Main banner image frame at the very top
image_frame_top = ctk.CTkFrame(root, fg_color="transparent")
image_frame_top.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

try:
    image_path = "GUI/redstone_lamp.png"
    pil_main_image = Image.open(image_path)
    # Maintain original dimensions by not specifying a size
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
input_frame.grid_rowconfigure(3, weight=1) # Adjusted for the new button

ctk.CTkLabel(input_frame, text="Input", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=5)

# Text widget for user input
input_text = ctk.CTkTextbox(input_frame, height=200)
input_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# --- Submit Button ---
def submit_button_action():
    """
    Retrieves input, calls the external function, and updates the output textbox.

    """
    user_input = input_text.get("0.0", "end-1c")#gets the user input
    processed_output = process_input(user_input)#process it note: process_input is the name of the function in test.py
    output_text.delete("0.0", "end") #displays
    output_text.insert("0.0", processed_output) #same here

submit_button = ctk.CTkButton(input_frame, text="Submit", command=submit_button_action)
submit_button.grid(row=2, column=0, padx=10, pady=5)
# Note: Changed row to 2 to place it below the input_text widget
# The tabview is now on row 3

# Mode switch tab view
tabview = ctk.CTkTabview(input_frame)
tabview.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

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
# You can add text to the box like this:
output_text.insert("0.0", "Your output will be displayed here.")


root.mainloop()
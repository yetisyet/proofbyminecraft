import customtkinter as ctk
import tkinter as tk
from PIL import Image
import threading
import time

# Note: The 'mainlogic.py' file must be in the same directory for this code to run.
# The 'process_input' function from that file is called when the submit button is pressed.
# A placeholder is provided for demonstration if the file is not available.
try:
    from mainlogic import process_input
except ImportError:
    print("CRITICAL: mainlogic.py not found..")
    def process_input(text):
        """Placeholder function for mainlogic.process_input."""
        return f"CRITICAL ERROR: '{text}'"

# Set the initial appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialize the main window
root = ctk.CTk()
root.title("Proof by Minecraft")
root.geometry("800x600") # Increased default window size for better initial layout
root.minsize(700, 500) #minimum size so it cant be intefecimally small

# Configure grid to make the window resizable
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
# Corrected: Set weight on row 1 to allow the input/output frames to expand vertically
root.grid_rowconfigure(1, weight=1) 

# --- Virtual Keyboard Pop-up ---
keyboard_window_instance = None  # Global variable to hold the single keyboard window instance

def open_keyboard_popup():
    """
    Creates and displays a virtual keyboard pop-up window.
    Ensures only one instance is open and keeps it always on top.
    """
    global keyboard_window_instance

    # a) Check if a keyboard window already exists and is not destroyed
    if keyboard_window_instance is None or not( keyboard_window_instance.winfo_exists()):
        keyboard_window = ctk.CTkToplevel(root)
        keyboard_window.title("Virtual Keyboard")
        keyboard_window.geometry("300x200")
        keyboard_window.resizable(False, False)
        
        # Position the pop-up relative to the main window
        main_window_x = root.winfo_x()
        main_window_y = root.winfo_y()
        keyboard_window.geometry(f"+{main_window_x + 50}+{main_window_y + 50}")

        # b) Set the window to be always on top
        keyboard_window.attributes('-topmost', True)
        
        # Save the new instance to the global variable
        keyboard_window_instance = keyboard_window

        def insert_char(char):
            """Inserts a character into the main input text box."""

            input_text.insert("insert", char)

        key_frame = ctk.CTkFrame(keyboard_window)
        key_frame.pack(padx=10, pady=10, expand=True)
        key_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        keys = ["a", "b", "c", "d", "e", "~", "(", ")", "v", "^"]
        for i, char in enumerate(keys):
            key_button = ctk.CTkButton(key_frame, text=char, width=40, height=40,
                                       command=lambda c=char: insert_char(c))
            key_button.grid(row=i // 5, column=i % 5, padx=5, pady=5)
        
        close_button = ctk.CTkButton(keyboard_window, text="Done", command=keyboard_window.destroy)
        close_button.pack(pady=10)
    else:
        # If the window already exists, just bring it to the front
        keyboard_window_instance.deiconify()
        keyboard_window_instance.lift()


# --- Tutorial Window Logic ---
class TutorialWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Tutorial")
        self.geometry("400x300")
        self.minsize(400, 300)
        self.grab_set()  # Make the window modal

        # Center the tutorial window over the main window
        self.update_idletasks()
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()
        
        win_x = main_x + (main_width // 2) - (self.winfo_width() // 2)
        win_y = main_y + (main_height // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{win_x}+{win_y}")

        # Add widgets for the tutorial content
        ctk.CTkLabel(
            self, 
            text="Welcome to Proof by Minecraft!", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(20, 5), padx=20)
        
        ctk.CTkLabel(
            self, 
            text="1. Enter your logical formula into the 'Formula input' box." 
            "\n\n2. Use the virtual keyboard for special symbols." 
            "\n\n3. Select a tab for the type of analysis you need." 
            "\n\n4. Click 'Submit' to see the result." 
            "\n\n The current notation is: (^ for and) (v for or) \nand (~ for the negation)", 
            wraplength=350,
            justify="left"
        ).pack(pady=10, padx=20)
        
        ctk.CTkButton(self, text="Got it!", command=self.destroy).pack(pady=(10, 20))

def open_tutorial_window():
    """Opens the tutorial window."""
    TutorialWindow(root)

# --- Theme Icon and Animation Logic ---
#lets make it look nice
try:
    icon_size = 40
    light_mode_icon_path = "GUI/light_mode.png"
    dark_mode_icon_path = "GUI/dark_mode.png" #PNG NOT VSG TIKINER DOES NOT SUPPORT SVG AAAAAAåååååå

    pil_light_mode_icon = Image.open(light_mode_icon_path)
    pil_dark_mode_icon = Image.open(dark_mode_icon_path)

    light_mode_icon = ctk.CTkImage(light_image=pil_light_mode_icon, size=(icon_size, icon_size))
    dark_mode_icon = ctk.CTkImage(light_image=pil_dark_mode_icon, size=(icon_size, icon_size))
except FileNotFoundError: #Better call saul
    print("Error: light_mode.png or dark_mode.png not found. Using placeholder.")
    light_mode_icon = None
    dark_mode_icon = None

def toggle_appearance_mode(): #dark vs light mode

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

# Main banner image frame at the very top thing
image_frame_top = ctk.CTkFrame(root, fg_color="transparent")
image_frame_top.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

try:
    image_path = "GUI/combination.png"
    pil_main_image = Image.open(image_path)
    main_image = ctk.CTkImage(light_image=pil_main_image, size=pil_main_image.size)
    main_label = ctk.CTkLabel(image_frame_top, image=main_image, text="")
    main_label.pack(expand=True, fill="both")
except FileNotFoundError: #oh no
    print(f"Error: Image file not found at {image_path}. Displaying a placeholder.")
    ctk.CTkLabel(image_frame_top, text="Proof by Minecraft", font=("Impact", 38, "bold")).pack()


# Main content frames for input and output
input_frame = ctk.CTkFrame(root)
input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
input_frame.grid_columnconfigure(0, weight=1)
# Prioritize vertical space for the text box
input_frame.grid_rowconfigure(1, weight=2) 
# Give the tabview a lower vertical weight
input_frame.grid_rowconfigure(4, weight=1)

#imgoinginsanehelp
ctk.CTkLabel(input_frame, text="Formula input", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=5)

# Text widget for user input
input_text = ctk.CTkTextbox(input_frame, height=100) # Adjusted height
input_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
input_text.insert("0.0", "Enter your logic statement here...")

# --- Keyboard Button ---
keyboard_button = ctk.CTkButton(input_frame, text="Open Keyboard", command=open_keyboard_popup)
keyboard_button.grid(row=2, column=0, padx=10, pady=5)


# --- New function to process a truth table ---
def process_truthtable(text):
    """Placeholder for the truth table processing logic."""
    return f"Processing truth table for: '{text}'"


# --- Submit Button Action: Modified to check which function to call ---
def submit_button_action():
    user_input = input_text.get("0.0", "end-1c")
    processed_output = ""
    
    # Check which radio button is selected
    if statements_var.get() == "StatementEvaluation":
        # Call the existing function for normal logic
        processed_output = process_input(user_input)
    elif arguments_var.get() == "Truthtable":
        # Call the new function for truth tables
        processed_output = process_input(user_input, True)
    else:
        processed_output = "Please select a logic type to process."

    output_text.delete("0.0", "end")
    output_text.insert("0.0", processed_output)


# --- Submit Button ---
submit_button = ctk.CTkButton(input_frame, text="Submit", command=submit_button_action)
submit_button.grid(row=3, column=0, padx=10, pady=5)

# --- Default Text Handling ---
default_text = "Enter your logic statement here..."
default_text_present = True

def on_input_click(event):
    global default_text_present
    if default_text_present:
        input_text.delete("0.0", "end")
        default_text_present = False

def on_focus_out(event):
    global default_text_present
    if not input_text.get("0.0", "end-1c"):
        input_text.insert("0.0", default_text)
        default_text_present = True

input_text.bind("<FocusIn>", on_input_click)
input_text.bind("<FocusOut>", on_focus_out)

#redbull tastes terrible
tabview = ctk.CTkTabview(input_frame)
tabview.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

statements_tab = tabview.add("Normal Logic")
statements_tab.grid_columnconfigure(0, weight=1)
statements_var = ctk.StringVar(value="None")
ctk.CTkRadioButton(statements_tab, text="Statement Evaluation", variable=statements_var, value="StatementEvaluation").pack(anchor="w", padx=10, pady=5)

arguments_tab = tabview.add("Truth Table")
arguments_tab.grid_columnconfigure(0, weight=1)
arguments_var = ctk.StringVar(value="None")
ctk.CTkRadioButton(arguments_tab, text="Truth Table", variable=arguments_var, value="Truthtable").pack(anchor="w", padx=10, pady=5)

# ITS A OUTPUT FRAME MORTY
output_frame = ctk.CTkFrame(root)
output_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
output_frame.grid_columnconfigure(0, weight=1)
output_frame.grid_rowconfigure(1, weight=1)
output_frame.grid_rowconfigure(2, weight=0) # Ensure the button row has space

ctk.CTkLabel(output_frame, text="Output", font=("Arial", 16, "bold")).grid(row=0, column=0, padx=5, pady=5)

# ITS A TEXT BOX MORTY
output_text = ctk.CTkTextbox(output_frame, height=100, width=400) # Adjusted height
output_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
output_text.insert("0.0", "Your output will be displayed here.")


# A button to open the tutorial window
tutorial_button = ctk.CTkButton(
    master=root,
    text="?",
    width=30,
    height=30,
    font=("Arial", 16),
    command=open_tutorial_window
)
tutorial_button.place(relx=0.02, rely=0.02, anchor="nw")

# --- New Function to Copy Output ---
def copy_output_to_clipboard():
    """Copies the content of the output_text widget to the clipboard."""
    text_to_copy = output_text.get("0.0", "end-1c")
    if text_to_copy:
        root.clipboard_clear()
        root.clipboard_append(text_to_copy)

# --- New Button to Copy Output ---
copy_button = ctk.CTkButton(
    master=output_frame,
    text="Copy Output",
    command=copy_output_to_clipboard
)
copy_button.grid(row=2, column=0, padx=10, pady=5)


#youtoob guy told me this was very important
root.mainloop()

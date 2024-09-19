# Import necessary libraries
import os  # To interact with the operating system
from tkinter import Tk, Label, Button, Listbox, filedialog, messagebox


# Function to choose original folder
def choose_original_folder():
    # Open a folder selection dialog
    folder_original_path = filedialog.askdirectory()

    # If a folder is selected, show its contents
    if folder_original_path:
        selected_original_folder_label.config(text=f"Selected Folder: {folder_original_path}")
        list_files(folder_original_path)
        global selected_original_folder
        selected_original_folder = folder_original_path


# Function to choose the destination folder
def choose_destination_folder():
    # Open a folder selection dialog
    folder_destination_path = filedialog.askdirectory()

    # If a folder is selected, show its contents
    if folder_destination_path:
        selected_destination_folder_label.config(text=f"Selected Folder: {folder_destination_path}")
        global selected_destination_folder
        selected_destination_folder = folder_destination_path


# Function to list all files in the selected folder
def list_files(folder_original_path):
    # Clear the listbox first
    file_listbox.delete(0, 'end')

    # List all files in the folder
    try:
        files = os.listdir(folder_original_path)  # Get list of files
        for file in files:
            file_path = os.path.join(folder_original_path, file)
            if os.path.isfile(file_path):  # Only add files, not subdirectories
                file_listbox.insert('end', file)  # Insert each file into the listbox
    except Exception as e:
        messagebox.showerror("Error", f"Could not list files: {e}")


# Function to manually copy the folders
def copy_file(original, destination):
    try:
        with open(original, 'rb') as f_original:  # Open the source file in binary read mode
            content = f_original.read()  # Read the file content

        with open(destination, 'wb') as f_destination:  # Open the destination file in binary write mode
            f_destination.write(content)  # Write the content to the destination
    except Exception as e:
        messagebox.showerror("Error", f"Could not copy file {original}: {e}")


# Function to handle copying the entire folder
def copy_folder():
    # Create a new folder called "CopiedFolder"
    new_folder = os.path.join(selected_destination_folder, "CopiedFolder")

    try:
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)  # Create the new folder if it doesn't exist

        # Copy each file in the selected folder manually
        files = os.listdir(selected_original_folder)
        for file in files:
            original_file = os.path.join(selected_original_folder, file)
            if os.path.isfile(original_file):  # Only copy files
                dest_file = os.path.join(new_folder, file)
                copy_file(original_file, dest_file)  # Use the manual copy function

        messagebox.showinfo("Success", f"Folder copied successfully to {new_folder}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not copy folder: {e}")


# Create the main window
root = Tk()
root.title("Folder Copier")
root.geometry("600x600")

# Button to choose the original folder
choose_folder_button = Button(root, text="Choose Folder", command=choose_original_folder)
choose_folder_button.pack(pady=10)

# Label for showing the original selected folder
selected_original_folder_label = Label(root, text="Select a folder", wraplength=300)
selected_original_folder_label.pack(pady=10)

# Button to choose the destination folder
choose_folder_button = Button(root, text="Choose Folder", command=choose_destination_folder)
choose_folder_button.pack(pady=10)

# Label for showing the selected destination folder
selected_destination_folder_label = Label(root, text="Select a folder", wraplength=300)
selected_destination_folder_label.pack(pady=10)

# Listbox to show files in the selected folder
file_listbox = Listbox(root, width=50, height=10)
file_listbox.pack(pady=10)

# Button to copy the folder
copy_button = Button(root, text="Copy Folder", command=copy_folder)
copy_button.pack(pady=10)

# Start the GUI main loop
root.mainloop()

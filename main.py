# Import necessary libraries
import os  # To interact with the operating system
from tkinter import Tk, Label, Button, Listbox, filedialog, messagebox


# Function to choose a folder
def choose_folder():
    # Open a folder selection dialog
    folder_path = filedialog.askdirectory()

    # If a folder is selected, show its contents
    if folder_path:
        selected_folder_label.config(text=f"Selected Folder: {folder_path}")
        list_files(folder_path)
        global selected_folder
        selected_folder = folder_path


# Function to list all files in the selected folder
def list_files(folder_path):
    # Clear the listbox first
    file_listbox.delete(0, 'end')

    # List all files in the folder
    try:
        files = os.listdir(folder_path)  # Get list of files
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):  # Only add files, not subdirectories
                file_listbox.insert('end', file)  # Insert each file into the listbox
    except Exception as e:
        messagebox.showerror("Error", f"Could not list files: {e}")


# Function to manually copy folder and its files
def copy_file(src, dst):
    """Manually copy a file from src to dst."""
    try:
        with open(src, 'rb') as f_src:  # Open the source file in binary read mode
            content = f_src.read()  # Read the file content

        with open(dst, 'wb') as f_dst:  # Open the destination file in binary write mode
            f_dst.write(content)  # Write the content to the destination
    except Exception as e:
        messagebox.showerror("Error", f"Could not copy file {src}: {e}")


# Function to handle copying the entire folder
def copy_folder():
    # Create a new folder called "CopiedFolder"
    new_folder = os.path.join(os.getcwd(), "CopiedFolder")

    try:
        if not os.path.exists(new_folder):
            os.mkdir(new_folder)  # Create the new folder if it doesn't exist

        # Copy each file in the selected folder manually
        files = os.listdir(selected_folder)
        for file in files:
            src_file = os.path.join(selected_folder, file)
            if os.path.isfile(src_file):  # Only copy files
                dest_file = os.path.join(new_folder, file)
                copy_file(src_file, dest_file)  # Use the manual copy function

        messagebox.showinfo("Success", f"Folder copied successfully to {new_folder}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not copy folder: {e}")


# Create the main window
root = Tk()
root.title("Folder Copier")
root.geometry("400x400")

# Label for showing the selected folder
selected_folder_label = Label(root, text="No folder selected", wraplength=300)
selected_folder_label.pack(pady=10)

# Button to choose a folder
choose_folder_button = Button(root, text="Choose Folder", command=choose_folder)
choose_folder_button.pack(pady=10)

# Listbox to show files in the selected folder
file_listbox = Listbox(root, width=50, height=10)
file_listbox.pack(pady=10)

# Button to copy the folder
copy_button = Button(root, text="Copy Folder", command=copy_folder)
copy_button.pack(pady=10)

# Start the GUI main loop
root.mainloop()

# Import necessary libraries
import os  # To interact with the operating system
from tkinter import Tk, Label, Button, Listbox, filedialog, messagebox, PhotoImage
from tkinter import ttk


# Function to show keynotes
def show_keynotes():
    keynotes = (
        "Keynotes:\n"
        "- The Current progress bar is bit irrelevant, "
        "as it represents the copy process and not the end of the copy, "
        "for this we can change the copy to a different thread\n"
    )
    messagebox.showinfo("Keynotes", keynotes)


# Function to show help
def show_help():
    help_text = (
        "Help:\n"
        "This application allows you to copy files from one folder to another.\n"
        "Steps to use the application:\n"
        "1. Click 'Choose Original Folder' to select the folder with files.\n"
        "2. Click 'Choose Destination Folder' to select where to copy files.\n"
        "3. Click 'Copy Folder Manually' to start the copying process.\n"
        "4. Monitor the progress using the progress bar.\n"
        "If you encounter any issues, please check folder permissions."
    )
    messagebox.showinfo("Help", help_text)


# Function to choose original folder
def choose_original_folder():
    # Open a folder selection dialog
    folder_original_path = filedialog.askdirectory()

    # If a folder is selected, show its contents
    if folder_original_path:
        selected_original_folder_label.config(text=f'Selected Folder: {folder_original_path}')
        list_files(folder_original_path, 1)
        global selected_original_folder
        selected_original_folder = folder_original_path


# Function to choose the destination folder
def choose_destination_folder():
    # Open a folder selection dialog
    folder_destination_path = filedialog.askdirectory()

    # If a folder is selected, show its contents
    if folder_destination_path:
        selected_destination_folder_label.config(text=f'Selected Folder: {folder_destination_path}')
        list_files(folder_destination_path, 2)
        global selected_destination_folder
        selected_destination_folder = folder_destination_path


# Function to list all files and directories in the selected folder
def list_files(folder_path, list_number):
    try:
        items = os.listdir(folder_path)  # Get list of files and directories

        if list_number == 1:
            file_original_listbox.delete(0, 'end')  # Clear listbox
        elif list_number == 2:
            file_destination_listbox.delete(0, 'end')  # Clear listbox

        for item in items:
            item_path = os.path.join(folder_path, item)

            # Distinguish between files and directories
            if os.path.isdir(item_path):
                display_text = f'{"[Fold]"} - {item} '  # Label directories
            else:
                display_text = f'{"[File]"} - {item} '  # Normal file display

            # Insert into the appropriate listbox
            if list_number == 1:
                file_original_listbox.insert('end', display_text)
            elif list_number == 2:
                file_destination_listbox.insert('end', display_text)
    except Exception as e:
        messagebox.showerror('Error', f'Could not list files and directories: {e}')


# Function to manually copy the folders
def copy_file(original, destination):
    try:
        with open(original, 'rb') as f_original:  # Open the source file in binary read mode
            content = f_original.read()  # Read the file content

        with open(destination, 'wb') as f_destination:  # Open the destination file in binary write mode
            f_destination.write(content)  # Write the content to the destination
            list_files(selected_destination_folder, 2)
    except Exception as e:
        messagebox.showerror('Error', f'Could not copy file {original}: {e}')


# Function to copy folders and subfolders recursively with a progress bar
def copy_folder_recursively(original_folder, destination_folder, progress_bar):
    try:
        if not os.path.exists(destination_folder):
            os.mkdir(destination_folder)
        items = os.listdir(original_folder)
        total_items = len(items)

        for index, item in enumerate(items):
            source_path = os.path.join(original_folder, item)
            dest_path = os.path.join(destination_folder, item)

            if os.path.isdir(source_path):
                copy_folder_recursively(source_path, dest_path, progress_bar)
            else:
                copy_file(source_path, dest_path)

            # Update progress bar
            progress_bar['value'] = (index + 1) / total_items * 100
            root.update_idletasks()  # Refresh the GUI

    except Exception as e:
        messagebox.showerror('Error', f'Could not copy folder: {e}')

# Function to handle copying the entire folder
def copy_folder_manually():
    global progress_bar
    new_folder = os.path.join(selected_destination_folder, 'CopiedFolder')

    # Create the ProgressBar
    progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=300)
    progress_bar.grid(row=4, column=0, columnspan=2, pady=20)

    try:
        copy_folder_recursively(selected_original_folder, new_folder, progress_bar)
        progress_bar['value'] = 100  # Complete progress
        messagebox.showinfo('Success', f'Folder copied successfully to {new_folder}')
    except Exception as e:
        messagebox.showerror('Error', f'Could not copy folder: {e}')
    finally:
        progress_bar.destroy()  # Remove progress bar after copying


# Create the main window
root = Tk()
root.title('Folder Copier')
root.geometry('600x600')

# Set the window icon
root.iconbitmap('assets/software_icon.ico')  # Replace 'your_icon.ico' with your icon file name

# Set up grid configuration for two columns
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Original folder column
choose_original_folder_button = Button(root, text='Choose Original Folder', command=choose_original_folder)
choose_original_folder_button.grid(row=0, column=0, pady=(50, 0))

# Original folder label
selected_original_folder_label = Label(root, text='Select a folder')
selected_original_folder_label.grid(row=1, column=0, pady=10)

# List Original Files/Folders
file_original_listbox = Listbox(root, width=50, height=10)
file_original_listbox.grid(row=2, column=0, padx=(20, 10), pady=(0, 10))

# Button Destination folder
choose_destination_folder_button = Button(root, text='Choose Destination Folder', command=choose_destination_folder)
choose_destination_folder_button.grid(row=0, column=1, pady=(50, 0))

# Label select destination folder list
selected_destination_folder_label = Label(root, text='Select a folder')
selected_destination_folder_label.grid(row=1, column=1, pady=10)

# List the destination folders
file_destination_listbox = Listbox(root, width=50, height=10)
file_destination_listbox.grid(row=2, column=1, padx=(10, 20), pady=(0, 10))

# Copy folder button centered below both columns
copy_button = Button(root, text='Copy Folder Manually', command=copy_folder_manually)
copy_button.grid(row=3, column=0, columnspan=2, pady=20)

# Keynotes button
keynotes_button = Button(root, text='Keynotes', command=show_keynotes)
keynotes_button.grid(row=5, column=0, pady=10)

# Help button
help_button = Button(root, text='Help', command=show_help)
help_button.grid(row=5, column=1, pady=10)

# Start the GUI main loop
root.mainloop()
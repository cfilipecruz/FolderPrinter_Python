import os  # To interact with the operating system
from tkinter import Tk, Label, Button, Text , Listbox, filedialog, messagebox, Checkbutton, IntVar
from tkinter import ttk  # Visuals
import time

# Variables
selected_original_folder = ''
selected_destination_folder = ''
log_file_path = 'assets/file_actions.log'
window_width = 1200  # Set your desired width
window_height = 800  # Set your desired height


# Function to log actions
def log_action(action, file_name, user):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {action}: {file_name} by {user}\n"
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)


# Function to read and display logs
# Function to display logs
def display_logs():
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()
            for log in logs:
                log_text.insert('end', log.strip() + '\n')  # Add a newline after each log entry
        log_text.see('end')  # Scroll to the end of the Text widget


# Assume a function to get the current user (this is a placeholder)
def get_current_user():
    return os.getlogin()  # Returns the current user's login name


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

#network
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
        with open(original, 'rb') as f_original:
            content = f_original.read()

        with open(destination, 'wb') as f_destination:
            f_destination.write(content)
            list_files(selected_destination_folder, 2)
            log_action("Copied", original, get_current_user())  # Log the copy action
    except Exception as e:
        messagebox.showerror('Error', f'Could not copy file {original}: {e}')


# Function to delete files that no longer exist in the original folder
def delete_missing_files(original_folder, destination_folder):
    try:
        original_items = set(os.listdir(original_folder))
        destination_items = set(os.listdir(destination_folder))

        for item in destination_items:
            if item not in original_items:
                item_path = os.path.join(destination_folder, item)
                if os.path.isdir(item_path):
                    for root, dirs, files in os.walk(item_path, topdown=False):
                        for name in files:
                            os.remove(os.path.join(root, name))
                            log_action("Deleted", os.path.join(root, name), get_current_user())  # Log the deletion
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                    os.rmdir(item_path)
                    log_action("Deleted", item_path, get_current_user())  # Log the deletion
                else:
                    os.remove(item_path)
                    log_action("Deleted", item_path, get_current_user())  # Log the deletion
        list_files(destination_folder, 2)
    except Exception as e:
        messagebox.showerror('Error', f'Could not delete missing files: {e}')


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
            root.update_idletasks()

        # After copying, check and delete missing files
        delete_missing_files(original_folder, destination_folder)

    except Exception as e:
        messagebox.showerror('Error', f'Could not copy folder: {e}')


# Function to handle copying the entire folder
def copy_folder_manually(auto):
    if selected_original_folder == '':
        messagebox.showerror('Error', 'Please select an original folder')
    elif selected_destination_folder == '':
        messagebox.showerror('Error', 'Please select a destination folder')
    else:
        new_folder = os.path.join(selected_destination_folder, 'CopiedFolder')
        progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=300)
        progress_bar.grid(row=6, column=0, columnspan=2, pady=20)

        try:
            copy_folder_recursively(selected_original_folder, new_folder, progress_bar)
            progress_bar['value'] = 100  # Complete progress
            if not auto:
                messagebox.showinfo('Success', f'Folder copied successfully to {new_folder}')
        except Exception as e:
            messagebox.showerror('Error', f'Could not copy folder: {e}')
        finally:
            progress_bar.destroy()  # Remove progress bar after copying


# Timer function to update file lists
def update_file_lists():
    if timer_var.get():  # Check if the timer is activated
        copy_folder_manually(True)  # Start copying if the timer is enabled
        if selected_original_folder:
            list_files(selected_original_folder, 1)
        if selected_destination_folder:
            list_files(selected_destination_folder, 2)
        root.after(30000, update_file_lists)  # Schedule the next update in 60 seconds


# Function to start the timer
def toggle_timer():
    if timer_var.get():
        update_file_lists()  # Start updating if the timer is enabled


# Create the main window
root = Tk()
root.title('Folder Copier')

# Get user screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position for centering
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

# Set the window geometry (size and position)
root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

# Set the window icon
root.iconbitmap('assets/software_icon.ico')  # Replace 'your_icon.ico' with your icon file name

# Configure grid
# Dont mess with this, not worth it
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)  # Listboxes
root.grid_rowconfigure(7, weight=1)  # Log Text Box

# Original folder column button
choose_original_folder_button = Button(root, text='Choose Original Folder', command=choose_original_folder)
choose_original_folder_button.grid(row=0, column=0, pady=(20, 0), padx=(20, 20))

# Original folder label
selected_original_folder_label = Label(root, text='Select a folder')
selected_original_folder_label.grid(row=1, column=0, pady=(10, 20), padx=(20, 20))

# List Original Files/Folders
file_original_listbox = Listbox(root, width=50, height=10)
file_original_listbox.grid(row=2, column=0, padx=(20, 10), pady=(10, 20))

# Button Destination folder
choose_destination_folder_button = Button(root, text='Choose Destination Folder', command=choose_destination_folder)
choose_destination_folder_button.grid(row=0, column=1, pady=(20, 0), padx=(20, 20))

# Label select destination folder list
selected_destination_folder_label = Label(root, text='Select a folder')
selected_destination_folder_label.grid(row=1, column=1, pady=(10, 20), padx=(20, 20))

# List the destination folders
file_destination_listbox = Listbox(root, width=50, height=10)
file_destination_listbox.grid(row=2, column=1, padx=(10, 20), pady=(10, 20))

# Copy folder button centered below both columns
copy_button = Button(root, text='Copy Folder Manually', command=lambda: copy_folder_manually(False))
copy_button.grid(row=3, column=0, columnspan=2, pady=20)

# Switch for the timer
timer_var = IntVar()
timer_switch = Checkbutton(root, text='Enable Auto Update (30 seconds)', variable=timer_var, command=toggle_timer)
timer_switch.grid(row=4, column=0, columnspan=2, pady=(10, 20), sticky='ew')

# Keynotes button
keynotes_button = Button(root, text='Keynotes', command=show_keynotes)
keynotes_button.grid(row=3, column=0, pady=(10, 20))

# Help button
help_button = Button(root, text='Help', command=show_help)
help_button.grid(row=3, column=1, pady=(10, 20))

# Text widget for displaying logs
log_text = Text(root, wrap='word')
log_text.grid(row=7, column=0, columnspan=2, padx=20, pady=(10, 20), sticky='nsew')
display_logs()

# Configure the grid row for the log text
root.grid_rowconfigure(7, weight=1)

# Start the GUI main loop
root.mainloop()


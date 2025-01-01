import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import sys

# Define the paths to QEMU and QEMU Image utility
QEMU_SYSTEM_PATH = r"C:\\Program Files\\qemu\\qemu-system-x86_64.exe"
QEMU_IMG_PATH = r"C:\\Program Files\\qemu\\qemu-img.exe"

def create_vm_interactive():
    # Create a new Toplevel window to enter VM details
    vm_window = tk.Toplevel()
    vm_window.title("Enter VM Details")
    vm_window.geometry("400x300")
    vm_window.configure(bg="#f5f5f5")

    def submit_vm_details():
        name = name_entry.get()
        memory = memory_entry.get()
        disk_size = disk_size_entry.get()

        # Validate the entries
        if not name or not memory or not disk_size:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        # Path to the Ubuntu ISO
        iso_path = "C:\\Users\\peedo.abourayya\\Downloads\\ubuntu-20.04.6-desktop-amd64.iso"
        
        # Ensure the ISO path exists
        if not os.path.exists(iso_path):
            messagebox.showerror("Error", "ISO file not found.")
            return

        # Create a virtual disk
        subprocess.run([QEMU_IMG_PATH, "create", "-f", "qcow2", f"{name}.qcow2", disk_size])

        # Run the VM with the attached ISO and disk
        subprocess.run([QEMU_SYSTEM_PATH,
                        "-m", memory,
                        "-hda", f"{name}.qcow2",  # Attach the virtual disk
                        "-cdrom", iso_path,  # Attach the Ubuntu ISO to the virtual CD-ROM
                        "-boot", "d"  # Boot from CD-ROM (ISO) first
                       ])
        # Close the VM window after the operation
        vm_window.destroy()

    # Create labels and entry fields
    name_label = tk.Label(vm_window, text="VM Name:", bg="#f5f5f5", font=("Helvetica", 12))
    name_label.pack(pady=(10, 5))
    name_entry = tk.Entry(vm_window, font=("Helvetica", 12))
    name_entry.pack(pady=(5, 15))

    memory_label = tk.Label(vm_window, text="Memory (MB):", bg="#f5f5f5", font=("Helvetica", 12))
    memory_label.pack(pady=(10, 5))
    memory_entry = tk.Entry(vm_window, font=("Helvetica", 12))
    memory_entry.pack(pady=(5, 15))

    disk_size_label = tk.Label(vm_window, text="Disk Size (MB):", bg="#f5f5f5", font=("Helvetica", 12))
    disk_size_label.pack(pady=(10, 5))
    disk_size_entry = tk.Entry(vm_window, font=("Helvetica", 12))
    disk_size_entry.pack(pady=(5, 15))

    # Create submit button
    submit_button = tk.Button(vm_window, text="Submit", command=submit_vm_details, 
                              bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                              relief="flat", bd=2, activebackground="#45a049", activeforeground="white")
    submit_button.pack(pady=(10, 20))

    vm_window.mainloop()

def main_2():
    root = tk.Tk()

    # Window Title
    root.title("VM Creation")

    # Set window size and background color
    root.geometry("600x500")
    root.configure(bg='#f0f0f0')

    # Create buttons with new styles
    pady_value = 15  # Vertical padding between buttons

    # Create VM button
    create_vm_button = tk.Button(root, text="Create VM Interactively", command=create_vm_interactive, 
                                 bg="#4CAF50", fg="white", height=2, width=30, font=("Helvetica", 12, "bold"),
                                 relief="flat", bd=2, activebackground="#45a049", activeforeground="white")
    create_vm_button.pack(pady=(pady_value, pady_value))

    root.mainloop()

if __name__ == "__main__":
    main_2()

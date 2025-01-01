import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import docker
from docker.errors import APIError, NotFound
import re


def create_dockerfile():
    file_path = filedialog.askdirectory(title="Select Directory to Save Dockerfile")
    
    # Ask user to choose Python or Java for Dockerfile
    choice = simpledialog.askinteger("Choose", "Choose:\n1. Python\n2. Java\nEnter your choice (1 or 2):")
    if choice not in [1, 2]:
        messagebox.showerror("Error", "Invalid choice! Please enter either '1' for Python or '2' for Java.")
        return

    if choice == 1:
        content = "FROM python:3.9\nWORKDIR /app\nCOPY . /app\nRUN pip install --no-cache-dir -r requirements.txt\nEXPOSE 80\nENV NAME World\nCMD python app.py"
    elif choice == 2:
        content = "FROM openjdk:11\nWORKDIR /app\nCOPY . /app\n# Add necessary Java configurations\nCMD java app"

    complete_path = f"{file_path}/Dockerfile"
    try:
        with open(complete_path, 'w') as file:
            file.write(content)
        messagebox.showinfo("Dockerfile Created", "Dockerfile created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating Dockerfile: {e}")

def validate_image_name(image_name):
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_.-]{0,127}$', image_name):
        raise ValueError("Invalid image name. It must start with a letter and can only contain lowercase letters, digits, underscores, periods, and dashes.")

def validate_tag(tag):
    if not re.match(r'^[a-zA-Z0-9_.-]{0,127}$', tag):
        raise ValueError("Invalid tag. It can only contain lowercase letters, digits, underscores, periods, and dashes.")

def build_docker_image():
    dockerfile_path = filedialog.askdirectory(title="Select Directory Containing Dockerfile")
    image_name = simpledialog.askstring("Image Name", "Enter the image name:")
    tag = simpledialog.askstring("Tag", "Enter the tag:")
    
    try:
        validate_image_name(image_name)
        validate_tag(tag)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    image_name_tag = f"{image_name}:{tag}"
    client = docker.from_env()

    try:
        image, build_logs = client.images.build(path=dockerfile_path, tag=image_name_tag, rm=True)
        messagebox.showinfo("Build Image", "Docker image built successfully!")
        print("Docker image built successfully!")
        print("Image ID:", image.id)
    except docker.errors.BuildError as e:
        messagebox.showerror("Error", f"Failed to build Docker image.\nBuild logs: {e}")

def create_container():
    image_name = simpledialog.askstring("Image Name", "Enter the image name:")
    container_name = simpledialog.askstring("Container Name", "Enter the container name:")
    client = docker.from_env()

    try:
        container = client.containers.run(
            image=image_name,
            name=container_name,
            detach=True,
            log_config={'type': 'json-file'}
        )
        messagebox.showinfo("Create Container", f"Container {container.id} created from image {image_name}")
    except docker.errors.APIError as e:
        messagebox.showerror("Error", f"Error creating container: {e}")

def list_docker_images():
    client = docker.from_env()

    try:
        images = client.images.list()
        image_list = "\n".join([str(image.tags) for image in images])
        messagebox.showinfo("Docker Images", f"Docker images:\n{image_list}")
    except APIError as e:
        messagebox.showerror("Error", f"Error listing Docker images: {e}")

def stop_specific_container(container_id):
    def stop():
        try:
            client = docker.from_env()
            container = client.containers.get(container_id)
            container.stop()
            messagebox.showinfo("Stop Container", f"Container '{container_id}' stopped successfully!")
        except NotFound as e:
            messagebox.showerror("Container Not Found", f"Container not found: {e}")
        except APIError as e:
            messagebox.showerror("Error", f"Error stopping container: {e}")

    return stop

def list_running_containers():
    client = docker.from_env()

    try:
        containers = client.containers.list()
        root = tk.Tk()
        root.title("Running Containers")

        for container in containers:
            container_frame = tk.Frame(root)
            container_info = f"Container ID: {container.id}, Name: {container.name}"
            container_label = tk.Label(container_frame, text=container_info)
            container_label.pack(side=tk.LEFT)

            stop_button = tk.Button(container_frame, text="Stop", command=stop_specific_container(container.id), bg="#FF4136", fg="white", font='Helvetica 12 bold', relief="flat", padx=15, pady=10)
            stop_button.pack(side=tk.RIGHT)

            container_frame.pack(pady=5)

        root.mainloop()
    except APIError as e:
        messagebox.showerror("Error", f"Error listing running containers: {e}")

def stop_container():
    container_id = simpledialog.askstring("Container ID", "Enter the ID of the container to stop:")
    client = docker.from_env()

    try:
        container = client.containers.get(container_id)
        container.stop()
        messagebox.showinfo("Stop Container", f"Container '{container_id}' stopped successfully!")
    except NotFound as e:
        messagebox.showerror("Container Not Found", f"Container not found: {e}")
    except APIError as e:
        messagebox.showerror("Error", f"Error stopping container: {e}")

def main():
    root = tk.Toplevel()
    root.title("Docker Management")

    root.geometry("600x750")
    root.configure(bg="#2f2f2f")  # Dark background color for the main window

    pady_value = 15

    create_dockerfile_button = tk.Button(root, text="Create Dockerfile", command=create_dockerfile, bg="#4CAF50", height=3, width=30, fg="white", font='Helvetica 14 bold', relief="flat", padx=10, pady=10)
    create_dockerfile_button.pack(pady=(pady_value, pady_value))

    build_image_button = tk.Button(root, text="Build Docker Image", command=build_docker_image, bg="#2196F3", height=3, width=30, fg="white", font='Helvetica 14 bold', relief="flat", padx=10, pady=10)
    build_image_button.pack(pady=(pady_value, pady_value))

    create_container_button = tk.Button(root, text="Create Container", command=create_container, bg="#FF9800", height=3, width=30, fg="white", font='Helvetica 14 bold', relief="flat", padx=10, pady=10)
    create_container_button.pack(pady=(pady_value, pady_value))

    list_images_button = tk.Button(root, text="List Docker Images", command=list_docker_images, bg="#9C27B0", height=3, width=30, fg="white", font='Helvetica 14 bold', relief="flat", padx=10, pady=10)
    list_images_button.pack(pady=(pady_value, pady_value))

    list_containers_button = tk.Button(root, text="List Running Containers", command=list_running_containers, bg="#3F51B5", height=3, width=30, fg="white", font='Helvetica 14 bold', relief="flat", padx=10, pady=10)
    list_containers_button.pack(pady=(pady_value, pady_value))

    stop_container_button = tk.Button(root, text="Stop Container", command=stop_specific_container, bg="#F44336", height=3, width=30, fg="white", font='Helvetica 14 bold', relief="flat", padx=10, pady=10)
    stop_container_button.pack(pady=(pady_value, pady_value))

    root.mainloop()

if __name__ == "__main__":
    main()

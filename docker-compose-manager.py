import os
import subprocess
import yaml

# Check if docker-compose.yml exists in the current directory
if not os.path.isfile("docker-compose.yml"):
    print("Error: docker-compose.yml file not found in the current directory.")
    exit(1)

# Load the docker-compose.yml file
with open("docker-compose.yml", "r") as f:
    compose_data = yaml.safe_load(f)

# Get the list of services with container_name defined
services = [service for service, config in compose_data.get("services", {}).items() if "container_name" in config]

if not services:
    print("No services found with a container_name defined.")
    exit(1)

# Get the list of running containers and their names
running_containers = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}"]).decode().strip().split("\n")

# Check if any of the containers are running
containers_running = any(service in running_containers for service in services)

if containers_running:
    print("Some containers are already running.")
    stop_containers = input("Do you want to stop and remove all existing containers? (y/n/0 to exit): ").lower()

    if stop_containers == "y":
        subprocess.run(["docker", "compose", "down", "--volumes", "--remove-orphans"])
    elif stop_containers == "n":
        print("Currently running containers:")
        for i, container in enumerate(running_containers, start=1):
            print(f"{i}. {container}")
        print("0. Exit and run 'docker compose down'")

        selection = input("Do you want to connect to a running container or exit? (enter number): ")
        if selection == "0":
            subprocess.run(["docker", "compose", "down", "--volumes", "--remove-orphans"])
            exit(0)
        elif selection.isdigit() and 1 <= int(selection) <= len(running_containers):
            container_name = running_containers[int(selection) - 1]
            container_id = subprocess.check_output(["docker", "ps", "-qf", f"name={container_name}"]).decode().strip()
            subprocess.run(["docker", "exec", "-it", container_id, "sh"])
        else:
            print("Invalid selection. Exiting without starting or connecting to containers.")
            exit(0)
    elif stop_containers == "0":
        subprocess.run(["docker", "compose", "down", "--volumes", "--remove-orphans"])
        exit(0)
    else:
        print("Invalid selection. Exiting without starting or connecting to containers.")
        exit(0)

# Try to run docker compose up
try:
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
except subprocess.CalledProcessError as e:
    print("An error occurred while running 'docker compose up':")
    print(e.output.decode())
    exit(1)

# Print the list of available services
print("Available services:")
for i, service in enumerate(services, start=1):
    print(f"{i}. {service}")
print("0. Exit and run 'docker compose down'")

# Prompt the user to select a service
while True:
    selection = input("Select a service (enter the number) or 0 to exit: ")
    if selection == "0":
        subprocess.run(["docker", "compose", "down", "--volumes", "--remove-orphans"])
        exit(0)
    elif selection.isdigit() and 1 <= int(selection) <= len(services):
        break
    else:
        print("Invalid selection. Please try again.")

# Get the container name of the selected service
selected_service = services[int(selection) - 1]
container_name = compose_data["services"][selected_service]["container_name"]

# Get the container ID of the selected service
container_id = subprocess.check_output(["docker", "ps", "-qf", f"name={container_name}"]).decode().strip()

if not container_id:
    print(f"No running container found for service '{selected_service}'.")
    exit(1)

# Execute shell into the selected service container
subprocess.run(["docker", "exec", "-it", container_id, "sh"])

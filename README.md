# Docker Container Management Script

This Python 3.X script is designed to simplify the management of Docker containers, providing a user-friendly interface to inspect, start, stop, and connect to containers defined in a `docker-compose.yml` file.

## Why Does This Script Exist?

Managing Docker containers can be a tedious and error-prone process, especially when dealing with multiple containers and services. This script aims to streamline the process by providing an interactive command-line interface, making it easier to inspect and interact with your Docker containers.

## Features

- Check for running containers and offer options to stop/remove or connect to them
- Start new containers using `docker compose up`
- List available services defined in the `docker-compose.yml` file
- Connect to a running container with a single command

## Usage

1. Ensure you have Python 3 installed on your system.
2. Copy the script to the directory containing your `docker-compose.yml` file.
3. Open a terminal and navigate to the directory containing the script.
4. Run the script with the following command:

`bash
python3 docker_container_management.py
`

5. Follow the prompts in the terminal to manage your Docker containers.

### Available Options

When the script starts, it checks for running containers. If any containers are running, you will be prompted with the following options:

- **Stop and remove all existing containers**: Enter `y` to stop and remove all running containers.
- **Connect to a running container**: Enter `n` to list the currently running containers. Then, enter the corresponding number to connect to a specific container.
- **Exit without starting or connecting**: Enter `0` to exit the script without taking any action.

If no containers are running or after stopping and removing existing containers, the script will start new containers using `docker compose up`. After that, you will be presented with a list of available services defined in the `docker-compose.yml` file.

- **Connect to a service container**: Enter the corresponding number to connect to the container for that service.
- **Exit and run 'docker compose down'**: Enter `0` to exit the script and run `docker compose down` to stop and remove all containers.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).

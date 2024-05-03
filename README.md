# Docker Container Starter

This repository contains a Bash script and a Python script designed to automate the starting of Docker containers with a specified delay after system boot. This is particularly useful for ensuring that all required services and network configurations are in place before starting the containers.

## Prerequisites

Before you run the installation script, make sure you have the following installed on your system:
- `systemd`
- `Docker`
- `Docker Compose`
- `Python 3`

These components are necessary for the script to function correctly.

## Installation

To set up the Docker Container Starter, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Pand3ru/docker-container-starter.git
   cd docker-container-starter
   ```
2. **Run the Install Script**
   ```bash
   ./install.sh
   ```
   During the installation, you will be prompted to enter:
   - Your Pushover API token
   - Your Pushover user token
   - The delay time in seconds (default is 90)
   These inputs are used to configure the system to send notifications via Pushover and to set the delay timer for starting the Docker containers.
3. **Configuration**
   - The script will automatically create a `.env` file containing your Pushover API tokens.
   - It will also set up systemd unit files to manage the services.

## Usage
Once installed, the system will automatically start the specified Docker containers after the delay you set during installation every time the system boots. This is handled by the systemd timer created and enabled by the installation script.

If you need to adjust the delay time or modify which containers are started, you will need to edit the systemd timer and service files located at `/etc/systemd/system/`.

## Contributing

Contributions to this project are welcome! I myself have some more ideas for this project but I don't know if I will pursue them.

## License
This project is licensed under the MIT License - see the LICENSE file for details.



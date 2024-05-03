#!/bin/bash

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

for needed in systemctl docker docker-compose python3; do
    if ! command_exists $needed; then
        echo "Error: $needed is required but not installed. Please install $needed before running this script."
        exit 1
    fi
done

read -p "Enter your Pushover API token: " pushover_api_token
read -p "Enter your Pushover user token: " pushover_user_token

read -p "Enter the delay time in seconds (default is 90): " delay_time
delay_time=${delay_time:-90}

echo "Creating .env file..."
cat << EOF > .env
PUSHOVER_API_TOKEN=$pushover_api_token
PUSHOVER_USER_TOKEN=$pushover_user_token
EOF

echo "Creating systemd timer and service unit files..."
cat << EOF > delayed-start.timer
[Unit]
Description=Delayed Start Timer

[Timer]
OnBootSec=${delay_time}s
Unit=delayed-start.service

[Install]
WantedBy=timers.target
EOF

cat << EOF > delayed-start.service
[Unit]
Description=Delayed Start Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/main.py

[Install]
WantedBy=multi-user.target
EOF

sudo mv delayed-start.timer delayed-start.service /etc/systemd/system/
sudo systemctl enable delayed-start.timer delayed-start.service
sudo systemctl start delayed-start.timer

echo "Installation completed successfully. The services will start automatically."


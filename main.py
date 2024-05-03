import os
import http.client, urllib
import subprocess as s
import docker
import json

from dotenv import load_dotenv

load_dotenv()

client = docker.from_env()

def load_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        return config.get("CONTAINER_PATHS", {})

CONTAINER_PATHS = load_config()

def check_containers():
    for container_name, _ in CONTAINER_PATHS.items():
        container_running = any(container_name in container.name for container in client.containers.list())

        if not container_running:
            try:
                s.run(["docker-compose", "-f", os.path.join(os.getenv("HOME"), CONTAINER_PATHS[container_name], "docker-compose.yml"), "up", "-d"], check=True)
                send_push(f"Starting {container_name}")
            except subprocess.CalledProcessError as e:
                print(f"Error starting {container_name}: {e}")
                send_push(f"{container_name} failed to start")

def send_push(message: str):
    pushover_api_token = os.getenv("PUSHOVER_API_TOKEN")
    pushover_user_token = os.getenv("PUSHOVER_USER_TOKEN")

    conn = http.client.HTTPSConnection("api.pushover.net:443")
    payload = urllib.parse.urlencode({
        "token": pushover_api_token,
        "user": pushover_user_token,
        "message": message,
    })
    headers = { "Content-Type": "application/x-www-form-urlencoded" }

    try:
        conn.request("POST", "/1/messages.json", payload, headers)
        response = conn.getresponse()
        print("Response Status:", response.status)
        print("Response Reason:", response.reason)
    except Exception as e:
        print("Error:", e)
    
if __name__ == "__main__":
    check_containers()

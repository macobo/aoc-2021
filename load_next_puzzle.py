from sys import argv
from time import sleep
from datetime import datetime, timedelta, timezone
import requests
import webbrowser

year = int(argv[1])
day = int(argv[2])
base_url = f"https://adventofcode.com/{year}/day/{day}"
input_url = f"{base_url}/input"
session_token = open("session.txt").read().strip()

SLEEP_CUTOFF_SECONDS = 5

def log(message):
    print(f"{datetime.now().strftime('%H:%M:%S')} -- {message}")

def check_puzzle_available() -> bool:
    response = requests.get(base_url)
    return response.status_code == 200

def load_input_data():
    response = requests.get(input_url, cookies={"session": session_token})
    assert response.status_code == 200, f"Session likely isn't valid - check session.txt. {response.__dict__}"

    with open(f"day{day}.input", "w") as f:
        f.write(response.text)

def time_until_puzzle_available() -> timedelta:
    target_time = datetime(year, 12, day, hour=5, tzinfo=timezone.utc)
    now = datetime.now(tz=timezone.utc)

    return max(target_time - now, timedelta(seconds=0))

def get_sleep_time(time_to_go):
    if time_to_go.total_seconds() > 3600:
        return 120
    if time_to_go.total_seconds() > 600:
        return 30
    return min(5, time_to_go.total_seconds() - SLEEP_CUTOFF_SECONDS)

while (time_to_go := time_until_puzzle_available()).total_seconds() > SLEEP_CUTOFF_SECONDS:
    sleep_time = get_sleep_time(time_to_go)
    log(f"sleeping {sleep_time}s, {str(time_to_go).split('.')[0]} to go")
    sleep(sleep_time)

log("Checking if site is available...")
while not check_puzzle_available():
    log(f"Task not yet available, checking again in 5s")
    sleep(5)

log("Task is available, loading input data & opening the page")
load_input_data()
webbrowser.open(base_url)

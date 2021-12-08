from sys import argv
from time import sleep, strftime, gmtime
from datetime import datetime, timedelta, timezone
from typing import Optional
import bs4
import requests
import webbrowser
import tqdm

year = int(argv[1])
day = int(argv[2])
base_url = f"https://adventofcode.com/{year}/day/{day}"
input_url = f"{base_url}/input"
session_token = open("session.txt").read().strip()

SLEEP_CUTOFF_SECONDS = 5

def log(message):
    print(f"{datetime.now().strftime('%H:%M:%S')} -- {message}")

def attempt_load_puzzle() -> Optional[str]:
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        return soup.select_one("code").get_text().strip()
    return None

def load_input_data():
    response = requests.get(input_url, cookies={"session": session_token})
    assert response.status_code == 200, f"Session likely isn't valid - check session.txt. {response.__dict__}"

    with open(f"day{day}.input", "w") as f:
        f.write(response.text)

def time_until_puzzle_available() -> float:
    target_time = datetime(year, 12, day, hour=5, tzinfo=timezone.utc)
    now = datetime.now(tz=timezone.utc)

    return max(target_time - now, timedelta(seconds=0)).total_seconds()

def format_timedelta(seconds):
    return strftime('%H:%M:%S', gmtime(seconds))

seconds_to_go = time_until_puzzle_available()
if seconds_to_go > 0:
    with tqdm.tqdm(total=seconds_to_go, bar_format="{desc}|{bar}|{percentage:3.0f}%") as t:
        while (seconds_to_go := time_until_puzzle_available()) > SLEEP_CUTOFF_SECONDS:
            t.set_description(f"{format_timedelta(seconds_to_go)} to go")
            t.update()
            sleep(1)

log("Waiting until site is available...")

while not (sample_input := attempt_load_puzzle()):
    log(f"Task not yet available, checking again in 5s")
    sleep(5)

with open(f"day{day}.sample.input", "w") as f:
    f.write(sample_input)

log("Task is available, loading input data & opening the page")
load_input_data()
webbrowser.open(base_url)

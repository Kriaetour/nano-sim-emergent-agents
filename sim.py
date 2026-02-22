import ollama
import json
import time
from config import *

world = {"history": [], "moods": {}}
agents = [f"Agent{i}" for i in range(AGENTS)]

def tick():
    agent = agents[0]  # Stub: 1 agent first
    obs = f"Room: {ROOM_ITEMS}. History: {world['history'][-2:]}"
    resp = ollama.chat(model=MODEL, messages=[{'role':'user', 'content': f"You are {agent}. {obs}. Respond JSON: {{'say': 'hi', 'mood': 'happy'}}"}])
    action = json.loads(resp['message']['content'])
    world['history'].append(f"{agent}: {action}")
    print(action)
    time.sleep(1)  # Vibe pace

if __name__ == "__main__":
    while True:
        tick()
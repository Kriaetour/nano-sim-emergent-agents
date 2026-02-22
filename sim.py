import ollama
import json
import time
import re
from config import *

world = {"history": [], "moods": {}}
agents = [f"Agent{i}" for i in range(AGENTS)]

def tick():
    agent = agents[0]
    obs = f"Room: {ROOM_ITEMS}. History: {world['history'][-2:]}"
    prompt = f"""You are {agent} in a pub sim.
OBS: {obs}

Respond with **ONLY** valid JSON object, no other text:
{{
  "say": "your message",
  "mood": "happy|grumpy|excited"
}}

Example ONLY JSON: {{"say": "Cheers!", "mood": "happy"}}"""
    
    resp = ollama.chat(model=MODEL, messages=[{'role':'user', 'content': prompt}])
    raw = resp['message']['content']
    
    # Extract JSON (handles extra text)
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        action = json.loads(json_match.group())
    else:
        action = {"say": "?", "mood": "confused"}  # Fallback
    
    world['history'].append(f"{agent}: {action['say']} ({action['mood']})")
    print(f"[{agent}] {action['say']} | Mood: {action['mood']}")
    print(f"History: {world['history'][-1]}")


if __name__ == "__main__":
    while True:
        tick()
from data.engine import *
import json
import os
import sys

def path_getter(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

game_path = path_getter(os.path.join('game.json'))
with open(game_path, 'r', encoding="utf-8") as f:
    data = json.load(f)
    main(data)

for sprite in data['sprites'].values():
    exec(sprite['code'])
running()


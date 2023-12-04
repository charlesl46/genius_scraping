from genius import get_lyrics
import pandas as pd
import json
from rich.progress import track

df = pd.read_csv("best_songs.csv",encoding='latin-1')
titles = df["title"].values

dico = {}
for title in track(titles):
    dico[title] = get_lyrics(title)

with open("lyrics.json","w") as file:
    json.dump(dico,file)

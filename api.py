import requests
from fastapi import FastAPI, Query
from typing import Optional
def get_brawler_info(name: str):
    url = "https://api.brawlapi.com/v1/brawlers"
    response = requests.get(url)
    data = response.json()
    for brawler in data['list']:
        if brawler['name'].lower() == name.lower():
            return {
                "name": brawler['name'],
                "class": brawler['class']['name'],
                "rarity": brawler['rarity']['name'],
                "image": brawler['imageUrl'],
                "description": brawler['description'],
                "starPowers": [
                    {"name": sp["name"], "description": sp["description"]}
                    for sp in brawler['starPowers']
                ],
                "gadgets": [
                    {"name": gd["name"], "description": gd["description"]}
                    for gd in brawler['gadgets']
                ]
            }
    return {"error": "Brawler not found"}


def get_map_info(name: str):
    url = "https://api.brawlapi.com/v1/maps"
    response = requests.get(url)
    data = response.json()
    for map in data['list']:
        if map['name'].lower() == name.lower():
            return {
                "name": map["name"],
                "image": map["imageUrl"],
                "gamemode": map["gameMode"]["name"],
                "gamemodeImage": map["gameMode"]["imageUrl"],
                "Id": map["id"]
            }
    return {"error": "Map not found"}


app = FastAPI()
@app.get("/brawler")
def fetch_brawler(name: str = Query(..., description="Enter brawler name")):
    data = get_brawler_info(name)
    return data

@app.get("/map")
def fetch_map(name: str = Query(..., description="Enter map name")):
    data = get_map_info(name)
    return data
import requests
import json
import time
import os

BASE_URL = "https://pokeapi.co/api/v2/pokemon"

def fetch_pokemon_details(limit=10, offset=0):
    """
    Забирает список покемонов и затем детальную информацию по каждому.
    limit: сколько покемонов забрать
    offset: с какого по счету начать (для пагинации)
    """
    url = f"{BASE_URL}?limit={limit}&offset={offset}"
    print(f"Запрашиваем список покемонов: {url}")
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    results = data.get("results", [])
    pokemon_data = []
    
    for item in results:
        pokemon_name = item["name"]
        pokemon_url = item["url"]
        
        print(f"Загружаем данные для: {pokemon_name}...")
        detail_response = requests.get(pokemon_url)
        
        if detail_response.status_code == 200:
            pokemon_data.append(detail_response.json())
        
        time.sleep(0.5) 
        
    return pokemon_data

def save_to_json(data, filepath):
    """Сохраняет список словарей в JSON файл"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Данные успешно сохранены в {filepath}")

if __name__ == "__main__":
    print("🚀 Старт ETL-процесса (Extract)...")
    
    pokemons = fetch_pokemon_details(limit=20, offset=0)
    
    save_to_json(pokemons, "data/raw/pokemons_raw.json")
    
    print(f"✅ Готово! Собрано {len(pokemons)} записей.")

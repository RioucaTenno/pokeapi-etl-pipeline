import json
import pandas as pd
import os
from sqlalchemy import create_engine

if os.path.exists("/opt/airflow"):
    DB_URL = "postgresql+psycopg2://admin:admin@postgres:5432/pokemon_db"
    FILE_PATH = "/opt/airflow/data/raw/pokemons_raw.json"
else:
    DB_URL = "postgresql+psycopg://admin:admin@localhost:5433/pokemon_db"
    FILE_PATH = "data/raw/pokemons_raw.json"

def transform_and_load():
    print("🚀 Старт процесса Transform & Load...")
    engine = create_engine(DB_URL)
    
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Ошибка: Файл {FILE_PATH} не найден.")
        return

    pokemons_list = []
    types_list = []

    for p in raw_data:
        pokemons_list.append({
            "id": p["id"],
            "name": p["name"],
            "height": p["height"],
            "weight": p["weight"],
            "base_experience": p["base_experience"]
        })

        for t in p["types"]:
            types_list.append({
                "pokemon_id": p["id"],
                "slot": t["slot"],
                "type_name": t["type"]["name"]
            })

    df_pokemons = pd.DataFrame(pokemons_list)
    df_types = pd.DataFrame(types_list)

    print(f"📦 Подготовлено {len(df_pokemons)} строк для таблицы pokemons")
    print(f"📦 Подготовлено {len(df_types)} строк для таблицы pokemon_types")

    print("⏳ Загружаем данные в PostgreSQL...")
    
    df_pokemons.to_sql("pokemons", engine, if_exists="replace", index=False)
    df_types.to_sql("pokemon_types", engine, if_exists="replace", index=False)

    print("✅ Данные успешно загружены в базу!")

if __name__ == "__main__":
    transform_and_load()
# Pokémon ETL Pipeline (Airflow + Docker + PostgreSQL)

## 📌 О проекте
Это учебный ETL-пайплайн, который автоматически собирает данные о покемонах из публичного PokeAPI, трансформирует их и загружает в базу данных PostgreSQL. Оркестрация процессов реализована через Apache Airflow.

## 🛠️ Стек технологий
* **Язык:** Python 3
* **Оркестрация:** Apache Airflow 2.8
* **База данных:** PostgreSQL 15
* **Инфраструктура:** Docker, Docker Compose
* **Библиотеки:** Pandas, SQLAlchemy, Requests, psycopg2

## 🏗️ Архитектура пайплайна
1. **Extract:** Скрипт `extract.py` обращается к PokeAPI, забирает данные о 20 покемонах (с пагинацией) и сохраняет их в сыром виде в `data/raw/pokemons_raw.json`.
2. **Transform:** Скрипт `transform_load.py` читает JSON, разворачивает сложную вложенную структуру (способности, типы) в плоские таблицы Pandas.
3. **Load:** Очищенные данные загружаются в две таблицы в PostgreSQL (`pokemons` и `pokemon_types`).
4. **Orchestration:** Airflow DAG (`pokemon_pipeline.py`) запускает Extract и Transform/Load последовательно по расписанию (`@daily`).

## 🚀 Как запустить локально
1. Убедитесь, что у вас установлен Docker Desktop.
2. Клонируйте репозиторий.
3. В корне проекта выполните команду:
   ```bash
   docker-compose up -d --build

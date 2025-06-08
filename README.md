# Реалізація системи для обміну файлами
## Даний проект є реалізацією застосунку SharAll за допомогою якого можна здійснювати безпечний обмін файлами через мережу Інтернет

## Технологічний стек
* Python
* FastApi
* SQLite DB
* AWS S3 Bucket

## Інструкція щодо запуску:
## 1. Встановимо системні залежності

```bash
sudo apt install python3
```

## 2. Створимо робочу директорію та скопіюємо вміст репозиторію
```bash
mkdir app
git clone https://github.com/manabr0w/filesharing-system
```

## 3. Створимо ізольоване середовище для роботи застосунку
```bash
python3 -m venv .venv
source .venv/bin/activate
```
## 4. Встановимо залежності для проекту
```python3
pip install -r requirements.txt
```
## 5. Створимо і заповнимо .env файл за шаблоном

```.env
AWS_BUCKET_NAME=your_backet
AWS_REGION=your_region
AWS_ACCESS_KEY=key
AWS_SECRET_KEY=key
DATABASE_URL="db_url"
```

## 6. Запустимо наш проект
```bash
 uvicorn app.main:app --host 0.0.0.0 --port 8000
```


### Пояснбвальна [записка](https://docs.google.com/document/d/1owjyfgyWtKU2LTts3xRLaUtHc9KNhYI9Y9yMuL3j8rI/edit?usp=sharing) до курсової роботи

FROM python:3.13-slim AS base

# Ishlash papkasini yaratish
WORKDIR /app

# Poetry o'rnatish
RUN pip install --no-cache-dir poetry

# Poetry konfiguratsiya fayllarini nusxalash va o'rnatish
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Loyihani nusxalash
COPY . .


# 8000 portni ochish
EXPOSE 8000

# Dastur ishga tushirish (main.py)
CMD ["python", "main.py"]

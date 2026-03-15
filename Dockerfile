# Përdorim një version të lehtë të Python
FROM python:3.11-slim

# Dosja ku do të qëndrojë kodi brenda Docker
WORKDIR /app

# Kopjojmë listën e paketave (krijoje këtë skedar nëse s'e ke)
COPY requirements.txt .

# Instalojmë libraritë e nevojshme
RUN pip install --no-cache-dir -r requirements.txt

# Kopjojmë pjesën tjetër të projektit
COPY . .

# Porti që do të përdorë Flask
EXPOSE 5000

# Komanda për ta nisur aplikacionin
CMD ["python", "app.py"]
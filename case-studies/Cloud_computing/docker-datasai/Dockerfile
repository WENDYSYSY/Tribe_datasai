# python:3.12-slim : ~150 Mo vs ~1 Go pour l\'image complète
# Toujours fixer la version — jamais "latest"
FROM python:3.12-slim
 
# Désactive les fichiers .pyc et active les logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
 
WORKDIR /app
 
# requirements.txt AVANT le code — optimise le cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
 
COPY . .
 
# Utilisateur non-root — bonne pratique sécurité 2026
RUN adduser --disabled-password --gecos \'\' appuser
USER appuser
 
EXPOSE 8000
 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
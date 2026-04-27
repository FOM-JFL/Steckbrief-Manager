# --- Build Stage ---
FROM python:3.12-slim AS base

# Sicherheits-Best-Practice: Non-root User
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

# Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendung kopieren
COPY api_server.py app.py index.html VERSION ./

# Kein Secret im Image – wird via Environment/Key Vault injiziert
# Non-root User verwenden
USER appuser

# Health-Check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

EXPOSE 5000 6111

CMD ["sh", "-c", "python app.py & python api_server.py"]

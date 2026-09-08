Pagina web de la Dra. Viviana Romero Nossa

## Correr en local

```
cp .env.example .env   # completa las variables SMTP
docker compose up --build
```

Luego abre http://localhost:8010

Si el puerto 8010 también estuviera ocupado por otro proyecto tuyo, cambia el `8010` en `docker-compose.override.yml` por el que prefieras (el `8000` de la derecha es el puerto interno del contenedor, no lo toques).

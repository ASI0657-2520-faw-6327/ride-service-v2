# Imagen oficial con Python 3.13 + uv
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS prod

# Configuración básica
ENV APP_DIR=/app \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    PORT=8000

WORKDIR ${APP_DIR}

# 1) Copiamos definición de dependencias
COPY pyproject.toml uv.lock ./

# 2) Instalamos dependencias del proyecto (solo libs, sin código aún)
RUN uv sync --frozen --no-install-project

# 3) Copiamos el resto del código
COPY . .

# 4) Sincronizamos de nuevo (por si hay extras en pyproject que dependen del código)
RUN uv sync --frozen

# 5) Añadimos el venv al PATH (uv suele usar /app/.venv)
ENV PATH="${APP_DIR}/.venv/bin:${PATH}"

# 6) Exponemos el puerto interno de la app
EXPOSE 8001

# 7) Comando por defecto: ejecutar tu main
CMD ["uv", "run",  "-m", "src.main"]
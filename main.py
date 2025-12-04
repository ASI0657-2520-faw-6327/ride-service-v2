from fastapi import FastAPI

from src.infrastructure.db.session import init_db
from src.interface.api.ride_router import router as ride_router

app = FastAPI(title="Ride Service")


@app.on_event("startup")
def on_startup() -> None:
    """
    Se ejecuta al arrancar la app.
    Aquí inicializamos la base de datos (crear tablas en dev, etc.).
    """
    init_db()


# Montamos las rutas de la capa interface
app.include_router(ride_router)


if __name__ == "__main__":
    import uvicorn

    # IMPORTANTE: el string es "<paquete>.<módulo>:<variable_app>"
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)


import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from psycopg.rows import dict_row
from pydantic import BaseModel

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("Falta DATABASE_URL en el archivo .env")


def conectar():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


app = FastAPI(
    title="Retrobyte API",
    description="Catálogo de videojuegos retro para compra y alquiler",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Videojuego(BaseModel):
    titulo: str
    consola: str
    anio: int
    precio_compra: float
    precio_alquiler: float
    disponible: bool = True
    imagen_url: str | None = None


@app.get("/")
def inicio():
    return {"mensaje": "Hola, Retrobyte API"}


@app.get("/videojuegos")
def listar():
    with conectar() as conn:
        return conn.execute("SELECT * FROM videojuegos ORDER BY id").fetchall()


@app.get("/videojuegos/{id}")
def buscar(id: int):
    with conectar() as conn:
        videojuego = conn.execute(
            "SELECT * FROM videojuegos WHERE id = %s", (id,)
        ).fetchone()
    if videojuego is None:
        raise HTTPException(status_code=404, detail="Ese videojuego no existe")
    return videojuego


@app.post("/videojuegos", status_code=201)
def agregar(videojuego: Videojuego):
    with conectar() as conn:
        return conn.execute(
            """
            INSERT INTO videojuegos (
                titulo, consola, anio, precio_compra, precio_alquiler, disponible, imagen_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                videojuego.titulo,
                videojuego.consola,
                videojuego.anio,
                videojuego.precio_compra,
                videojuego.precio_alquiler,
                videojuego.disponible,
                videojuego.imagen_url,
            ),
        ).fetchone()


@app.put("/videojuegos/{id}")
def editar(id: int, datos: Videojuego):
    with conectar() as conn:
        videojuego = conn.execute(
            """
            UPDATE videojuegos
            SET titulo = %s,
                consola = %s,
                anio = %s,
                precio_compra = %s,
                precio_alquiler = %s,
                disponible = %s,
                imagen_url = %s
            WHERE id = %s
            RETURNING *
            """,
            (
                datos.titulo,
                datos.consola,
                datos.anio,
                datos.precio_compra,
                datos.precio_alquiler,
                datos.disponible,
                datos.imagen_url,
                id,
            ),
        ).fetchone()
    if videojuego is None:
        raise HTTPException(status_code=404, detail="Ese videojuego no existe")
    return videojuego


@app.delete("/videojuegos/{id}", status_code=204)
def borrar(id: int):
    with conectar() as conn:
        borrado = conn.execute(
            "DELETE FROM videojuegos WHERE id = %s RETURNING id", (id,)
        ).fetchone()
    if borrado is None:
        raise HTTPException(status_code=404, detail="Ese videojuego no existe")

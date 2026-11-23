import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("Falta DATABASE_URL en el archivo .env")


def conectar():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


app = FastAPI()


class Album(BaseModel):
    titulo: str
    artista: str
    anio: int


@app.get("/")
def inicio():
    return {"mensaje": "Hola, FastAPI"}


@app.get("/albums")
def listar():
    with conectar() as conn:
        return conn.execute("SELECT * FROM albums ORDER BY id").fetchall()


@app.get("/albums/{id}")
def buscar(id: int):
    with conectar() as conn:
        album = conn.execute(
            "SELECT * FROM albums WHERE id = %s", (id,)
        ).fetchone()
    if album is None:
        raise HTTPException(status_code=404, detail="Ese álbum no existe")
    return album


@app.post("/albums")
def agregar(album: Album):
    with conectar() as conn:
        return conn.execute(
            "INSERT INTO albums (titulo, artista, anio) VALUES (%s, %s, %s) RETURNING *",
            (album.titulo, album.artista, album.anio),
        ).fetchone()


@app.put("/albums/{id}")
def editar(id: int, datos: Album):
    with conectar() as conn:
        album = conn.execute(
            "UPDATE albums SET titulo = %s, artista = %s, anio = %s WHERE id = %s RETURNING *",
            (datos.titulo, datos.artista, datos.anio, id),
        ).fetchone()
    if album is None:
        raise HTTPException(status_code=404, detail="Ese álbum no existe")
    return album


@app.delete("/albums/{id}")
def borrar(id: int):
    with conectar() as conn:
        borrado = conn.execute(
            "DELETE FROM albums WHERE id = %s RETURNING id", (id,)
        ).fetchone()
    if borrado is None:
        raise HTTPException(status_code=404, detail="Ese álbum no existe")
    return {"mensaje": "Álbum borrado"}
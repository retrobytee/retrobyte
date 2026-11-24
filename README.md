# Retrobyte 🎮

Tienda y alquiler de videojuegos retro desarrollada en pareja con **FastAPI**, **Supabase (PostgreSQL)** y frontend en **Stitch**.

## Integrantes
- **[Nombre 1]**
- **[Nombre 2]**

## Enlaces
- **API en Render (`/docs`):** `https://TU-API.onrender.com/docs` *(pendiente de despliegue)*
- **Frontend publicado:** `https://TU-FRONTEND` *(pendiente de despliegue)*

## Base de datos (Supabase)
Crea la tabla `videojuegos` en Supabase con **RLS activado**, `id` automático y al menos 6 filas iniciales:

```sql
CREATE TABLE videojuegos (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  titulo TEXT NOT NULL,
  consola TEXT NOT NULL,
  anio INTEGER NOT NULL,
  precio_compra DOUBLE PRECISION NOT NULL,
  precio_alquiler DOUBLE PRECISION NOT NULL,
  disponible BOOLEAN NOT NULL DEFAULT TRUE,
  imagen_url TEXT
);

ALTER TABLE videojuegos ENABLE ROW LEVEL SECURITY;

INSERT INTO videojuegos (titulo, consola, anio, precio_compra, precio_alquiler, disponible, imagen_url) VALUES
  ('Super Mario World', 'SNES', 1990, 49.99, 4.99, TRUE, 'https://upload.wikimedia.org/wikipedia/en/3/32/Super_Mario_World_Coverart.png'),
  ('The Legend of Zelda: Ocarina of Time', 'Nintendo 64', 1998, 59.99, 5.99, TRUE, 'https://upload.wikimedia.org/wikipedia/en/5/57/The_Legend_of_Zelda_Ocarina_of_Time.jpg'),
  ('Sonic the Hedgehog 2', 'Sega Mega Drive', 1992, 34.99, 3.50, TRUE, 'https://upload.wikimedia.org/wikipedia/en/0/0c/Sonic_2_US_Cover.jpg'),
  ('Chrono Trigger', 'SNES', 1995, 89.99, 7.99, FALSE, 'https://upload.wikimedia.org/wikipedia/en/a/a7/Chrono_Trigger.jpg'),
  ('Metal Gear Solid', 'PlayStation', 1998, 44.99, 4.50, TRUE, 'https://upload.wikimedia.org/wikipedia/en/3/33/Metal_Gear_Solid_cover_art.png'),
  ('Tetris', 'Game Boy', 1989, 24.99, 2.50, TRUE, 'https://upload.wikimedia.org/wikipedia/en/4/4a/Tetris_Boxshot_NES.jpg');
```

## Cómo levantar el proyecto en local

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd retrobyte
   ```

2. **Crear y activar el entorno virtual:**
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Copia `.env.example` a `.env` y coloca tu `DATABASE_URL` de Supabase:
   ```bash
   cp .env.example .env
   ```

5. **Ejecutar la API:**
   ```bash
   uvicorn main:app --reload
   ```
   Luego abre `http://127.0.0.1:8000/docs` en el navegador para probar los endpoints.

## Endpoints principales
- `GET /videojuegos` — Lista todos los videojuegos.
- `GET /videojuegos/{id}` — Obtiene un videojuego por su `id` (devuelve `404` si no existe).
- `POST /videojuegos` — Agrega un videojuego (`201 Created`).
- `PUT /videojuegos/{id}` — Edita un videojuego existente (`404` si no existe).
- `DELETE /videojuegos/{id}` — Elimina un videojuego (`204 No Content`, `404` si no existe).

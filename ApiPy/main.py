from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import pyodbc
from typing import List, Optional

# === CONFIGURACIÓN ===
DATABASE_CONFIG = {
    "server": r"localhost",  # Si no funciona prueba: r".\SQLEXPRESS"
    "database": "TiendaDB",
    "username": "sa",
    "password": "Isravelasco8"  # ← Pon tu contraseña real
}

def get_connection_string():
    return (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']};"
        "Encrypt=optional;"
        "TrustServerCertificate=yes;"
    )

# === MODELOS ===
class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    precio: float
    descripcion: Optional[str] = None

class ProductoCrear(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None

app = FastAPI(title="API Productos", version="1.0.0")

def get_db():
    conn = pyodbc.connect(get_connection_string())
    try:
        yield conn
    finally:
        conn.close()

# === ENDPOINTS ===
@app.get("/")
def raiz():
    return {"mensaje": "¡Todo funciona perfectamente! 🚀 Ve a /docs"}

@app.get("/productos", response_model=List[Producto])
def listar(db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT id, nombre, precio, descripcion FROM Productos")
    return [{"id": r.id, "nombre": r.nombre, "precio": float(r.precio), "descripcion": r.descripcion} for r in cur.fetchall()]

@app.post("/productos", response_model=Producto)
def crear(prod: ProductoCrear, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("INSERT INTO Productos VALUES (?, ?, ?)", prod.nombre, prod.precio, prod.descripcion)
    db.commit()
    cur.execute("SELECT @@IDENTITY AS id")
    return {"id": cur.fetchone()[0], "nombre": prod.nombre, "precio": prod.precio, "descripcion": prod.descripcion}

@app.get("/productos/{id}", response_model=Producto)
def uno(id: int, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("SELECT * FROM Productos WHERE id=?", id)
    r = cur.fetchone()
    if not r: raise HTTPException(404, "No encontrado")
    return {"id": r.id, "nombre": r.nombre, "precio": float(r.precio), "descripcion": r.descripcion}

@app.put("/productos/{id}", response_model=Producto)
def actualizar(id: int, prod: ProductoCrear, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("UPDATE Productos SET nombre=?, precio=?, descripcion=? WHERE id=?", prod.nombre, prod.precio, prod.descripcion, id)
    db.commit()
    if cur.rowcount == 0: raise HTTPException(404, "No encontrado")
    return {"id": id, "nombre": prod.nombre, "precio": prod.precio, "descripcion": prod.descripcion}

@app.delete("/productos/{id}")
def eliminar(id: int, db=Depends(get_db)):
    cur = db.cursor()
    cur.execute("DELETE FROM Productos WHERE id=?", id)
    db.commit()
    if cur.rowcount == 0: raise HTTPException(404, "No encontrado")
    return {"mensaje": "Eliminado ✅"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
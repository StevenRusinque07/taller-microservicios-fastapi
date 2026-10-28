from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Microservicio de Productos", version="1.0.0")

class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int

productos_db: List[Producto] = [
    Producto(id=1, nombre="Laptop Asus ZenBook", precio=1200.0, stock=10),
    Producto(id=2, nombre="Mouse Inalámbrico Logitech", precio=25.0, stock=50),
    Producto(id=3, nombre="Teclado Mecánico RGB", precio=85.0, stock=20)
]

@app.get("/productos", response_model=List[Producto])
def obtener_productos():
    return productos_db

@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int):
    for prod in productos_db:
        if prod.id == producto_id:
            return prod
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.post("/productos", response_model=Producto, status_code=201)
def crear_producto(producto: Producto):
    for prod in productos_db:
        if prod.id == producto.id:
            raise HTTPException(status_code=400, detail="El ID del producto ya existe")
    productos_db.append(producto)
    return producto

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
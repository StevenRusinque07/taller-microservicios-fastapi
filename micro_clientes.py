from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Microservicio de Clientes", version="1.0.0")

class Cliente(BaseModel):
    id: int
    nombre: str
    email: str

clientes_db: List[Cliente] = [
    Cliente(id=101, nombre="Steven Rusinque", email="steven@example.com"),
    Cliente(id=102, nombre="Maria Lopez", email="maria@example.com")
]

@app.get("/clientes", response_model=List[Cliente])
def obtener_clientes():
    return clientes_db

@app.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    for cli in clientes_db:
        if cli.id == cliente_id:
            return cli
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.post("/clientes", response_model=Cliente, status_code=201)
def crear_cliente(cliente: Cliente):
    for cli in clientes_db:
        if cli.id == cliente.id:
            raise HTTPException(status_code=400, detail="El ID del cliente ya existe")
    clientes_db.append(cliente)
    return cliente

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
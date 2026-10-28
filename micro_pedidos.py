from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx

app = FastAPI(title="Microservicio de Pedidos (Resiliente)", version="1.0.0")

PRODUCTOS_URL = "http://127.0.0.1:8001/productos"
CLIENTES_URL = "http://127.0.0.1:8002/clientes"

class PedidoRequest(BaseModel):
    id: int
    cliente_id: int
    producto_id: int
    cantidad: int

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    cliente_nombre: str
    producto_id: int
    producto_nombre: str
    cantidad: int
    precio_unitario: float
    total: float
    estado: str
    nota_resiliencia: Optional[str] = None

pedidos_db: List[PedidoResponse] = []

@app.get("/pedidos", response_model=List[PedidoResponse])
def obtener_pedidos():
    return pedidos_db

@app.post("/pedidos", response_model=PedidoResponse, status_code=201)
async def crear_pedido(pedido_req: PedidoRequest):
    cliente_nombre = "Cliente Desconocido"
    producto_nombre = "Producto Genérico (Fallback)"
    precio_unitario = 0.0
    estado = "COMPLETADO"
    nota_resiliencia = "Todos los servicios respondieron correctamente."

    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            resp_cli = await client.get(f"{CLIENTES_URL}/{pedido_req.cliente_id}")
            if resp_cli.status_code == 200:
                cliente_nombre = resp_cli.json().get("nombre", "Cliente Registrado")
            else:
                raise HTTPException(status_code=400, detail=f"Cliente ID {pedido_req.cliente_id} no existe")
        except httpx.RequestError:
            cliente_nombre = f"Cliente ID {pedido_req.cliente_id} (Verificación diferida)"
            nota_resiliencia = "ADVERTENCIA: Servicio de Clientes no disponible."

        try:
            resp_prod = await client.get(f"{PRODUCTOS_URL}/{pedido_req.producto_id}")
            if resp_prod.status_code == 200:
                prod_data = resp_prod.json()
                producto_nombre = prod_data.get("nombre")
                precio_unitario = prod_data.get("precio", 0.0)
            else:
                raise HTTPException(status_code=400, detail=f"Producto ID {pedido_req.producto_id} no existe")
        except httpx.RequestError:
            estado = "PENDIENTE_VALIDACION_STOCK"
            precio_unitario = 50.0
            nota_resiliencia = "TOLERANCIA A FALLOS ACTIVADA: Servicio de Productos fuera de línea. Pedido registrado en modo degradado."

    total = precio_unitario * pedido_req.cantidad
    nuevo_pedido = PedidoResponse(
        id=pedido_req.id,
        cliente_id=pedido_req.cliente_id,
        cliente_nombre=cliente_nombre,
        producto_id=pedido_req.producto_id,
        producto_nombre=producto_nombre,
        cantidad=pedido_req.cantidad,
        precio_unitario=precio_unitario,
        total=total,
        estado=estado,
        nota_resiliencia=nota_resiliencia
    )

    pedidos_db.append(nuevo_pedido)
    return nuevo_pedido

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)
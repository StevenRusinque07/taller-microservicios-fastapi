# Taller Práctico: Arquitectura de Microservicios (Tienda Virtual)

Este repositorio contiene la solución práctica de arquitectura de microservicios desarrollada con **FastAPI** y **HTTPX**, orientada a garantizar la resiliencia y tolerancia a fallos ante caídas parciales de servicios.

##  Microservicios
- **Productos (Puerto 8001):** Administra el catálogo de la tienda.
- **Clientes (Puerto 8002):** Administra el registro e información de clientes.
- **Pedidos (Puerto 8003):** Orquesta la compra y gestiona la tolerancia a fallos mediante mecanismos de *Fallback*.

##  Instalación y Ejecución
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
# API de Productos 🛒

API REST completa construida con **FastAPI + SQL Server + Docker**.

---

## 📋 ¿Qué hace este proyecto?
- ✅ Crear productos
- ✅ Listar todos los productos
- ✅ Ver un producto por ID
- ✅ Actualizar productos
- ✅ Eliminar productos

---

## 🚀 Cómo levantar el proyecto

```bash
# 1. Descargar o clonar este repositorio
# 2. Entrar a la carpeta del proyecto
cd api-productos

# 3. Levantar todo con Docker
docker-compose up -d --build



## Base de datos — Configuración

Conectarse a SQL Server con estos datos:

- **Servidor**: `localhost`
- **Usuario**: `sa`
- **Contraseña**: `TuContraseña123!`

Ejecutar esta consulta una sola vez:

CREATE DATABASE TiendaDB;
GO

USE TiendaDB;
GO

CREATE TABLE Productos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    descripcion VARCHAR(255)
);
GO

## Probar la API

Abre tu navegador y entra a:
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

Ahí puedes probar todos los botones:

- **POST** → Crear productos
- **GET** → Listar todos
- **GET /{id}** → Ver uno solo
- **PUT /{id}** → Modificar
- **DELETE /{id}** → Eliminar

## Tecnologías usadas

- **FastAPI** — Framework de Python para APIs rápidas
- **SQL Server 2022** — Base de datos
- **Docker** — Para que todo funcione igual en cualquier PC
- **Python 3.14** — Lenguaje de programación


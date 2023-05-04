# API de Monitoreo con sensores ESP32

API desarrollada para monitorear temperatura, humedad y otros datos obtenidos por sensores integrados con ESP32.

# Referencia de la API

#### Obtener todos los datos de todos los sensores

```http
  GET /api/sensores
```

#### Enviar datos desde un sensor

```http
  POST /api/sensores/{id}/{valor}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `integer` | **Required**. ID del sensor que envia los datos |
| `valor` | `float` | **Required**. Valor enviado por el sensor |

#### Obtener todos los usuarios

```http
  GET /api/usuarios
```

#### Agregar un nuevo usuario

```http
  POST /api/usuarios
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Nombre del usuario nuevo |
| `password` | `string` | **Required**. Contraseña del usuario nuevo |

# API desplegada

- https://task-management-api-0ds8.onrender.com/api/tasks

## Tech Stack

**Server:** Flask

## Autores

- [@EmilioRivera0](https://github.com/EmilioRivera0)
- [@C4ncino](https://github.com/C4ncino)
- [@JuanPabloGHC](https://github.com/JuanPabloGHC)
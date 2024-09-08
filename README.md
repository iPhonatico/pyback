
# Parking Reservation System API

Este proyecto gestiona las reservas de parqueo, incluyendo la capacidad dinámica por horarios.

## Requisitos

- Python 3.x
- Django 5.x
- Django REST Framework
- Django Signals
- Postman para realizar pruebas de API

## Endpoints

### 1. Crear una reserva activa

Este endpoint crea una nueva reserva activa y reduce la capacidad del parqueo para el horario seleccionado.

- **Método:** `POST`
- **URL:** `/api/accounting/reservations/`

#### Headers:

```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <your_token>"
}
```

#### Body:

```json
{
  "vehicle": {
    "plate": "ABC123",
    "color": "rojo"
  },
  "parking": 1,
  "parkingSchedule": 2,
  "state": "A",
  "payAmount": 5.00
}
```

### 2. Cancelar una reserva activa

Este endpoint cancela una reserva activa, lo que aumenta la capacidad del parqueo en el horario correspondiente.

- **Método:** `POST`
- **URL:** `/api/accounting/reservations/<id>/cancel/`

#### Headers:

```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <your_token>"
}
```

#### Body:
Ningún body es necesario, solo la acción.

### 3. Eliminar una reserva activa

Este endpoint elimina una reserva activa, lo que restaura la capacidad del parqueo en el horario correspondiente.

- **Método:** `DELETE`
- **URL:** `/api/accounting/reservations/<id>/`

#### Headers:

```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <your_token>"
}
```

#### Body:
Ningún body es necesario, solo la acción.

### 4. Marcar una reserva como pagada

Este endpoint cambia el estado de una reserva a "Pagada".

- **Método:** `POST`
- **URL:** `/api/accounting/reservations/<id>/pay/`

#### Headers:

```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <your_token>"
}
```

#### Body:
Ningún body es necesario, solo la acción.

### 5. Crear una reserva automática

Este endpoint crea una reserva automática basándose en la disponibilidad actual del parqueo y el horario en curso.

- **Método:** `POST`
- **URL:** `/api/accounting/reservations/automatic/`

#### Headers:

```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <your_token>"
}
```

#### Body:

```json
{
  "plate": "DEF456",
  "color": "azul",
  "parking": 1,
  "automatic": true
}
```

### 6. Filtrar reservas por fecha (`ParkingSchedule__date`)

Este endpoint devuelve todas las reservas activas en una fecha específica.

- **Método:** `GET`
- **URL:** `/api/accounting/reservations/?parkingSchedule__date=2024-09-09`

#### Headers:

```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <your_token>"
}
```

### 7. Filtrar reservas por parqueadero

Este endpoint devuelve todas las reservas asociadas a un parqueo específico.

- **Método:** `GET`
- **URL:** `/api/accounting/reservations/?parking=1`

#### Headers:

```json
{
  "Content-Type": "application/json",
  "Authorization": "Token <your_token>"
}
```

## Testing

Puedes utilizar **Postman** para realizar estas solicitudes. Asegúrate de tener los encabezados correctos para la autenticación si tu API está protegida con tokens.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un **pull request** si deseas añadir alguna funcionalidad o mejorar el código existente.


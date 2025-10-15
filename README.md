
# Estructura Propuesta:
    Monolitica con organizacion Layered (Presentacion, Logica de Negocio, Acceso a Datos, Persistencia/Datos)

## Presentacion:
    Modularizada en el directorio /Backend/routes
*   Son las APIs (REST), todos los endpoints basicamente, que permitan la comunicacion con las entidades.
*   Se implementara en un principio con FastAPI (propuesto por Igna Pasté) o se puede usar Flask.
*   Solo va a delegar el trabajo a la logica de negocio, haciendo ciertas validaciones minimas.

## Logica de Negocio:
    Modularizada en el directorio /Backend/services
*   Solo trabaja con lenguaje python, recibe python y devuelve python.
*   Creacion de instancias de entidades, lanzar exceptions, implementacion de las transacciones y llamados a los CRUD para insercion en la BD

## Acceso a Datos:
    Modularizada en el directorio /Backend/repository
*   Implementacion del crud para las entidades del dominio, aquí se va a trabajar con el ORM, SQLAlchemy (propuesto por Igna Pasté).
*   No debe haber lógica, solo implementar el CRUD necesario para persistir los datos.

## Persistencia/Datos:
    Modularizada en el directorio /Backend/models
*   Implementacion de las clases y tablas de la base de datos.
*   Posibilidad de incorporar schemas.py en esta capa al igual que los Models de las clases. Considerar la base de datos en su propio directorio

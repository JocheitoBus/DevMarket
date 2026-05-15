```markdown
# DevMarket Backend - Especificación Técnica

Este repositorio contiene el backend de **DevMarket**, un MVP (Mínimo Producto Viable) de un marketplace para desarrolladores donde se pueden listar y adquirir componentes de software, scripts y plantillas de código.

Este proyecto ha sido desarrollado siguiendo un enfoque de **Aprendizaje Autodidacta**, con el objetivo de consolidar conocimientos avanzados en desarrollo de APIs, diseño de bases de datos relacionales, autenticación segura y aplicación estricta de buenas prácticas de ingeniería de software.

---

## 🚀 Objetivos del Proyecto

- **Desarrollo de APIs RESTful:** Diseño e implementación de endpoints siguiendo los estándares de la industria.
- **Persistencia con MySQL:** Modelado relacional, integridad referencial y uso eficiente de un ORM.
- **Autenticación con JWT:** Flujo seguro de registro e inicio de sesión con tokens sin estado (Stateless).
- **Buenas Prácticas (Clean Code):** Separación estricta de responsabilidades, tipado estático y modularidad.
- **Arquitectura Escalable:** Implementación de *Clean Architecture* para facilitar el mantenimiento y la evolución del sistema.

---

## 🛠️ Stack Tecnológico y Justificación

| Tecnología | Componente / Rol | Justificación Técnica |
| :--- | :--- | :--- |
| **Python 3.10+** | Lenguaje Core | Lenguaje robusto, con un ecosistema backend maduro y soporte fuerte para *Type Hints* (tipado estático moderno), lo que reduce errores en tiempo de ejecución. |
| **FastAPI** | Framework Web | Asíncrono por definición (basado en ASGI), rendimiento comparable a Node.js y Go, validación de datos automática mediante Pydantic y auto-generación de documentación interactiva (Swagger). |
| **MySQL** | Base de Datos Relacional | Garantiza propiedades ACID para transacciones seguras de propiedad. Estructura relacional óptima para mapear usuarios, productos y órdenes mediante llaves foráneas. |
| **SQLAlchemy 2.0** | ORM (Object-Relational Mapping) | Permite interactuar con MySQL mediante objetos de Python utilizando el patrón *Data Mapper*, facilitando el desacoplamiento de las consultas SQL nativas. |
| **PyJWT & Passlib** | Seguridad y Autenticación | Manejo de tokens de sesión sin estado (Stateless) mediante JSON Web Tokens y encriptación segura de contraseñas utilizando el algoritmo *Bcrypt*. |

---

## 📐 Arquitectura del Software (Clean Architecture)

Para asegurar que las reglas de negocio sean completamente independientes de los frameworks, bases de datos o interfaces de usuario, el proyecto se estructura en tres capas esenciales:

* **Capa Core (Dominio/Negocio):** Contiene las entidades puras del sistema y los casos de uso (reglas de negocio como "Registrar un Usuario" o "Procesar una Compra"). No tiene dependencias de librerías externas.
* **Capa de Interfaces (Controladores/Rutas):** Es la puerta de entrada a la aplicación. Los controladores de FastAPI capturan las peticiones HTTP, validan los datos de entrada con esquemas de Pydantic y delegan la ejecución a los Casos de Uso.
* **Capa de Infraestructura:** Contiene las implementaciones tecnológicas concretas: los modelos de base de datos de SQLAlchemy, las conexiones al servidor de MySQL y las librerías de encriptación.

---

## 📂 Estructura de Directorios

```text
devmarket_backend/
├── src/
│   ├── config/                  # Variables de entorno y conexión a la DB
│   ├── core/                    # CAPA CORE (Reglas de negocio puras)
│   │   ├── entities/            # Modelos abstractos (User, Product)
│   │   └── use_cases/           # Lógica de aplicación (RegisterUser, LoginUser)
│   ├── infrastructure/          # CAPA INFRAESTRUCTURA (Tecnología externa)
│   │   ├── database/            # Modelos de SQLAlchemy y sesión de la DB
│   │   ├── repositories/        # Implementación del acceso a datos (MySQL)
│   │   └── security/            # Utilidades de JWT y hashing de contraseñas
│   └── interfaces/              # CAPA INTERFACES (Entrega Web / FastAPI)
│       ├── controllers/         # Orquestadores de peticiones HTTP
│       ├── routes/              # Definición de Endpoints y enrutamiento
│       └── schemas/             # Esquemas de Pydantic para Request/Response
├── main.py                      # Punto de entrada de la aplicación FastAPI
└── requirements.txt             # Dependencias del proyecto
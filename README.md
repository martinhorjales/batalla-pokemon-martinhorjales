# batalla-pokemon-martinhorjales

### Aplicación de batallas pokemon de Martín Horjales UDAW2 

Repo: https://github.com/martinhorjales/batalla-pokemon-martinhorjales.git

### Creación entorno virtual: 
```bash
python -m venv venv
```

### Instalación de flask con los requerimientos:
```bash
.\venv\Scripts\pip install -r requirements.txt
```

### Estructura del Proyecto (Arquitectura por Capas):
```text
mi_proyecto/
├─ requirements.txt
├─ venv/
├─ data/
│  └─ pokemons-starters.json
└─ app/
   ├─ main.py
   ├─ deps.py
   ├─ forms/        — Formularios de Flask-WTF para validación segura.
   ├─ models/       — Clases POO que representan el dominio (Pokemon, Trainer).
   ├─ repositories/ — Lógica de acceso a datos (lectura del JSON).
   ├─ routes/       — Controladores organizados en Blueprints.
   ├─ services/     — Lógica de negocio adicional.
   ├─ static/       — Archivos CSS, JavaScript e imágenes de la interfaz.
   └─ templates/    — Plantillas HTML renderizadas con Jinja2.
```

## Arquitectura y Blueprints (Fase IV)
Para mantener el código modular y escalable, el sistema de rutas se ha dividido en dos *Blueprints* principales:
1. **`usuario_bp` (`/usuario_routes.py`):** Aisla toda la lógica de sesión. Se encarga de la pantalla de bienvenida, la validación del nombre a través de Flask-WTF y el cierre de sesión (`logout`).
2. **`pokemon_bp` (`/pokemons_route.py`):** Agrupa todo el dominio principal de la aplicación. Gestiona el listado, los filtros de búsqueda por GET, la visualización de detalles por ID y el sistema de batalla.

## Flujo de Interacción y Vistas
1. **Página Principal:** Pantalla de aterrizaje estática.
2. **Identificación:** Vista con un formulario seguro (protección CSRF) donde el usuario introduce su nombre. Si ya está identificado, redirige automáticamente.
3. **Listado de Pokémon (Pokedex):** Muestra todos los Pokémon. Permite filtrar por tipo, peso y altura enviando los datos por `GET` en la URL. Solo accesible para entrenadores registrados.
4. **Detalle Pokémon:** Muestra la información extendida de un Pokémon específico según su ID.
5. **Batalla:** Vista inmersiva donde el Pokémon seleccionado por el usuario se enfrenta a un rival elegido aleatoriamente (excluyendo al propio Pokémon del usuario).

## Uso de la Sesión (Justificación Fase III)
Se ha implementado `Flask-Session` configurado para guardar los datos en ficheros locales (`.flask_session`). Se almacenan los siguientes datos con sus respectivas justificaciones:

* **`trainer`**: Guarda el nombre del usuario validado. **Motivo:** Es esencial para proteger las rutas. Un decorador `@login_required` comprueba su existencia; si no está, bloquea el acceso al listado y la batalla, redirigiendo a la pantalla de identificación. Además, se usa para mostrar el nombre en la interfaz.
* **`pokemon`**: Almacena una lista que contiene el diccionario del Pokémon escogido por el jugador y sus 4 ataques aleatorios. **Motivo:** Garantiza que, si el usuario recarga la página `/batalla-pokemon` en medio de un combate, el luchador y sus ataques sigan siendo exactamente los mismos, evitando perder el estado actual.
* **`pokemonRival`**: Almacena el diccionario del Pokémon enemigo seleccionado al azar. **Motivo:** Al igual que con el Pokémon del jugador, es obligatorio guardarlo en sesión para mantener la consistencia. Si no se guardara, cada vez que el usuario refrescara la página o enviara una acción, el rival cambiaría de forma aleatoria, rompiendo la lógica de la batalla.

## Arquitectura y Refactorización (Fase IV)
Para preparar el proyecto para futuras ampliaciones, el código ha sido reorganizado siguiendo una arquitectura en capas dentro del directorio `app/`, separando claramente la lógica de presentación, negocio y datos.

* **Modelos (POO):** La representación del dominio de la aplicación (entidades como el Pokémon o el Entrenador) se ha implementado utilizando Programación Orientada a Objetos (clases y *dataclasses*) dentro de la carpeta `models/`.
* **Blueprints:** La lógica de enrutamiento se ha extraído a la carpeta `routes/` utilizando dos *Blueprints* distintos. Se ha estructurado así para aislar la gestión del usuario y la sesión (`usuario_bp`) de la lógica principal de la aplicación, que es la visualización y el combate de las criaturas (`pokemon_bp`).
* **Formularios con Flask-WTF:** Para gestionar las entradas del usuario de forma segura y modular, se creó el directorio `forms/`. Se migró el formulario HTML de identificación a una clase de Flask-WTF (`EntrenadorForm`), añadiendo validación en el backend y protección CSRF.
* **Flujo de Interacción:** El usuario debe registrarse a través de la vista de identificación (controlada de forma segura por WTF). Una vez validados sus datos, el flujo le permite navegar por el listado de Pokémon y acceder a las batallas.
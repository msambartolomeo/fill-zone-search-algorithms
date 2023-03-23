# fill-zone-search-algorithms

[Enunciado](docs/SIA_TP1.pdf)

### Requisitos

- Python3
- pip3
- [pipenv](https://pypi.org/project/pipenv/)

### Instalación

Ejecutar

```sh
pipenv install
```

para instalar las dependencias necesarias en el ambiente virtual

## Ejecución

```sh
pipenv run python main.py [config_file]
```

### Archivo de configuración

Para configurar la ejecución es necesario un archivo de configuración el cual especifique parámetros que necesita el programa para funcionar.
A continuación se detalla el formato del archivo de configuración.

- `logging_level`: nivel de debug
- `game`: seleccionar el juego -- Options(8-puzzle, fill-zone)

El resto de los settings son diferentes dependiendo de la eleccion de `game`

Para "fill-zone":
- `board_settings`: configuración sobre la generación del tablero del fill zone
  - `type`: forma de generar el tablero, define cuales de los siguientes parámetros serán considerados -- Options(static, random)
  - `board`: (type = "static") string que describa el tablero, con un numero identificando cada color por ejemplo "4,5,5,3;4,3,0,3;3,4,0,2;1,5,1,0" es una matriz 4x4
  - `board_size`: (type = "random") numero entero que representa el lado de la matriz a generar
  - `color_count`: (type = "random") numero entero que representa la cantidad de colores de la matriz a generar
- `search_settings`: configuración sobre el algoritmo a utilizar para hacer la búsqueda
  - `algorithm`: algoritmo a utilizar para la búsqueda -- Options(bfs, dfs, A*, greedy, iddfs)
  - `heuristic`: heurística a utilizar si el algoritmo lo utiliza -- Options(eccentricity, color_count, combination, node_count)
  - `depth`: (algorithm = "iddfs") numero entero que representa la profundidad inicial para iddfs
  - `update_depth`: (algorithm = "iddfs") numero entero que define cuanto se amuenta la profundidad despues de cada iteracion
  
Para "8-puzzle":

- `board_settings`: configuración sobre la generación del tablero de 8 puzzle
  - `board`: estado inicial del tablero, por ejemplo "5,7,3;8,2,None;1,6,4"
  - `goal`: estado final del tablero, por ejemplo "1,2,3;8,None,4;7,6,5"
- `search_settings`: configuración sobre el algoritmo a utilizar para hacer la búsqueda
  - `algorithm`: algoritmo a utilizar para la búsqueda -- Options(bfs, dfs, A*, greedy, iddfs)
  - `heuristic`: heurística a utilizar si el algoritmo lo utiliza -- Options(manhattan, out_of_place)
  
De todas formas se incluyen archivos de configuracion de ejemplo para el [fill-zone](config_fill_zone.example.json) y para el [8-puzzle](config_8_puzzle.example.json)

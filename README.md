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
- `board_settings`: configuración sobre la generación del tablero del fill zone
  - `type`: forma de generar el tablero, define cuales de los siguientes parámetros serán considerados -- Options(static, random)
  - `board`: (type = "static") string que describa el tablero, con un numero identificando cada color por ejemplo "4,5,5,3;4,3,0,3;3,4,0,2;1,5,1,0" es una matriz 4x4
  - `board_size`: (type = "random") numero entero que representa el lado de la matriz a generar
  - `color_count`: (type = "random") numero entero que representa la cantidad de colores de la matriz a generar
- `search_settings`: configuración sobre el algoritmo a utilizar para hacer la búsqueda
  - `algorithm`: algoritmo a utilizar para la búsqueda -- Options(bfs, dfs, A*, greedy) (iddfs se encuentra en su propia branch)
  - `heuristic`: heurística a utilizar si el algoritmo lo utiliza -- Options(eccentricity, color_count, combination, node_count)
  
De todas formas se incluye un [archivo de configuración de ejemplo](config.example.json)

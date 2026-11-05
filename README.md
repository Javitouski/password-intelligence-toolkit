# Password Intelligence Toolkit

[![CI Code Quality](https://github.com/Javitouski/password-intelligence-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Javitouski/password-intelligence-toolkit/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)

Herramienta modular desarrollada en **Python** para el análisis de seguridad de contraseñas, estimación teórica de entropía y auditoría local de hashes SHA-256 mediante ataques de fuerza bruta y diccionario.

El proyecto está orientado al aprendizaje de programación, algoritmos de búsqueda, criptografía aplicada y buenas prácticas de ingeniería de software.

## Características

- **Análisis de entropía:** Cálculo de la entropía teórica en bits según la longitud y el conjunto de caracteres utilizado, con estimaciones de tiempo basadas en benchmarking local.
- **Ataque por fuerza bruta:** Generación secuencial de combinaciones de caracteres mediante `itertools.product`, con soporte para letras mayúsculas, minúsculas, números y símbolos.
- **Ataque por diccionario:** Procesamiento de archivos de contraseñas línea por línea, evitando cargar el diccionario completo en memoria RAM.
- **Generación de hashes:** Conversión de texto plano a hashes SHA-256 mediante `hashlib`.
- **CLI con argparse:** Interfaz de línea de comandos organizada en subcomandos independientes.
- **Calidad de código:** Integración de MyPy, Pytest y GitHub Actions para análisis estático y pruebas automatizadas.

## Arquitectura del proyecto

```text
password-intelligence-toolkit/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── cracker/
│       ├── attacks/
│       │   ├── brute_force.py
│       │   └── dictionary.py
│       ├── engine.py
│       ├── hashes.py
│       ├── models.py
│       └── utils.py
├── tests/
├── .gitignore
├── dictionary.txt
├── main.py
└── README.md
```

La arquitectura separa las responsabilidades principales:

- `main.py`: Gestión de argumentos, validación inicial y presentación de resultados.
- `engine.py`: Orquestación de las operaciones mediante `CrackerEngine`.
- `attacks/`: Implementación de los algoritmos de búsqueda.
- `hashes.py`: Generación de hashes SHA-256.
- `models.py`: Modelos de resultados tipados mediante `@dataclass`.
- `utils.py`: Benchmarking local y estimaciones de entropía.
- `tests/`: Pruebas automatizadas del proyecto.

## Requisitos

- Python 3.11 (versión utilizada en CI).
- Git para clonar el repositorio.
- MyPy y Pytest para ejecutar las comprobaciones de desarrollo.

## Instalación

**1. Clonar el repositorio**

```bash
git clone https://github.com/Javitouski/password-intelligence-toolkit.git
cd password-intelligence-toolkit
```

**2. Crear un entorno virtual (recomendado)**

```bash
python -m venv .venv
```

Activar el entorno según el sistema operativo:

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

**3. Instalar herramientas de desarrollo**

```bash
python -m pip install mypy pytest
```

Las funcionalidades principales utilizan módulos de la biblioteca estándar de Python.

## Uso

El proyecto utiliza una CLI basada en subcomandos.

Para visualizar la ayuda general:

```bash
python main.py --help
```

### 1. Generar un hash SHA-256

```bash
python main.py hash "abc"
```

Resultado esperado:

```text
[+] Plain text: abc
[+] SHA-256   : ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```

### 2. Ataque por diccionario

```bash
python main.py dict <HASH_SHA256> -w dictionary.txt
```

Parámetros:

- `<HASH_SHA256>`: Hash SHA-256 de 64 caracteres hexadecimales.
- `-w, --wordlist`: Ruta del archivo que contiene las contraseñas candidatas.

El programa compara el hash de cada entrada del diccionario con el hash objetivo.

### 3. Ataque por fuerza bruta

```bash
python main.py brute <HASH_SHA256> -l 4 --lower --digits
```

Parámetros disponibles:

| Parámetro | Descripción |
|---|---|
| `-l, --length` | Longitud máxima de las combinaciones |
| `--lower` | Letras minúsculas |
| `--upper` | Letras mayúsculas |
| `--digits` | Dígitos del 0 al 9 |
| `--symbols` | Símbolos especiales |

Los conjuntos de caracteres pueden combinarse.

Antes de iniciar el ataque, la herramienta ejecuta un benchmark local para estimar la velocidad de cálculo de hashes SHA-256.

**Limitación actual:** Si el tiempo estimado supera los 300 segundos, la CLI informa al usuario y no inicia el ataque de fuerza bruta.

## Entropía y benchmarking

La herramienta calcula la entropía teórica mediante:

$$
H = L \times \log_2(N)
$$

Donde:

- `H`: Entropía teórica expresada en bits.
- `L`: Longitud de la contraseña considerada.
- `N`: Cantidad de caracteres disponibles en el conjunto seleccionado.

El benchmark mide la velocidad aproximada de cálculo SHA-256 del equipo local y la utiliza para estimar tiempos de búsqueda.

Estas estimaciones suponen una distribución uniforme de contraseñas y no representan necesariamente la resistencia real de una contraseña elegida por una persona.

## Calidad de código y testing

El proyecto utiliza **GitHub Actions** para ejecutar automáticamente verificaciones en eventos `push` y `pull_request` sobre la rama `main`.

El pipeline incluye:

- **MyPy:** Verificación estática de tipos.
- **Pytest:** Ejecución automatizada de las pruebas disponibles.
- **Python 3.11:** Entorno utilizado por el workflow de integración continua.

### Verificación de tipos

```bash
mypy --explicit-package-bases main.py src/
```

### Ejecución de pruebas

```bash
pytest -v
```

## Limitaciones actuales

- La auditoría se limita a hashes SHA-256 sin salt.
- Los ataques se ejecutan localmente y sin aceleración por GPU.
- La estimación de entropía se basa en el espacio de búsqueda teórico.
- El benchmarking representa el rendimiento aproximado del entorno local.
- La CLI no incluye actualmente un menú interactivo.

## Exención de responsabilidad

Este proyecto fue desarrollado exclusivamente con fines educativos, investigación en ciberseguridad y auditorías de seguridad autorizadas.

La herramienta debe utilizarse únicamente sobre hashes propios o sistemas y datos para los cuales exista autorización expresa.

El autor no se responsabiliza por usos indebidos o no autorizados de este software.

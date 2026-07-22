```markdown
# Password Intelligence Toolkit
[![CI Code Quality](https://github.com/Javitouski/password-intelligence-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Javitouski/password-intelligence-toolkit/actions)

Herramienta modular en Python diseñada para el análisis de seguridad, cálculo de entropía y auditoría de hashes (SHA-256) mediante ataques de fuerza bruta y diccionario.

## Características

* **Análisis de Entropía:** Cálculo matemático de la fortaleza de contraseñas y estimación de tiempos de rotura.
* **Ataque por Fuerza Bruta:** Generación secuencial de combinaciones configurables (mayúsculas, minúsculas, números, símbolos).
* **Ataque por Diccionario:** Lectura eficiente línea por línea para mitigar consumo de memoria en archivos grandes.
* **Generador de Hashes:** Herramienta de conversión de texto plano a SHA-256.

## Arquitectura

```text
password-intelligence-toolkit/
├── .github/workflows/    # Pipelines de Integración Continua (GitHub Actions)
├── src/
│   └── cracker/          # Paquete principal
│       ├── attacks/      # Módulos independientes de ataques
│       ├── engine.py     # Orquestador principal (CrackerEngine)
│       ├── models.py     # Estructuras de datos (@dataclass)
│       └── utils.py      # Benchmark y cálculo de entropía
├── main.py               # Interfaz de línea de comandos (CLI)
└── README.md
```

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Javitouski/password-intelligence-toolkit.git](https://github.com/Javitouski/password-intelligence-toolkit.git)
   cd password-intelligence-toolkit
   ```

2. **Instalar dependencias:**
   ```bash
   pip install mypy pytest
   ```

## Uso

Para iniciar la interfaz interactiva de línea de comandos (CLI):

```bash
python main.py
```

## Calidad de Código

El proyecto utiliza **MyPy** para la verificación estática de tipos y **GitHub Actions** para CI/CD automático en cada `push`.

Para ejecutar la revisión de tipos manualmente:
```bash
mypy --explicit-package-bases main.py src/
```

## Exención de Responsabilidad

Este proyecto fue desarrollado exclusivamente con fines educativos y de investigación en ciberseguridad.

```

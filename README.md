# App de Logística Valencia

### Configuración de `flake8`
Este es un fragmento de configuración para `flake8`, una herramienta de linting para Python que revisa el código en busca de errores y problemas de estilo.

#### Opciones configuradas:
1. **`max-line-length = 88`**  
   - Define la longitud máxima de una línea en **88 caracteres** (en lugar de los 79 caracteres predeterminados de PEP 8).

2. **`ignore = E203, E266, E501, W503`**  
   - Ignora los siguientes errores:
     - **`E203`**: Espacios antes de `:` en slices (e.g., `x[1 : 2]`).
     - **`E266`**: Demasiados `#` al inicio de un comentario (e.g., `### Comentario`).
     - **`E501`**: Línea demasiado larga (ya controlada por `max-line-length`).
     - **`W503`**: Salto de línea antes de un operador binario (e.g., `+`, `-`).
`
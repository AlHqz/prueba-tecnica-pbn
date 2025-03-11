# Prueba Técninca

Prueba técnica para PBN para agregar recursos educativos al repositorio a través de un script en Python.

## Requisitos
*   Python 3.7+ (o superior).  El script ha sido probado con Python 3.9, 3.10, 3.11 y 3.12.
*   Bibliotecas de Python:
    *   requests (para hacer las llamadas a la API)
    *   python-dotenv (para manejar el token)

# Primer paso, instala las dependencias necesarias
```bash
pip install requests python-dotenv
```

# Segundo, manejo de token de API de GitHub
1.  Consigue tu token en Settings->Developer Settings
2.  Clona el repositorio a tu computadora
3.  En la carpeta donde está este archivo y el archivo .py, crea un nuevo archivo llamado .env (sin extensión)
4.  Dentro del archivo escribe lo siguiente: GITHUB_TOKEN=<TuToken> (Reemplaza <TuToken> por el token que generaste)
5.  Para mayor seguridad, en caso de que hagas cambios y lo subas a tu propio repositorio de GitHub. Crea un archivo .gitignore y dentro del mismo, escribe .env. Esto evitará que el archivo .env con tu token se suba a tu repositorio de GitHub

# Tercero, instrucciones de uso (Windows)
1. Activa el virtual environment:
```bash
.venv\Scripts\activate
```
3. Ejecuta el script desde el IDE o consola:
```bash
py prueba_tecnica.py
```

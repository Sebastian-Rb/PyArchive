# PyArchive - Sistema de gestion de archivos con CLI
**Sistemas Operativos — Grupo 11**

Gestor de archivos interactivo por consola que simula y visualiza las llamadas al sistema (syscalls) involucradas en operaciones comunes del sistema de archivos. Desarrollado como parte del trabajo práctico sobre llamadas al sistema en sistemas operativos.

---

## Requisitos

- Python 3.8+
- [rich](https://github.com/Textualize/rich)

```bash
pip install rich
```

---

## Uso

```bash
irm https://raw.githubusercontent.com/Sebastian-Rb/PyArchive/main/GestorArchivos.py | python -
```

Se abre una consola interactiva. Escribe `help` para ver todos los comandos.

---

## Comandos

| Comando | Descripción | Syscalls simuladas |
|---|---|---|
| `mkdir <nombre>` | Crear una carpeta | `mkdir()` |
| `crear <nombre> <texto>` | Crear archivo y escribir contenido | `open()`, `write()`, `close()` |
| `leer <nombre>` | Leer contenido de un archivo | `open()`, `read()`, `close()` |
| `chmod <perms> <nombre>` | Cambiar permisos (ej: `chmod 644 arch.txt`) | `chmod()` |
| `ls [ruta]` | Listar archivos del directorio actual | `getdents()` |
| `cd <ruta>` | Cambiar de directorio | `chdir()` |
| `pwd` | Mostrar ruta actual | `getcwd()` |
| `rm <nombre>` | Eliminar archivo o carpeta | `unlink()`, `rmdir()` |
| `demo` | Ejecutar demostración completa | todas las anteriores |
| `exit` | Salir | — |

---

## Demo rápida

El comando `demo` ejecuta automáticamente todos los comandos en secuencia: crea una carpeta, crea un archivo, escribe contenido, lo lee y cambia sus permisos.

```bash
(filemgr) demo
```

---

## Tarea 1 S3

Ingeniera si lee esto ponganos 10

El programa permite ver las llamadas al sistema con ejemplos ejectuados.

- Apertura y lectura de archivos
- Escritura y creación de archivos
- Creación de directorios
- Modificación de permisos
- Navegación del sistema de archivos

Cada operación tiene nombradas las syscalls equivalentes en sistemas UNIX/Linux (`open`, `read`, `write`, `close`, `chmod`, `mkdir`, `chdir`, `getcwd`, `getdents`, `unlink`).

---

## Integrantes

- <!-- nombre -->
- <!-- nombre -->
- <!-- nombre -->
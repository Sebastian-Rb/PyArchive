import cmd
import os
import stat
import shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text


# ───────────── Changelogs ────────────
# vzzzz Le cambie excepciones genéricas por OSError en casos de lectura/escritura de archivos, errores especificos por llamadas al sistema
# Comando DEMO para probar todo el flujo de operaciones.


console = Console()

# ──────────── Helper de salida ──────────── (Funciones para formatear la salida en la consola, color con rich y eso)
def syscall(name, descripcion):
    console.print(f"  [bold cyan][syscall][/bold cyan] [yellow]{name}[/yellow] → {descripcion}")

def ok(msg):
    console.print(f"  [bold green][OK][/bold green] {msg}")

def error(msg):
    console.print(f"  [bold red][ERROR][/bold red] {msg}")

def action(titulo):
    console.rule(f"[bold blue]{titulo}[/bold blue]")


# ──────────── Gestor de archivos ────────────    
class FileManager(cmd.Cmd):
    intro = ''
    prompt = '\n(filemgr)'

    def preloop(self):
        console.print(Panel(
            "[bold cyan]Grupo 11[/bold cyan] - Gestor de Archivos\n"
            "Integrantes: \n"
            "[yellow]Sebastian[/yellow] Ramirez\n"
            "[yellow][/yellow] \n"
            "[yellow][/yellow] \n"
            "[yellow][/yellow] \n"
            "[dim]Escribe [bold yellow]help[/bold yellow] para ver los comandos disponibles.[/dim]",
            box =box.DOUBLE,
            border_style="cyan", 
        ))
    
    # ──────────── Comandos base ──────────── (listar, cambiar directorio, mostrar directorio actual, eliminar archivos/directorios) 
    def do_ls(self, arg):
        "Listar archivos/directorios del directorio actual"
        action("ls - Listar archivos/directorios")
        syscall("getdents()", "leyendo directorio actual")

        ruta = arg.strip() if arg.strip() else "."
        try:
            entradas = os.listdir(ruta)
            table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
            table.add_column("Nombre")
            table.add_column("Tipo")
            table.add_column("Tamaño")

            for nombre in sorted(entradas):
                ruta_completa = os.path.join(ruta, nombre)
                tipo = "[blue]DIR[/blue]" if os.path.isdir(ruta_completa) else "[white]FILE[/white]"

                try:
                    tamaño = os.path.getsize(ruta_completa)
                except OSError: 
                    tamaño = "N/A"
                table.add_row(nombre, tipo, str(tamaño))
            
            console.print(table)
            ok(f"{len(entradas)} entradas encontradas.")
        except Exception as e:
            error(f"No se pudo listar el directorio: {e}")
    
    def do_cd(self, arg):
        "Cambiar el directorio actual: cd <ruta>"
        action("cd - Cambiar directorio")
        if not arg.strip():
            error("Debes especificar un directorio. Ej: cd carpetaname")
            return
        syscall("chdir()", f"cambiando al directorio '{arg}'")
        try:
            os.chdir(arg)
            ok(f"Directorio cambiado a: {os.getcwd()}")
        except FileNotFoundError:
            error(f"El directorio '{arg}' no existe.")
        except PermissionError:
            error(f"No tienes permisos para acceder a '{arg}'.")

    def do_pwd(self, arg):
        "Mostrar el directorio actual"
        action("pwd - Directorio actual")
        syscall("getcwd()", "obteniendo directorio actual")
        ok(os.getcwd())

    def do_rm(self, arg):
        "Eliminar un archivo o directorio: rm <nombre>"
        action("rm - Eliminar")
        if not arg.strip():
            error("Especifique que quiere eliminar. Ej: rm archivo.txt")
            return
        if not os.path.exists(arg):
            error(f"'{arg}' no existe.")
            return
        try:
            if os.path.isdir(arg):
                syscall("rmdir() / unlinkat()", f"eliminando '{arg}'...")
                shutil.rmtree(arg)
            else:
                syscall("unlink()", f"eliminando '{arg}'...")
                os.remove(arg)
            ok(f"'{arg}' ha sido eliminado.")
        except PermissionError:
            error(f"No tienes permisos para eliminar '{arg}'.")

    # ──────────── Comando de trabajo ──────────── (Comando para crear un archivo)

    def do_mkdir(self, arg):
        "Crear nueva carpeta: mkdir <nombre>"
        action("mkdir - Crear carpeta")
        if not arg.strip():
            error("Especifique el nombre. Ej: mkdir nueva_carpeta")
            return
        syscall("mkdir()", f"creando carpeta '{arg}'...")
        try:
            os.mkdir(arg)
            ok(f"Carpeta '{arg}' creada.")
        except FileExistsError:
            error(f"'{arg}' ya existe.")
        except PermissionError:
            error(f"No tienes permisos para crear carpetas aqui.")

    def do_crear(self, arg):
        "Crear un nuevo archivo con contenido: crear <nombre> <contenido>..."
        action("crear - Crear archivo")
        partes = arg.strip().split(' ', 1)
        if len(partes) < 2:
            error("Como usar: crear <nombre> <contenido>. Ej: asdf.txt 'ASDF'")
            return
        
        nombre, contenido = partes[0], partes[1]

        syscall("open(O_CREAT | O_WRONLY)", f"abriendo/creando '{nombre}'")
        syscall("write()", f"escribiendo {len(contenido)} bytes")
        syscall("close()", "cerrando descriptor de archivo")

        try:
            with open(nombre, "w", encoding="utf-8") as f:
                f.write(contenido)
            ok(f"Archivo '{nombre}' creado con {len(contenido)} caracteres")
        except PermissionError:
            error("Sin permisos para escribir aquí")
        except OSError as e:  
            error(f"Error: {e}")
    
    def do_leer(self, arg):
        "Leer el contenido de un archivo: leer <nombre>"
        action("leer — Leer archivo")
        if not arg.strip():
            error("Especifica un archivo. Ej: leer notas.txt")
            return
        
        syscall("open(O_RDONLY)", f"abriendo '{arg}' en modo lectura")
        syscall("read()", "leyendo contenido del archivo")
        syscall("close()", "cerrando descriptor de archivo")

        try:
            with open(arg, "r", encoding="utf-8") as f:
                contenido = f.read()
            console.print(Panel(contenido, title=f"[cyan]{arg}[/cyan]", border_style="dim"))
            ok(f"length: {len(contenido)} caracteres leidos")
        except FileNotFoundError:
            error(f"'{arg}' no existe.")
        except PermissionError:
            error(f"No tienes permisos para leer '{arg}'.")
        except OSError as e:  
            error(f"Error de lectura: {e}")

    def do_chmod(self, arg):
        "Cambiar permisos de un archivo: chmod <permisos> <nombre>  →  Ej: chmod 644 notas.txt"
        action("chmod — Cambiar permisos")
        partes = arg.strip().split()
        if len(partes) != 2:
            error("Uso: chmod <permisos> <nombre>  →  Ej: chmod 644 notas.txt")
            return

        permisos_str, nombre = partes[0], partes[1]

        try:
            permisos_oct = int(permisos_str, 8)
        except ValueError:
            error(f"'{permisos_str}' no es un número octal válido.")
            return
        
        syscall("chmod()", f"cambiando permisos de '{nombre}' a {permisos_str}")
        try:
            os.chmod(nombre, permisos_oct)
            # Mostrar los permisos resultantes
            modo = oct(stat.S_IMODE(os.stat(nombre).st_mode))
            ok(f"Permisos de '{nombre}' cambiados a {modo}")
        except FileNotFoundError:
            error(f"'{nombre}' no existe.")
        except PermissionError:
            error(f"Sin permisos para cambiar esto")
        except OSError as e: 
            error(f"Error al cambiar permisos: {e}")
        
    def do_demo(self, arg):
        "Ejecutar demo completa de todas las operaciones del trabajo"
        action("DEMO — Simulación completa de syscalls")
        console.print("[dim]Ejecutando todos los pasos del trabajo...[/dim]\n")

        carpeta = "grupo11_demo"
        archivo = f"{carpeta}/notas.txt"

        # Crear carpeta
        console.print("[bold]Paso 1: Crear carpeta[/bold]")
        self.do_mkdir(carpeta)

        # Crear archivo con contenido
        console.print("\n[bold]Paso 2: Crear archivo y escribir[/bold]")
        self.do_crear(f"{archivo} Sistemas Operativos - Grupo 11 - Llamadas al sistema")

        # Leer contenido
        console.print("\n[bold]Paso 3: Leer contenido[/bold]")
        self.do_leer(archivo)

        # Cambiar permisos
        console.print("\n[bold]Paso 4: Cambiar permisos[/bold]")
        self.do_chmod(f"644 {archivo}")

        console.print()
        ok("[bold green]Demo completada. Carpeta 'grupo11_demo' creada con el archivo.[/bold green]")

    def do_exit(self, arg):
        "Salir del gestor"
        console.print("\n[dim]Cerrando gestor de archivos...[/dim]")
        return True

    # ──────────Salida (Cuadro de help formateado)──────────
    def do_help(self, arg):
        tabla = Table(title="Comandos disponibles", box=box.ROUNDED, border_style="cyan")
        tabla.add_column("Comando", style="yellow")
        tabla.add_column("Descripción")

        comandos = [
            ("ls [ruta]",              "Listar archivos del directorio actual"),
            ("pwd",                    "Mostrar ruta actual"),
            ("cd <ruta>",              "Cambiar de directorio"),
            ("mkdir <nombre>",         "Crear una carpeta"),
            ("crear <nombre> <texto>", "Crear archivo y escribir contenido"),
            ("leer <nombre>",          "Leer contenido de un archivo"),
            ("chmod <perms> <nombre>", "Cambiar permisos (ej: chmod 644 arch.txt)"),
            ("rm <nombre>",            "Eliminar archivo o carpeta"),
            ("demo",                   "Ejecutar demo completa de todas las operaciones"),
            ("exit",                   "Salir"),
        ]
        for cmd_nombre, desc in comandos:
            tabla.add_row(cmd_nombre, desc)

        console.print(tabla)


if __name__ == "__main__":
    FileManager().cmdloop()
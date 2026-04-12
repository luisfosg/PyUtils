import os
import importlib
import sys
import argparse

COMMANDS_FOLDER = "commands"


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80


def centered(text, width=None):
    if width is None:
        width = get_terminal_width()
    return text.center(width)


def load_commands(folder):
    commands = {}
    if not os.path.exists(folder):
        print(f"La carpeta '{folder}' no existe. Creándola...")
        os.makedirs(folder)
        return commands

    sys.path.insert(0, folder)

    for filename in os.listdir(folder):
        if filename.endswith(".py") and not filename.startswith("_"):
            module_name = filename[:-3]
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "run"):
                    commands[module_name] = module.run
                else:
                    pass
            except ImportError:
                pass
            except Exception:
                pass

    sys.path.pop(0)
    return commands


def show_menu(commands):
    width = min(get_terminal_width(), 60)
    print()
    print("┌" + "─" * (width - 2) + "┐")
    print("│" + centered("🛠️  PYTHON TOOLBOX", width - 2) + "│")
    print("├" + "─" * (width - 2) + "┤")

    if not commands:
        print("│" + centered("No hay comandos disponibles", width - 2) + "│")
    else:
        for i, command in enumerate(commands.keys(), start=1):
            cmd_display = f"  {i}. {command.replace('_', ' ').title()}"
            print("│" + cmd_display.ljust(width - 2) + "│")

    print("├" + "─" * (width - 2) + "┤")
    print("│" + centered("0. Salir", width - 2) + "│")
    print("└" + "─" * (width - 2) + "┘")


def main():
    commands = load_commands(COMMANDS_FOLDER)

    if not commands:
        print(
            "No hay comandos disponibles. Añade archivos .py en la carpeta 'commands' con una función 'run'."
        )
        return

    args_parser = argparse.ArgumentParser(description="PyToolbox CLI")
    args_parser.add_argument("command", nargs="?", help="Comando a ejecutar")
    args_parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="Argumentos para el comando"
    )
    parsed = args_parser.parse_args()

    if parsed.command:
        if parsed.command in commands:
            print(f"\n▶ Ejecutando: {parsed.command.replace('_', ' ').title()}")
            print("─" * 40)
            commands[parsed.command](parsed.args)
            print("─" * 40)
            print("✅ Completado\n")
        else:
            print(f"Comando '{parsed.command}' no encontrado.")
            print(f"Comandos disponibles: {', '.join(commands.keys())}")
        return

    while True:
        show_menu(commands)
        choice = input("  → ").strip()

        if choice == "0":
            print("\n👋 ¡Hasta luego!")
            break

        try:
            choice = int(choice)
            if 1 <= choice <= len(commands):
                command_name = list(commands.keys())[choice - 1]
                print(f"\n▶ Ejecutando: {command_name.replace('_', ' ').title()}")
                print("─" * 40)
                remaining_args = sys.argv[2:] if len(sys.argv) > 2 else []
                commands[command_name](remaining_args)
                print("─" * 40)
                print("✅ Completado\n")
            else:
                print("  ⚠️ Opción inválida. Inténtalo de nuevo.")
        except ValueError:
            print("  ⚠️ Por favor, ingresa un número válido.")


if __name__ == "__main__":
    main()

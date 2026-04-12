import os
import rarfile


def run(args=None):
    def descomprimir_rar():
        if args and len(args) > 0:
            path = args[0]
        else:
            path = input("Ingresa el path donde buscar los archivos .rar: ").strip()

        if not os.path.exists(path):
            print("El path ingresado no existe. Inténtalo de nuevo.")
            return

        rar_files = [f for f in os.listdir(path) if f.endswith(".rar")]

        if not rar_files:
            print("No se encontraron archivos .rar en el directorio proporcionado.")
            return

        for rar_file in rar_files:
            rar_path = os.path.join(path, rar_file)
            output_dir = os.path.join(path, rar_file.replace(".rar", ""))

            try:
                with rarfile.RarFile(rar_path) as rf:
                    print(f"Descomprimiendo '{rar_file}' en '{output_dir}'...")
                    rf.extractall(output_dir)
                    print(f"Archivo '{rar_file}' descomprimido con éxito.")
            except rarfile.Error as e:
                print(f"Error al descomprimir '{rar_file}': {e}")

    descomprimir_rar()

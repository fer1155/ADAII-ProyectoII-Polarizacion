def txt_to_dzn(input_txt, output_dzn):
    """
    Convierte un archivo .txt con el formato del proyecto MinPol
    a un archivo .dzn para MiniZinc
    
    Formato esperado del archivo .txt:
    - Linea 1: n (numero de personas)
    - Linea 2: m (numero de opiniones)
    - Linea 3: lista de m valores separados por comas (distribucion p_i)
    - Linea 4: lista de m valores separados por comas (valores v_i)
    - Lineas 5 a 4+m: 3 valores por linea (resistencias: baja, media, alta)
    - Linea 5+m: ct (costo total maximo)
    - Linea 6+m: maxMovs (movimientos maximos)
    
    Parametros:
        input_txt: ruta del archivo .txt de entrada
        output_dzn: ruta del archivo .dzn de salida
    
    Retorna:
        True si la conversion fue exitosa, False en caso contrario
    """
    
    try:
        # Leer todas las lineas del archivo de entrada y eliminar espacios
        with open(input_txt, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        
        # Parsear los datos de las primeras lineas
        n = int(lines[0])  # Numero total de personas
        m = int(lines[1])  # Numero de opiniones posibles
        
        # Distribucion de personas por cada opinion (vector p)
        # Separar por comas y convertir cada elemento a entero
        p = [int(x.strip()) for x in lines[2].split(',')]
        
        # Valores asociados a cada opinion (vector v)
        # Separar por comas y convertir cada elemento a flotante
        v = [float(x.strip()) for x in lines[3].split(',')]
        
        # Matriz de resistencias (m filas x 3 columnas)
        # Cada fila representa una opinion
        # Cada columna representa un nivel de resistencia (baja, media, alta)
        resistencias = []
        for i in range(4, 4 + m):
            fila = [int(x.strip()) for x in lines[i].split(',')]
            resistencias.append(fila)
        
        # Costo total maximo permitido
        ct = float(lines[4 + m])
        
        # Numero maximo de movimientos permitidos
        maxMovs = int(lines[5 + m])
        
        # Generar el archivo .dzn con formato MiniZinc
        with open(output_dzn, 'w') as f:
            # Escribir cada parametro en formato MiniZinc
            f.write(f"n = {n};\n")
            f.write(f"m = {m};\n")
            f.write(f"p = {p};\n")
            f.write(f"v = {v};\n")
            
            # Convertir matriz de resistencias a formato array2d de MiniZinc
            # array2d(1..m, 1..3, [valores...])
            # Aplanar la matriz (convertir de 2D a 1D) para el formato requerido
            flat_resistencias = [val for fila in resistencias for val in fila]
            f.write(f"s = array2d(1..{m}, 1..3, {flat_resistencias});\n")
            
            f.write(f"ct = {ct};\n")
            f.write(f"maxMovs = {maxMovs};\n")
        
        # Imprimir confirmacion y resumen de los datos convertidos
        print(f"Conversion exitosa: {output_dzn} creado")
        print(f"\nDatos convertidos:")
        print(f"  n (personas): {n}")
        print(f"  m (opiniones): {m}")
        print(f"  p (distribucion): {p}")
        print(f"  v (valores opiniones): {v}")
        print(f"  s (resistencias):")
        for i, fila in enumerate(resistencias, 1):
            print(f"    Opinion {i}: baja={fila[0]}, media={fila[1]}, alta={fila[2]}")
        print(f"  ct (costo maximo): {ct}")
        print(f"  maxMovs (movimientos maximos): {maxMovs}")
        
        return True
        
    except FileNotFoundError:
        # Error cuando no se encuentra el archivo de entrada
        print(f"Error: No se encontro el archivo '{input_txt}'")
        return False
    except IndexError:
        # Error cuando el archivo no tiene suficientes lineas
        print("Error: El archivo no tiene el formato correcto")
        return False
    except ValueError as e:
        # Error cuando los datos no se pueden convertir al tipo esperado
        print(f"Error al parsear los datos: {e}")
        return False
    except Exception as e:
        # Cualquier otro error no anticipado
        print(f"Error inesperado: {e}")
        return False


def ejemplo_uso():
    """
    Funcion de ejemplo que demuestra el uso del conversor
    Crea un archivo de entrada de ejemplo y lo convierte a formato .dzn
    """
    
    # Contenido de ejemplo con datos del proyecto MinPol
    # 10 personas, 3 opiniones, etc.
    contenido_ejemplo = """10
3
3,3,4
0.297,0.673,0.809
1,2,0
0,3,0
2,1,1
25
5"""
    
    # Crear archivo de entrada de ejemplo
    print("Creando archivo de ejemplo...")
    with open('entrada_ejemplo.txt', 'w') as f:
        f.write(contenido_ejemplo)
    
    print("\n" + "="*50)
    print("Convirtiendo entrada_ejemplo.txt a DatosProyecto.dzn")
    print("="*50 + "\n")
    
    # Ejecutar la conversion
    txt_to_dzn('entrada_ejemplo.txt', 'DatosProyecto.dzn')
    
    # Mostrar el contenido del archivo generado
    print("\n" + "="*50)
    print("Contenido del archivo .dzn generado:")
    print("="*50)
    
    with open('DatosProyecto.dzn', 'r') as f:
        print(f.read())


# Bloque principal que se ejecuta cuando se corre el script directamente
if __name__ == "__main__":
    import sys
    
    # Verificar el numero de argumentos de linea de comandos
    if len(sys.argv) == 3:
        # Uso con dos argumentos: python parser.py input.txt output.dzn
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        txt_to_dzn(input_file, output_file)
    elif len(sys.argv) == 2:
        # Uso con un argumento: python parser.py input.txt
        # (salida por defecto: DatosProyecto.dzn)
        input_file = sys.argv[1]
        txt_to_dzn(input_file, 'DatosProyecto.dzn')
    else:
        # Sin argumentos: mostrar ayuda y ejecutar ejemplo
        print("Uso:")
        print("  python parser.py input.txt output.dzn")
        print("  python parser.py input.txt")
        print("\nEjecutando ejemplo de demostracion...\n")
        ejemplo_uso()
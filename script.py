def txt_to_dzn(input_txt, output_dzn):
    """
    Convierte un archivo .txt con el formato del proyecto MinPol
    a un archivo .dzn para MiniZinc
    
    Formato del .txt:
    - Línea 1: n (número de personas)
    - Línea 2: m (número de opiniones)
    - Línea 3: lista de m valores separados por comas (distribución p_i)
    - Línea 4: lista de m valores separados por comas (valores v_i)
    - Líneas 5 a 4+m: 3 valores por línea (resistencias: baja, media, alta)
    - Línea 5+m: ct (costo total máximo)
    - Línea 6+m: maxMovs (movimientos máximos)
    """
    
    try:
        # Leer el archivo de entrada
        with open(input_txt, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
        
        # Parsear los datos
        n = int(lines[0])
        m = int(lines[1])
        
        # Distribución de personas por opinión
        p = [int(x.strip()) for x in lines[2].split(',')]
        
        # Valores de las opiniones
        v = [float(x.strip()) for x in lines[3].split(',')]
        
        # Matriz de resistencias (m filas x 3 columnas)
        resistencias = []
        for i in range(4, 4 + m):
            fila = [int(x.strip()) for x in lines[i].split(',')]
            resistencias.append(fila)
        
        # Costo total máximo
        ct = float(lines[4 + m])
        
        # Movimientos máximos
        maxMovs = int(lines[5 + m])
        
        # Generar archivo .dzn
        with open(output_dzn, 'w') as f:
            f.write(f"n = {n};\n")
            f.write(f"m = {m};\n")
            f.write(f"p = {p};\n")
            f.write(f"v = {v};\n")
            
            # Convertir matriz de resistencias a formato MiniZinc array2d
            # array2d(1..m, 1..3, [valores...])
            flat_resistencias = [val for fila in resistencias for val in fila]
            f.write(f"s = array2d(1..{m}, 1..3, {flat_resistencias});\n")
            
            f.write(f"ct = {ct};\n")
            f.write(f"maxMovs = {maxMovs};\n")
        
        print(f"✓ Conversión exitosa: {output_dzn} creado")
        print(f"\nDatos convertidos:")
        print(f"  n (personas): {n}")
        print(f"  m (opiniones): {m}")
        print(f"  p (distribución): {p}")
        print(f"  v (valores opiniones): {v}")
        print(f"  s (resistencias):")
        for i, fila in enumerate(resistencias, 1):
            print(f"    Opinión {i}: baja={fila[0]}, media={fila[1]}, alta={fila[2]}")
        print(f"  ct (costo máximo): {ct}")
        print(f"  maxMovs (movimientos máximos): {maxMovs}")
        
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: No se encontró el archivo '{input_txt}'")
        return False
    except IndexError:
        print("✗ Error: El archivo no tiene el formato correcto")
        return False
    except ValueError as e:
        print(f"✗ Error al parsear los datos: {e}")
        return False
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False


def ejemplo_uso():
    """Ejemplo de uso del conversor"""
    
    # Crear archivo de ejemplo
    contenido_ejemplo = """10
3
3,3,4
0.297,0.673,0.809
1,2,0
0,3,0
2,1,1
25
5"""
    
    print("Creando archivo de ejemplo...")
    with open('entrada_ejemplo.txt', 'w') as f:
        f.write(contenido_ejemplo)
    
    print("\n" + "="*50)
    print("Convirtiendo entrada_ejemplo.txt a DatosProyecto.dzn")
    print("="*50 + "\n")
    
    # Convertir
    txt_to_dzn('entrada_ejemplo.txt', 'DatosProyecto.dzn')
    
    print("\n" + "="*50)
    print("Contenido del archivo .dzn generado:")
    print("="*50)
    
    with open('DatosProyecto.dzn', 'r') as f:
        print(f.read())


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        # Uso: python script.py input.txt output.dzn
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        txt_to_dzn(input_file, output_file)
    elif len(sys.argv) == 2:
        # Uso: python script.py input.txt (salida por defecto: DatosProyecto.dzn)
        input_file = sys.argv[1]
        txt_to_dzn(input_file, 'DatosProyecto.dzn')
    else:
        # Ejecutar ejemplo
        print("Uso:")
        print("  python script.py input.txt output.dzn")
        print("  python script.py input.txt")
        print("\nEjecutando ejemplo de demostración...\n")
        ejemplo_uso()
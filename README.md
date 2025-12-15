# MinPol - Minimización de Polarización

Sistema de optimización diseñado para minimizar la polarización en grupos mediante la redistribución estratégica de opiniones, implementado con MiniZinc y una interfaz gráfica en Python.

---

## 📁 Estructura del Proyecto

```
MinPol/
├── README.md                      # Este archivo
├── .gitignore                     # Archivos excluidos del control de versiones
├── Proyecto.mzn                   # Modelo de optimización MiniZinc
├── DatosProyecto.dzn              # Archivo de datos generado (formato MiniZinc)
│
├── DatosDelProyecto/              # Instancias de ejemplo del profesor
│   ├── Prueba1.txt
│   ├── Prueba2.txt
│   └── ...
│
├── MisInstancias/                 # Instancias personalizadas
│   ├── Instancia1.txt
│   ├── Instancia2.txt
│   └── ...
│
└── ProyectoGUIFuentes/            # Código fuente de la interfaz gráfica
    ├── main.py                    # Aplicación principal con GUI
    ├── parser.py                  # Conversor TXT → DZN
    └── requirements.txt           # Dependencias Python
```

---

## 📋 Descripción de Archivos

### Archivos Principales

#### `Proyecto.mzn`
Modelo de optimización en MiniZinc que resuelve el problema de minimización de polarización. Define las variables de decisión, restricciones y función objetivo.

#### `DatosProyecto.dzn`
Archivo de datos en formato MiniZinc generado automáticamente. Contiene los parámetros del problema:
- `n`: Número total de personas
- `m`: Número de opiniones posibles
- `p`: Vector de distribución inicial de personas por opinión
- `v`: Vector de valores asociados a cada opinión
- `s`: Matriz de resistencias (m × 3: baja, media, alta)
- `ct`: Costo total máximo permitido
- `maxMovs`: Número máximo de movimientos permitidos

### Carpetas de Instancias

#### `DatosDelProyecto/`
Contiene archivos `.txt` con instancias de prueba proporcionadas por el profesor. Formato de cada archivo:
```
10                    # n (personas)
3                     # m (opiniones)
3,3,4                 # p (distribución inicial)
0.297,0.673,0.809     # v (valores de opiniones)
1,2,0                 # s[1] (resistencias opinión 1)
0,3,0                 # s[2] (resistencias opinión 2)
2,1,1                 # s[3] (resistencias opinión 3)
25                    # ct (costo máximo)
5                     # maxMovs (movimientos máximos)
```

#### `MisInstancias/`
Carpeta para almacenar instancias personalizadas con el mismo formato que las de prueba.

### Código Fuente (`ProyectoGUIFuentes/`)

#### `main.py`
Interfaz gráfica principal construida con Tkinter. Funcionalidades:
- **Gestión de archivos**: Seleccionar y convertir archivos `.txt` a formato `.dzn`
- **Entrada manual de datos**: Formularios para ingresar parámetros y matriz de resistencias
- **Ejecución del modelo**: Lanzar el optimizador MiniZinc directamente desde la GUI
- **Consola de salida**: Visualizar resultados y mensajes del sistema

#### `parser.py`
Módulo de conversión que transforma archivos `.txt` en formato `.dzn` compatible con MiniZinc. Puede usarse:
- Como módulo importado por `main.py`
- Como script independiente desde línea de comandos
- Con función de demostración incorporada

#### `requirements.txt`
Lista de dependencias Python necesarias:
```
minizinc>=0.7.0
```

---

## 🚀 Instrucciones de Instalación

### 1. Prerrequisitos

#### Instalar MiniZinc
Descargue e instale MiniZinc desde: https://www.minizinc.org/

**Verificar instalación:**
```bash
minizinc --version
```

#### Instalar Python
Python 3.7 o superior. Verificar con:
```bash
python --version
```

### 2. Configurar el Proyecto

#### Clonar o descargar el proyecto
```bash
git clone <url-del-repositorio>
cd MinPol
```

#### Instalar dependencias Python
```bash
cd ProyectoGUIFuentes
pip install -r requirements.txt
```

---

## 🎯 Uso de la Aplicación

### Opción 1: Interfaz Gráfica (Recomendado)

1. **Ejecutar la aplicación:**
   ```bash
   cd ProyectoGUIFuentes
   python main.py
   ```

2. **Flujo de trabajo en la GUI:**

   **Método A - Desde archivo existente:**
   - Click en "Seleccionar .txt" → Elegir archivo de instancia
   - Click en "Convertir a .dzn" → Genera `DatosProyecto.dzn`
   - Click en "Ejecutar Modelo" → Ver resultados en consola

   **Método B - Entrada manual:**
   - Completar los campos de "Parámetros del Sistema"
   - Ingresar el valor de `m` para generar la matriz de resistencias
   - Llenar la matriz de resistencias generada dinámicamente
   - Click en "Generar datos desde GUI" → Crea `DatosProyecto.dzn`
   - Click en "Ejecutar Modelo" → Ver resultados en consola

### Opción 2: Línea de Comandos

#### Convertir archivo TXT a DZN
```bash
cd ProyectoGUIFuentes
python parser.py ../MisInstancias/Instancia1.txt ../DatosProyecto.dzn
```

#### Ejecutar el modelo MiniZinc
```bash
cd ..
minizinc Proyecto.mzn DatosProyecto.dzn
```

#### Ejecutar ejemplo de demostración
```bash
cd ProyectoGUIFuentes
python parser.py
```
Esto genera archivos de ejemplo y muestra el proceso de conversión.

---

## 📊 Ejemplo de Uso Completo

### Crear una instancia personalizada

**Archivo:** `MisInstancias/MiPrueba.txt`
```
15
4
4,5,3,3
0.2,0.4,0.7,0.9
1,3,2
2,1,4
0,2,3
3,1,0
30
7
```

### Procesar con la GUI
1. Ejecutar `python main.py`
2. Seleccionar `MiPrueba.txt`
3. Convertir a DZN
4. Ejecutar modelo
5. Analizar resultados en la consola de salida

### Procesar por línea de comandos
```bash
cd ProyectoGUIFuentes
python parser.py ../MisInstancias/MiPrueba.txt ../DatosProyecto.dzn
cd ..
minizinc Proyecto.mzn DatosProyecto.dzn
```

---

## 🛠️ Solución de Problemas

### Error: "MiniZinc no está instalado"
- Verificar que MiniZinc esté en el PATH del sistema
- Reinstalar MiniZinc y asegurar que se agregue al PATH durante la instalación

### Error: "Formato incorrecto del archivo"
- Verificar que el archivo `.txt` tenga exactamente `6 + m` líneas
- Revisar que no haya líneas vacías o espacios adicionales
- Confirmar que los valores estén separados por comas

### Error: "Módulo 'tkinter' no encontrado"
En Linux, instalar:
```bash
sudo apt-get install python3-tk
```

### Tiempo de ejecución excedido
- El modelo tiene un timeout de 60 segundos
- Para instancias grandes, considerar reducir `n`, `m` o `maxMovs`
- Modificar el timeout en `main.py` línea del `subprocess.run()`

---

## 📝 Notas Adicionales

- Los archivos `.dzn` se sobrescriben automáticamente al generar nuevos datos
- La matriz de resistencias siempre tiene 3 columnas (baja, media, alta)
- Los valores de `v` deben ser flotantes en el rango [0, 1]
- La suma de los valores en `p` debe ser igual a `n`

---

## 👥 Contribuir

Para agregar nuevas instancias, crear archivos `.txt` en `MisInstancias/` siguiendo el formato especificado.

---

## 📄 Licencia

Este proyecto es parte de un trabajo académico. Consultar con los autores para términos de uso.

---

## 📧 Contacto

Para preguntas o reportar problemas, contactar al equipo de desarrollo del proyecto.

---

**Versión:** 1.0  
**Última actualización:** Diciembre 2025
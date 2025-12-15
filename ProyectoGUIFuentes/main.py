import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import subprocess
import os
from parser import txt_to_dzn

# RUTAS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_TXT = os.path.join(BASE_DIR, "..", "Mis Instancias")
RUTA_DZN = os.path.join(BASE_DIR, "..", "DatosProyecto.dzn")
RUTA_MZN = os.path.join(BASE_DIR, "..", "Proyecto.mzn")

# COLORES Y ESTILOS
COLORES = {
    'primary': '#2196F3',
    'primary_dark': '#1976D2',
    'secondary': '#4CAF50',
    'secondary_dark': '#388E3C',
    'accent': '#FF5722',
    'bg_dark': '#263238',
    'bg_light': '#ECEFF1',
    'text_dark': '#212121',
    'text_light': '#FFFFFF',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'border': '#B0BEC5'
}

# GUI
class MinPolGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("MinPol - Optimizacion")
        self.root.geometry("1000x750")
        self.root.configure(bg=COLORES['bg_light'])

        # Variable para almacenar la ruta del archivo seleccionado
        self.archivo_txt = None
        # Lista para almacenar los campos de entrada de resistencias
        self.res_entries = []

        # Configurar estilos visuales de los componentes
        self.configurar_estilos()

        # Crear el encabezado principal
        self.crear_header()

        # Crear el panel principal que contendra todas las secciones
        main_panel = tk.Frame(root, bg=COLORES['bg_light'])
        main_panel.pack(fill='both', expand=True, padx=20, pady=10)

        # Crear la seccion de gestion de archivos
        self.crear_seccion_archivo(main_panel)

        # Crear contenedor para los parametros y resistencias
        params_container = tk.Frame(main_panel, bg=COLORES['bg_light'])
        params_container.pack(fill='both', expand=True, pady=10)

        # Crear seccion de parametros del sistema
        self.crear_seccion_parametros(params_container)
        # Crear seccion de matriz de resistencias
        self.crear_seccion_resistencias(params_container)

        # Crear boton para generar el archivo dzn desde la GUI
        self.crear_boton_generar(main_panel)

        # Crear seccion de consola de salida
        self.crear_seccion_salida(main_panel)

        # Mensaje inicial en la consola
        self.log("Sistema iniciado correctamente. Listo para optimizar politicas.")

    # --------------------------------------------------
    def configurar_estilos(self):
        """Configura los estilos visuales de los componentes ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones primarios
        style.configure('Primary.TButton',
                       background=COLORES['primary'],
                       foreground=COLORES['text_light'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=10)
        style.map('Primary.TButton',
                 background=[('active', COLORES['primary_dark'])])

        # Estilo para botones secundarios
        style.configure('Secondary.TButton',
                       background=COLORES['secondary'],
                       foreground=COLORES['text_light'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=10)
        style.map('Secondary.TButton',
                 background=[('active', COLORES['secondary_dark'])])

    # --------------------------------------------------
    def crear_header(self):
        """Crea el encabezado principal de la aplicacion"""
        header = tk.Frame(self.root, bg=COLORES['primary'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        titulo = tk.Label(header,
                         text="MinPol - Minimizar la Polarizacion",
                         font=('Segoe UI', 24, 'bold'),
                         bg=COLORES['primary'],
                         fg=COLORES['text_light'])
        titulo.pack(pady=20)

    # --------------------------------------------------
    def crear_seccion_archivo(self, parent):
        """Crea la seccion de gestion de archivos con botones de accion"""
        frame = tk.LabelFrame(parent,
                             text="  Gestion de Archivos  ",
                             font=('Segoe UI', 11, 'bold'),
                             bg='white',
                             fg=COLORES['text_dark'],
                             relief='flat',
                             borderwidth=2)
        frame.pack(fill='x', pady=(0, 10))

        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(pady=15, padx=15)

        # Boton para seleccionar archivo txt
        btn_select = tk.Button(btn_frame,
                              text="Seleccionar .txt",
                              command=self.seleccionar_txt,
                              bg=COLORES['primary'],
                              fg=COLORES['text_light'],
                              font=('Segoe UI', 10, 'bold'),
                              relief='flat',
                              padx=20,
                              pady=10,
                              cursor='hand2')
        btn_select.grid(row=0, column=0, padx=5)
        # Efecto hover para cambiar color al pasar el mouse
        btn_select.bind('<Enter>', lambda e: e.widget.config(bg=COLORES['primary_dark']))
        btn_select.bind('<Leave>', lambda e: e.widget.config(bg=COLORES['primary']))

        # Boton para convertir txt a dzn
        btn_convert = tk.Button(btn_frame,
                               text="Convertir a .dzn",
                               command=self.convertir_txt,
                               bg=COLORES['secondary'],
                               fg=COLORES['text_light'],
                               font=('Segoe UI', 10, 'bold'),
                               relief='flat',
                               padx=20,
                               pady=10,
                               cursor='hand2')
        btn_convert.grid(row=0, column=1, padx=5)
        btn_convert.bind('<Enter>', lambda e: e.widget.config(bg=COLORES['secondary_dark']))
        btn_convert.bind('<Leave>', lambda e: e.widget.config(bg=COLORES['secondary']))

        # Boton para ejecutar el modelo MiniZinc
        btn_execute = tk.Button(btn_frame,
                               text="Ejecutar Modelo",
                               command=self.ejecutar_modelo,
                               bg=COLORES['accent'],
                               fg=COLORES['text_light'],
                               font=('Segoe UI', 10, 'bold'),
                               relief='flat',
                               padx=20,
                               pady=10,
                               cursor='hand2')
        btn_execute.grid(row=0, column=2, padx=5)
        btn_execute.bind('<Enter>', lambda e: e.widget.config(bg='#E64A19'))
        btn_execute.bind('<Leave>', lambda e: e.widget.config(bg=COLORES['accent']))

    # --------------------------------------------------
    def crear_seccion_parametros(self, parent):
        """Crea la seccion de parametros del sistema"""
        self.frame_inputs = tk.LabelFrame(parent,
                                         text="  Parametros del Sistema  ",
                                         font=('Segoe UI', 11, 'bold'),
                                         bg='white',
                                         fg=COLORES['text_dark'],
                                         relief='flat',
                                         borderwidth=2)
        self.frame_inputs.pack(side='left', fill='both', expand=True, padx=(0, 5))

        inner = tk.Frame(self.frame_inputs, bg='white')
        inner.pack(padx=15, pady=15, fill='both', expand=True)

        # Crear campos de entrada para cada parametro
        self.entry_n = self._campo_mejorado(inner, "Personas (n)", 0, "Numero total de personas")
        self.entry_m = self._campo_mejorado(inner, "Opiniones (m)", 1, "Numero de opiniones posibles")
        self.entry_p = self._campo_mejorado(inner, "Vector p", 2, "Ejemplo: 1,8,1")
        self.entry_v = self._campo_mejorado(inner, "Vector v", 3, "Ejemplo: 0.3,0.5,0.9")
        self.entry_ct = self._campo_mejorado(inner, "Costo (ct)", 4, "Costo total permitido")
        self.entry_maxMovs = self._campo_mejorado(inner, "Max Movimientos", 5, "Movimientos maximos")

        # Detectar cambios en el campo m para actualizar matriz de resistencias
        self.entry_m.bind("<KeyRelease>", lambda e: self.crear_resistencias())

    # --------------------------------------------------
    def _campo_mejorado(self, parent, texto, fila, placeholder):
        """Crea un campo de entrada mejorado con etiqueta y placeholder"""
        frame = tk.Frame(parent, bg='white')
        frame.grid(row=fila, column=0, sticky='ew', pady=5)
        parent.grid_columnconfigure(0, weight=1)

        # Etiqueta del campo
        label = tk.Label(frame,
                        text=texto,
                        font=('Segoe UI', 10),
                        bg='white',
                        fg=COLORES['text_dark'],
                        anchor='w')
        label.pack(side='left', padx=(0, 10))

        # Campo de entrada
        entry = tk.Entry(frame,
                        font=('Segoe UI', 10),
                        relief='solid',
                        borderwidth=1,
                        width=25)
        entry.pack(side='right', fill='x', expand=True)
        
        # Insertar placeholder inicial
        entry.insert(0, placeholder)
        entry.config(fg='gray')
        
        # Funciones para manejar el placeholder
        def on_focus_in(e):
            # Limpiar placeholder al enfocar
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=COLORES['text_dark'])
        
        def on_focus_out(e):
            # Restaurar placeholder si esta vacio
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg='gray')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

        return entry

    # --------------------------------------------------
    def crear_seccion_resistencias(self, parent):
        """Crea la seccion de matriz de resistencias"""
        self.frame_res = tk.LabelFrame(parent,
                                      text="  Matriz de Resistencias  ",
                                      font=('Segoe UI', 11, 'bold'),
                                      bg='white',
                                      fg=COLORES['text_dark'],
                                      relief='flat',
                                      borderwidth=2)
        self.frame_res.pack(side='left', fill='both', expand=True, padx=(5, 0))

        # Texto informativo inicial
        info = tk.Label(self.frame_res,
                       text="Ingrese 'm' y las resistencias se generaran automaticamente",
                       font=('Segoe UI', 9, 'italic'),
                       bg='white',
                       fg='gray')
        info.pack(pady=10)

    # --------------------------------------------------
    def crear_resistencias(self):
        """Genera dinamicamente la matriz de resistencias segun el valor de m"""
        # Limpiar widgets existentes
        for w in self.frame_res.winfo_children():
            w.destroy()

        # Limpiar lista de entradas
        self.res_entries.clear()

        try:
            # Obtener y validar el valor de m
            m_value = self.entry_m.get()
            if m_value == "Numero de opiniones posibles" or not m_value:
                return
            m = int(m_value)
            if m <= 0 or m > 20:
                return
        except ValueError:
            return

        # Crear canvas con scroll para la matriz
        canvas = tk.Canvas(self.frame_res, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame_res, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg='white')

        # Configurar el scroll
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Crear encabezados de la matriz
        tk.Label(scrollable, text="", bg='white', width=8).grid(row=0, column=0)
        for idx, nivel in enumerate(['Baja', 'Media', 'Alta'], 1):
            tk.Label(scrollable,
                    text=nivel,
                    font=('Segoe UI', 9, 'bold'),
                    bg=COLORES['bg_light'],
                    fg=COLORES['text_dark'],
                    relief='flat',
                    padx=10,
                    pady=5).grid(row=0, column=idx, padx=2, pady=5)

        # Crear filas de resistencias para cada opinion
        for i in range(m):
            # Etiqueta de la opinion
            tk.Label(scrollable,
                    text=f"Op {i+1}",
                    font=('Segoe UI', 9, 'bold'),
                    bg='white',
                    fg=COLORES['text_dark']).grid(row=i+1, column=0, pady=2)
            
            # Crear tres campos de entrada (baja, media, alta)
            fila = []
            for j in range(3):
                e = tk.Entry(scrollable,
                           width=8,
                           font=('Segoe UI', 9),
                           relief='solid',
                           borderwidth=1,
                           justify='center')
                e.grid(row=i+1, column=j+1, padx=2, pady=2)
                e.insert(0, "0")
                fila.append(e)
            self.res_entries.append(fila)

        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

    # --------------------------------------------------
    def crear_boton_generar(self, parent):
        """Crea el boton principal para generar el archivo dzn"""
        btn_generar = tk.Button(parent,
                               text="Generar datos desde GUI",
                               command=self.generar_desde_gui,
                               bg=COLORES['secondary'],
                               fg=COLORES['text_light'],
                               font=('Segoe UI', 11, 'bold'),
                               relief='flat',
                               padx=30,
                               pady=5,
                               cursor='hand2')
        btn_generar.pack(pady=10)
        btn_generar.bind('<Enter>', lambda e: e.widget.config(bg=COLORES['secondary_dark']))
        btn_generar.bind('<Leave>', lambda e: e.widget.config(bg=COLORES['secondary']))

    # --------------------------------------------------
    def crear_seccion_salida(self, parent):
        """Crea la seccion de consola de salida"""
        frame = tk.LabelFrame(parent,
                             text="  Consola de Salida  ",
                             font=('Segoe UI', 11, 'bold'),
                             bg='white',
                             fg=COLORES['text_dark'],
                             relief='flat',
                             borderwidth=2)
        frame.pack(fill='both', expand=True)

        # Area de texto con scroll para mostrar mensajes
        self.salida = scrolledtext.ScrolledText(frame,
                                               width=110,
                                               height=20,
                                               font=('Consolas', 10),
                                               bg='#1E1E1E',
                                               fg='#D4D4D4',
                                               relief='flat',
                                               padx=10,
                                               pady=10)
        self.salida.pack(padx=10, pady=10, fill='both', expand=True)

    # --------------------------------------------------
    def log(self, texto):
        """Agrega un mensaje a la consola de salida"""
        self.salida.insert(tk.END, texto + "\n")
        self.salida.see(tk.END)

    # --------------------------------------------------
    def seleccionar_txt(self):
        """Abre dialogo para seleccionar archivo txt"""
        self.archivo_txt = filedialog.askopenfilename(
            initialdir=RUTA_TXT,
            filetypes=[("Archivos TXT", "*.txt")],
            title="Seleccionar archivo de instancia"
        )
        if self.archivo_txt:
            nombre = os.path.basename(self.archivo_txt)
            self.log(f"Archivo seleccionado: {nombre}")

    # --------------------------------------------------
    def convertir_txt(self):
        """Convierte el archivo txt seleccionado a formato dzn"""
        if not self.archivo_txt:
            messagebox.showwarning("Advertencia", "Debe seleccionar un archivo .txt primero")
            return

        if txt_to_dzn(self.archivo_txt, RUTA_DZN):
            self.log("DatosProyecto.dzn actualizado exitosamente desde archivo .txt")
            messagebox.showinfo("Exito", "Conversion completada correctamente")
        else:
            self.log("Error al convertir el archivo")
            messagebox.showerror("Error", "No se pudo convertir el archivo")

    # --------------------------------------------------
    def generar_desde_gui(self):
        """Genera el archivo dzn a partir de los datos ingresados en la GUI"""
        try:
            # Funcion auxiliar para obtener valores limpiando placeholders
            def get_value(entry, placeholder):
                val = entry.get()
                return val if val != placeholder else ""

            # Obtener todos los valores de los campos
            n = get_value(self.entry_n, "Numero total de personas")
            m = get_value(self.entry_m, "Numero de opiniones posibles")
            p = get_value(self.entry_p, "Ejemplo: 1,8,1")
            v = get_value(self.entry_v, "Ejemplo: 0.3,0.5,0.9")
            ct = get_value(self.entry_ct, "Costo total permitido")
            maxMovs = get_value(self.entry_maxMovs, "Movimientos maximos")

            # Validar que todos los campos esten completos
            if not all([n, m, p, v, ct, maxMovs]):
                raise ValueError("Todos los campos son obligatorios")

            # Validar que el numero de resistencias coincida con m
            if len(self.res_entries) != int(m):
                raise ValueError("Numero incorrecto de filas de resistencias")

            # Construir el contenido del archivo temporal
            lineas = [n, m, p, v]

            # Agregar las filas de resistencias
            for fila in self.res_entries:
                lineas.append(",".join(e.get() for e in fila))

            lineas.append(ct)
            lineas.append(maxMovs)

            # Crear archivo temporal con los datos
            temp_txt = os.path.join(BASE_DIR, "entrada_gui_temp.txt")

            with open(temp_txt, "w") as f:
                f.write("\n".join(lineas))

            # Convertir el archivo temporal a dzn
            if txt_to_dzn(temp_txt, RUTA_DZN):
                self.log("DatosProyecto.dzn generado exitosamente desde la GUI")
                messagebox.showinfo("Exito", "Archivo generado correctamente")
            else:
                self.log("Error al generar desde la GUI")
                messagebox.showerror("Error", "No se pudo generar el archivo")

        except Exception as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
            self.log(f"Error: {str(e)}")

    # --------------------------------------------------
    def ejecutar_modelo(self):
        """Ejecuta el modelo MiniZinc con el archivo dzn generado"""
        # Validar que existe el archivo dzn
        if not os.path.exists(RUTA_DZN):
            messagebox.showwarning("Advertencia", "No existe DatosProyecto.dzn")
            return

        self.log("\n" + "="*60)
        self.log("Ejecutando modelo MiniZinc...")
        self.log("="*60 + "\n")

        try:
            # Ejecutar MiniZinc con timeout de 60 segundos
            resultado = subprocess.run(
                ["minizinc", RUTA_MZN, RUTA_DZN],
                capture_output=True,
                text=True,
                timeout=60
            )

            # Mostrar la salida estandar si existe
            if resultado.stdout:
                self.log("RESULTADO:")
                self.log("-" * 60)
                self.log(resultado.stdout)
                
            self.log("\n" + "="*60)
            self.log("Ejecucion completada")
            self.log("="*60 + "\n")

        except subprocess.TimeoutExpired:
            self.log("Tiempo de ejecucion excedido (60s)")
            messagebox.showerror("Error", "El modelo tardo demasiado en ejecutarse")
        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "MiniZinc no esta instalado o no se encuentra en el PATH del sistema.\n\n"
                "Por favor instale MiniZinc desde: https://www.minizinc.org/"
            )
            self.log("MiniZinc no encontrado en el sistema")

# MAIN
if __name__ == "__main__":
    root = tk.Tk()
    MinPolGUI(root)
    root.mainloop()
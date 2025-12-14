import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os

from parser import txt_to_dzn


# ======================================================
# RUTAS
# ======================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RUTA_TXT = os.path.join(BASE_DIR, "..", "Mis Instancias")
RUTA_DZN = os.path.join(BASE_DIR, "..", "DatosProyecto.dzn")
RUTA_MZN = os.path.join(BASE_DIR, "..", "Proyecto.mzn")


# ======================================================
# GUI
# ======================================================

class MinPolGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto MinPol - GUI")
        self.root.geometry("900x700")

        self.archivo_txt = None
        self.res_entries = []

        # ================= BOTONES SUPERIORES =================
        frame = tk.Frame(root)
        frame.pack(pady=5)

        tk.Button(frame, text="Seleccionar .txt",
                  command=self.seleccionar_txt, width=20).grid(row=0, column=0, padx=5)

        tk.Button(frame, text="Convertir .txt → .dzn",
                  command=self.convertir_txt, width=20).grid(row=0, column=1, padx=5)

        tk.Button(frame, text="Ejecutar modelo",
                  command=self.ejecutar_modelo, width=20).grid(row=0, column=2, padx=5)

        # ================= ENTRADAS MANUALES + RESISTENCIAS =================
        contenedor = tk.Frame(root)
        contenedor.pack(padx=10, pady=10, fill="x")

        self.frame_inputs = tk.LabelFrame(contenedor, text="Parámetros")
        self.frame_inputs.pack(side="left", padx=10, fill="y")

        self.frame_res = tk.LabelFrame(contenedor, text="Resistencias (baja / media / alta)")
        self.frame_res.pack(side="left", padx=10)

        self.entry_n = self._campo("n (personas)", 0)
        self.entry_m = self._campo("m (opiniones)", 1)
        self.entry_p = self._campo("p (ej: 1,8,1)", 2)
        self.entry_v = self._campo("v (ej: 0.3,0.5,0.9)", 3)
        self.entry_ct = self._campo("ct", 4)
        self.entry_maxMovs = self._campo("maxMovs", 5)

        # Detectar cambio en m automáticamente
        self.entry_m.bind("<KeyRelease>", lambda e: self.crear_resistencias())

        tk.Button(
            root,
            text="Generar DatosProyecto.dzn desde la GUI",
            command=self.generar_desde_gui,
            width=40,
            bg="#4CAF50",
            fg="white"
        ).pack(pady=5)

        # ================= SALIDA =================
        self.salida = scrolledtext.ScrolledText(root, width=110, height=20)
        self.salida.pack(padx=10, pady=10)

        self.log("GUI iniciada correctamente.")

    # --------------------------------------------------
    def _campo(self, texto, fila):
        tk.Label(self.frame_inputs, text=texto).grid(row=fila, column=0, sticky="w")
        e = tk.Entry(self.frame_inputs, width=25)
        e.grid(row=fila, column=1, padx=5, pady=2)
        return e

    # --------------------------------------------------
    def log(self, texto):
        self.salida.insert(tk.END, texto + "\n")
        self.salida.see(tk.END)

    # --------------------------------------------------
    def seleccionar_txt(self):
        self.archivo_txt = filedialog.askopenfilename(
            initialdir=RUTA_TXT,
            filetypes=[("Archivos TXT", "*.txt")]
        )
        if self.archivo_txt:
            self.log(f"Archivo seleccionado: {self.archivo_txt}")

    # --------------------------------------------------
    def convertir_txt(self):
        if not self.archivo_txt:
            messagebox.showwarning("Error", "Seleccione un archivo .txt")
            return

        if txt_to_dzn(self.archivo_txt, RUTA_DZN):
            self.log("✓ DatosProyecto.dzn actualizado desde archivo .txt")
        else:
            self.log("✗ Error al convertir el archivo")

    # --------------------------------------------------
    def crear_resistencias(self):
        for w in self.frame_res.winfo_children():
            w.destroy()

        self.res_entries.clear()

        try:
            m = int(self.entry_m.get())
            if m <= 0:
                return
        except ValueError:
            return

        tk.Label(self.frame_res, text="").grid(row=0, column=0)
        tk.Label(self.frame_res, text="Baja").grid(row=0, column=1)
        tk.Label(self.frame_res, text="Media").grid(row=0, column=2)
        tk.Label(self.frame_res, text="Alta").grid(row=0, column=3)

        for i in range(m):
            tk.Label(self.frame_res, text=f"Op {i+1}").grid(row=i+1, column=0)
            fila = []
            for j in range(3):
                e = tk.Entry(self.frame_res, width=5)
                e.grid(row=i+1, column=j+1, padx=2)
                e.insert(0, "0")  # valor por defecto
                fila.append(e)
            self.res_entries.append(fila)

    # --------------------------------------------------
    def generar_desde_gui(self):
        try:
            n = self.entry_n.get()
            m = self.entry_m.get()
            p = self.entry_p.get()
            v = self.entry_v.get()
            ct = self.entry_ct.get()
            maxMovs = self.entry_maxMovs.get()

            if len(self.res_entries) != int(m):
                raise ValueError("Número incorrecto de filas de resistencias")

            lineas = [n, m, p, v]

            for fila in self.res_entries:
                lineas.append(",".join(e.get() for e in fila))

            lineas.append(ct)
            lineas.append(maxMovs)

            temp_txt = os.path.join(BASE_DIR, "entrada_gui_temp.txt")

            with open(temp_txt, "w") as f:
                f.write("\n".join(lineas))

            if txt_to_dzn(temp_txt, RUTA_DZN):
                self.log("✓ DatosProyecto.dzn generado desde la GUI")
            else:
                self.log("✗ Error al generar desde la GUI")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------------------
    def ejecutar_modelo(self):
        if not os.path.exists(RUTA_DZN):
            messagebox.showwarning("Error", "No existe DatosProyecto.dzn")
            return

        self.log("\nEjecutando MiniZinc...\n")

        try:
            resultado = subprocess.run(
                ["minizinc", RUTA_MZN, RUTA_DZN],
                capture_output=True,
                text=True
            )

            if resultado.stdout:
                self.log("=== RESULTADO ===")
                self.log(resultado.stdout)

            if resultado.stderr:
                self.log("=== ERRORES ===")
                self.log(resultado.stderr)

        except FileNotFoundError:
            messagebox.showerror(
                "Error",
                "MiniZinc no está en el PATH."
            )


# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":
    root = tk.Tk()
    MinPolGUI(root)
    root.mainloop()

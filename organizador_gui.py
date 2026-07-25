import hashlib
import os
import shutil
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ==========================================
# CONFIGURACIÓN Y REGLAS
# ==========================================
CATEGORIAS = {
    "Documentos": [
        ".pdf",
        ".docx",
        ".doc",
        ".xlsx",
        ".xls",
        ".pptx",
        ".ppt",
        ".txt",
        ".csv",
    ],
    "Imagenes": [".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".bmp"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso"],
}

EXTENSIONES_SISTEMA = {
    ".dll",
    ".exe",
    ".sys",
    ".lnk",
    ".ini",
    ".tmp",
    ".dat",
    ".sqlite",
    ".json",
    ".lz4",
    ".bin",
    ".toc",
    ".pyz",
    ".pkg",
}

class AppOrganizadorV3:

    def __init__(self, root):
        self.root = root
        self.root.title("ResQ-File — Smart Organizer Edition")
        self.root.geometry("700x750")

        self.archivos_fallidos = []
        
        # Variables de Organizador
        self.ruta_destino = Path.home() / "Desktop" / "ORGANIZADO"
        
        # Variables de Migración (Puente)
        self.ruta_migracion = Path.home() / "Desktop"

        self.rutas_origen = [
            Path.home() / "Desktop",
            Path.home() / "Downloads",
            Path.home() / "Documents",
            Path.home() / "Music",
            Path.home() / "Pictures",
            Path.home() / "Videos",
        ]

        self.crear_interfaz_principal()

    def crear_interfaz_principal(self):
        # Crear sistema de pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        # Pestaña 1: Organizador Inteligente (El original)
        self.tab_organizador = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_organizador, text="Organizador Inteligente")
        self.crear_interfaz_organizador(self.tab_organizador)

        # Pestaña 2: Migración de Windows (La nueva función)
        self.tab_migracion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_migracion, text="Migración de Windows (Puente)")
        self.crear_interfaz_migracion(self.tab_migracion)

    # ==========================================
    # PESTAÑA 1: ORGANIZADOR ORIGINAL
    # ==========================================
    def crear_interfaz_organizador(self, parent):
        # --- SECCIÓN: RUTAS ---
        frame_rutas = ttk.LabelFrame(parent, text=" 1. Rutas de Trabajo ", padding=10)
        frame_rutas.pack(fill="x", padx=15, pady=10)

        lbl_origen = ttk.Label(
            frame_rutas, text="Orígenes: Escritorio, Descargas, Documentos, Música, Imágenes, Videos"
        )
        lbl_origen.pack(anchor="w", pady=2)

        btn_dest = ttk.Button(
            frame_rutas,
            text="Cambiar Carpeta Destino Respaldo",
            command=self.seleccionar_destino,
        )
        btn_dest.pack(anchor="w", pady=5)

        self.lbl_destino_val = ttk.Label(
            frame_rutas,
            text=f"Destino: {self.ruta_destino}",
            foreground="blue",
            wraplength=550,
        )
        self.lbl_destino_val.pack(anchor="w")

        # --- SECCIÓN: CATEGORÍAS ---
        frame_cats = ttk.LabelFrame(parent, text=" 2. Categorías a Incluir ", padding=10)
        frame_cats.pack(fill="x", padx=15, pady=5)

        self.vars_cats = {}
        for cat in CATEGORIAS.keys():
            var = tk.BooleanVar(value=True)
            chk = ttk.Checkbutton(frame_cats, text=cat, variable=var)
            chk.pack(side="left", expand=True)
            self.vars_cats[cat] = var

        self.var_otros = tk.BooleanVar(value=False)
        chk_otros = ttk.Checkbutton(
            frame_cats, text="Otros (Desconocidos)", variable=self.var_otros
        )
        chk_otros.pack(side="left", expand=True)

        # --- SECCIÓN: FILTROS DE FECHA Y SISTEMA ---
        frame_filtros = ttk.LabelFrame(parent, text=" 3. Filtros y Reglas ", padding=10)
        frame_filtros.pack(fill="x", padx=15, pady=5)

        self.var_ignorar_sistema = tk.BooleanVar(value=True)
        chk_sis = ttk.Checkbutton(
            frame_filtros,
            text="Omitir archivos de programa/sistema (.exe, .dll, .sqlite, etc.)",
            variable=self.var_ignorar_sistema,
        )
        chk_sis.grid(row=0, column=0, columnspan=2, sticky="w", pady=4)

        ttk.Label(frame_filtros, text="Fecha Inicio (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_inicio = ttk.Entry(frame_filtros, width=15)
        self.ent_inicio.insert(0, "2024-01-01")
        self.ent_inicio.grid(row=1, column=1, sticky="w", pady=2)

        ttk.Label(frame_filtros, text="Fecha Fin (YYYY-MM-DD):").grid(row=2, column=0, sticky="w", pady=2)
        self.ent_fin = ttk.Entry(frame_filtros, width=15)
        self.ent_fin.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.ent_fin.grid(row=2, column=1, sticky="w", pady=2)

        ttk.Label(frame_filtros, text="Acción:").grid(row=3, column=0, sticky="w", pady=5)
        self.var_modo = tk.StringVar(value="copiar")
        r1 = ttk.Radiobutton(frame_filtros, text="Copiar", variable=self.var_modo, value="copiar")
        r2 = ttk.Radiobutton(frame_filtros, text="Mover", variable=self.var_modo, value="mover")
        r1.grid(row=3, column=1, sticky="w")
        r2.grid(row=3, column=1, sticky="e")

        # --- SECCIÓN: EJECUCIÓN Y CONSOLA ---
        frame_ejec = ttk.Frame(parent, padding=10)
        frame_ejec.pack(fill="both", expand=True, padx=15)

        self.btn_iniciar = ttk.Button(
            frame_ejec,
            text="🚀 INICIAR RESPALDO ORGANIZADO",
            command=self.iniciar_hilo_org,
        )
        self.btn_iniciar.pack(fill="x", pady=5)

        self.txt_log_org = tk.Text(frame_ejec, height=12, state="disabled")
        self.txt_log_org.pack(fill="both", expand=True)

    def seleccionar_destino(self):
        dir_sel = filedialog.askdirectory()
        if dir_sel:
            self.ruta_destino = Path(dir_sel)
            self.lbl_destino_val.config(text=f"Destino: {self.ruta_destino}")

    def log_org(self, mensaje):
        self.txt_log_org.config(state="normal")
        self.txt_log_org.insert("end", mensaje + "\n")
        self.txt_log_org.see("end")
        self.root.update_idletasks()
        self.txt_log_org.config(state="disabled")

    def iniciar_hilo_org(self):
        self.btn_iniciar.config(state="disabled")
        threading.Thread(target=self.proceso_respaldo, daemon=True).start()

    def proceso_respaldo(self):
        self.log_org("=== INICIANDO PROCESO DE RESPALDO ===")
        # Validar Fechas
        try:
            f_inicio = datetime.strptime(self.ent_inicio.get().strip(), "%Y-%m-%d")
            f_fin = datetime.strptime(self.ent_fin.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD")
            self.btn_iniciar.config(state="normal")
            return

        exts_permitidas = set()
        for cat, checked in self.vars_cats.items():
            if checked.get():
                exts_permitidas.update(CATEGORIAS[cat])

        hashes_conocidos = set()
        procesados = 0
        omitidos = 0

        modo = self.var_modo.get()
        ruta_dest_abs = self.ruta_destino.resolve()

        for origen in self.rutas_origen:
            if not origen.exists():
                continue

            self.log_org(f"\nScanning: {origen.name}...")

            for archivo in origen.rglob("*"):
                if not archivo.is_file(): continue
                if ruta_dest_abs in archivo.resolve().parents: continue
                if archivo.name.startswith("~"): continue
                if self.ruta_destino in archivo.parents or archivo == self.ruta_destino: continue

                ext = archivo.suffix.lower()

                if self.var_ignorar_sistema.get() and ext in EXTENSIONES_SISTEMA: continue

                es_conocido = any(ext in exts for exts in CATEGORIAS.values())
                if es_conocido and ext not in exts_permitidas: continue
                if not es_conocido and not self.var_otros.get(): continue

                try:
                    ts = os.path.getmtime(archivo)
                    f_mod = datetime.fromtimestamp(ts)
                except OSError:
                    continue

                if not (f_inicio <= f_mod <= f_fin): continue

                h = self.calcular_hash(archivo)
                if not h: continue
                if h in hashes_conocidos:
                    self.log_org(f"[DUPLICADO OMITIDO] {archivo.name}")
                    omitidos += 1
                    continue

                hashes_conocidos.add(h)

                cat_final = "Otros"
                for c, exts in CATEGORIAS.items():
                    if ext in exts:
                        cat_final = c
                        break

                anio_mes = f_mod.strftime("%Y/%m_%B")
                dir_salida = self.ruta_destino / cat_final / anio_mes
                dir_salida.mkdir(parents=True, exist_ok=True)

                dest_final = dir_salida / archivo.name
                contador = 1
                while dest_final.exists():
                    dest_final = dir_salida / f"{archivo.stem}_{contador}{archivo.suffix}"
                    contador += 1

                try:
                    if modo == "copiar":
                        shutil.copy2(archivo, dest_final)
                    else:
                        shutil.move(archivo, dest_final)
                    self.log_org(f"[OK] {archivo.name} -> {cat_final}/{anio_mes}")
                    procesados += 1
                except Exception as e:
                    self.log_org(f"[ERROR] {archivo.name}: {e}")

        self.log_org("\n=== RESPALDO FINALIZADO ===")
        self.log_org(f"Archivos procesados: {procesados}")
        self.log_org(f"Duplicados omitidos: {omitidos}")
        messagebox.showinfo("Completado", "¡El respaldo ha sido completado!")
        self.btn_iniciar.config(state="normal")


    # ==========================================
    # PESTAÑA 2: NUEVO MÓDULO DE MIGRACIÓN
    # ==========================================
    def crear_interfaz_migracion(self, parent):
        # --- SECCIÓN: RUTA PUENTE (USB) ---
        frame_rutas = ttk.LabelFrame(parent, text=" 1. Unidad Puente (USB / Disco Externo) ", padding=10)
        frame_rutas.pack(fill="x", padx=15, pady=10)

        lbl_desc = ttk.Label(
            frame_rutas, 
            text="Selecciona la carpeta raíz de tu USB. El programa creará/leerá una carpeta llamada 'ResQ_Bridge'."
        )
        lbl_desc.pack(anchor="w", pady=2)

        btn_dest = ttk.Button(
            frame_rutas,
            text="Seleccionar Unidad Puente",
            command=self.seleccionar_destino_migracion,
        )
        btn_dest.pack(anchor="w", pady=5)

        self.lbl_rutamig_val = ttk.Label(
            frame_rutas,
            text=f"Ruta actual: {self.ruta_migracion}",
            foreground="blue",
            wraplength=550,
        )
        self.lbl_rutamig_val.pack(anchor="w")

        # --- SECCIÓN: ACCIONES ---
        frame_acciones = ttk.LabelFrame(parent, text=" 2. Acciones de Migración ", padding=10)
        frame_acciones.pack(fill="x", padx=15, pady=5)

        self.btn_exportar = ttk.Button(
            frame_acciones,
            text="⬆️ EXPORTAR (Extraer de esta PC hacia el Puente)",
            command=lambda: threading.Thread(target=self.proceso_exportacion, daemon=True).start()
        )
        self.btn_exportar.pack(fill="x", pady=5)

        self.btn_importar = ttk.Button(
            frame_acciones,
            text="⬇️ RESTAURAR (Inyectar del Puente a esta PC)",
            command=lambda: threading.Thread(target=self.proceso_importacion, daemon=True).start()
        )
        self.btn_importar.pack(fill="x", pady=5)

        # --- SECCIÓN: CONSOLA ---
        self.txt_log_mig = tk.Text(parent, height=15, state="disabled")
        self.txt_log_mig.pack(fill="both", expand=True, padx=15, pady=10)

    def seleccionar_destino_migracion(self):
        dir_sel = filedialog.askdirectory()
        if dir_sel:
            self.ruta_migracion = Path(dir_sel)
            self.lbl_rutamig_val.config(text=f"Ruta actual: {self.ruta_migracion}")

    def log_mig(self, mensaje):
        self.txt_log_mig.config(state="normal")
        self.txt_log_mig.insert("end", mensaje + "\n")
        self.txt_log_mig.see("end")
        self.root.update_idletasks()
        self.txt_log_mig.config(state="disabled")

    def proceso_exportacion(self):
        self.btn_exportar.config(state="disabled")
        self.btn_importar.config(state="disabled")
        self.log_mig("=== INICIANDO EXPORTACIÓN ESTRUCTURAL ===")
        
        dir_puente = self.ruta_migracion / "ResQ_Bridge"
        dir_puente.mkdir(parents=True, exist_ok=True)
        procesados = 0

        for origen in self.rutas_origen:
            if not origen.exists(): continue
            self.log_mig(f"\nExtrayendo de: {origen.name}...")

            for archivo in origen.rglob("*"):
                if not archivo.is_file(): continue
                
                # Evitar escaneo de la propia carpeta puente si está en el origen
                if dir_puente in archivo.parents: continue 
                
                # Omitir temporales
                if archivo.name.startswith("~"): continue

                try:
                    # Capturar la ruta relativa respecto a C:\Users\TuUsuario
                    ruta_relativa = archivo.relative_to(Path.home())
                    dest_final = dir_puente / ruta_relativa
                    
                    # Crear los directorios intermedios en la USB
                    dest_final.parent.mkdir(parents=True, exist_ok=True)

                    shutil.copy2(archivo, dest_final)
                    self.log_mig(f"[OK] -> {ruta_relativa}")
                    procesados += 1
                except ValueError:
                    # Ocurre si el archivo no es hijo de Path.home()
                    continue
                except Exception as e:
                    self.log_mig(f"[ERROR] {archivo.name}: {e}")

        self.log_mig(f"\n=== EXPORTACIÓN COMPLETADA ({procesados} archivos) ===")
        messagebox.showinfo("Puente Listo", f"Se han exportado {procesados} archivos al puente.")
        self.btn_exportar.config(state="normal")
        self.btn_importar.config(state="normal")

    def proceso_importacion(self):
        self.btn_exportar.config(state="disabled")
        self.btn_importar.config(state="disabled")
        self.log_mig("=== INICIANDO RESTAURACIÓN ESTRUCTURAL ===")
        
        dir_puente = self.ruta_migracion / "ResQ_Bridge"
        
        if not dir_puente.exists():
            self.log_mig("\n[ERROR] No se encontró la carpeta 'ResQ_Bridge' en la ruta seleccionada.")
            messagebox.showerror("Error", "No se detectó un Puente de Migración válido en esta unidad.")
            self.btn_exportar.config(state="normal")
            self.btn_importar.config(state="normal")
            return

        procesados = 0
        self.log_mig(f"Leyendo estructura desde: {dir_puente}...\n")

        for archivo in dir_puente.rglob("*"):
            if not archivo.is_file(): continue

            try:
                # Capturar la ruta relativa desde la carpeta puente (Ej: Desktop\foto.jpg)
                ruta_relativa = archivo.relative_to(dir_puente)
                # Inyectar en el nuevo Path.home() (C:\Users\NuevoUsuario)
                dest_final = Path.home() / ruta_relativa
                
                dest_final.parent.mkdir(parents=True, exist_ok=True)

                shutil.copy2(archivo, dest_final)
                self.log_mig(f"[OK] Restaurado -> {ruta_relativa}")
                procesados += 1
            except Exception as e:
                self.log_mig(f"[ERROR] {archivo.name}: {e}")

        self.log_mig(f"\n=== RESTAURACIÓN COMPLETADA ({procesados} archivos) ===")
        messagebox.showinfo("Restauración Lista", f"Se han inyectado {procesados} archivos a esta computadora.")
        self.btn_exportar.config(state="normal")
        self.btn_importar.config(state="normal")

    # ==========================================
    # UTILIDADES GENERALES
    # ==========================================
    def calcular_hash(self, ruta, chunk_size=1024 * 1024):
        sha256 = hashlib.sha256()
        try:
            with open(ruta, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (PermissionError, FileNotFoundError, OSError):
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = AppOrganizadorV3(root)
    root.mainloop()
# 🛡️ ResQ File Manager - Historial de Desarrollo y Versiones

## 📜 Historia y Concepto del Proyecto
ResQ File Manager nació para resolver un problema recurrente en el soporte técnico y el rescate de datos: la falta de una herramienta ligera, gráfica y 100% portable que combine en una sola interfaz la clasificación de archivos, la eliminación de duplicados sin margen de error y la migración rápida de perfiles de usuario sin depender de comandos complejos de terminal.

---

## 🛠️ Evolución de Versiones

### 🔹 v1.0.0 — El Prototipo Base (CLI y Pruebas Iniciales)
* **Objetivo:** Probar el motor lógico de organización de archivos.
* **Características:**
  * Script inicial en Python utilizando la biblioteca estándar (`os`, `shutil`).
  * Clasificación simple basada en diccionarios de extensiones (`.pdf`, `.docx` -> Documentos; `.jpg`, `.png` -> Imágenes).
* **Errores y Desafíos:**
  * **Manejo de rutas:** Errores con caracteres especiales y espacios en rutas de Windows.
  * **Sin GUI:** Solo ejecutable por consola de comandos, lo que complicaba la selección de carpetas origen/destino.

---

### 🔹 v1.5.0 — La Interfaz Gráfica y Filtro de Fechas
* **Objetivo:** Crear una interfaz accesible y añadir precisión al filtrado.
* **Características:**
  * Diseño de la GUI estructurada con **Tkinter**.
  * Incorporación del módulo de filtrado avanzado por rango de fechas (fecha de modificación del archivo).
  * Inclusión de validaciones visuales para la selección de directorios.
* **Errores y Desafíos:**
  * **Pantalla "No responde" (Congelamiento de la GUI):** Al escanear carpetas masivas con miles de archivos, la ventana principal de Tkinter se bloqueaba por completo.
  * **Solución:** Implementación de multiprocesamiento/hilos (`threading`) para ejecutar el escaneo en segundo plano y mantener la interfaz fluida.

---

### 🔹 v2.0.0 — Deduplicación Avanzada y Módulo ResQ Bridge
* **Objetivo:** Prevenir la duplicidad de archivos de forma matemáticamente exacta e incorporar la migración de perfiles.
* **Características:**
  * **Deduplicador por HASH:** Implementación del algoritmo `SHA-256` mediante `hashlib` para comparar la huella digital binaria de los archivos (evitando falsos positivos basados solo en el nombre).
  * **ResQ Bridge:** Módulo para mapear y clonar estructuras de carpetas de usuario (`Documentos`, `Imágenes`, `Descargas`) omitiendo automáticamente la basura del sistema (`AppData` temporal, cachés).
* **Errores y Desafíos:**
  * **Archivos bloqueados por el sistema:** Excepciones de permisos (`PermissionError`) al intentar leer archivos temporales o protegidos durante la deduplicación.
  * **Solución:** Se implementó un sistema de control de excepciones con bloques `try-except` para omitir archivos protegidos sin detener el proceso general.

---

### 🔹 v3.0.0 — Empaquetado, Portabilidad y Licenciamiento Libre (Versión Actual)
* **Objetivo:** Convertir el proyecto en un software distribuible para el usuario final.
* **Características:**
  * Compilación a ejecutable binario único (`.exe`) autocontenido utilizando **PyInstaller**.
  * Cero dependencias externas requeridas en el sistema de destino.
  * Adopción oficial de la licencia **GNU General Public License v3.0 (GPLv3)** para garantizar que el proyecto permanezca como software libre.
  * Creación del repositorio público en GitHub con documentación estructurada (`README.md`).

---

## 🛑 Errores Principales Solucionados Durante la Construcción

| Problema Encontrado | Causa Raíz | Solución Aplicada |
| :--- | :--- | :--- |
| Bloqueo de la ventana principal al procesar archivos masivos. | Tkinter corre en un solo hilo (*Single-threaded*) por defecto. | Mapeo de ejecuciones pesadas mediante el módulo `threading`. |
| Rendimiento lento al calcular HASH en archivos de varios Gigabytes. | Lectura completa en memoria RAM de archivos pesados. | Carga de archivos en bloques (*chunks*) de datos pequeños de 64 KB. |
| Colisión de nombres al mover archivos con el mismo nombre pero diferente contenido. | Sobreescritura no deseada en la carpeta de destino. | Adición de sufijos numéricos automáticos al detectar nombres idénticos. |
| Fallo al ejecutar en computadoras sin Python instalado. | Dependencia del intérprete del sistema. | Compilación estática con PyInstaller en formato `--onefile`. |

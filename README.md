# 🛡️ ResQ File Manager

> **Organizador inteligente de archivos y gestor de migración para Windows.**

**ResQ File Manager** es una herramienta de escritorio ligera y portátil desarrollada en Python y Tkinter. Está diseñada para limpiar, clasificar y migrar archivos personales de forma automática, eficiente y segura.

---

## ✨ Características Principales

### 📁 1. Organizador Inteligente
* **Clasificación Automática:** Filtra y mueve documentos, imágenes, videos y archivos comprimidos a sus carpetas correspondientes.
* **Cero Duplicados:** Utiliza verificación por **HASH** para detectar archivos idénticos y evitar almacenar copias innecesarias.
* **Filtros Avanzados:** Permite seleccionar rangos de fechas específicos para organizar solo lo que necesitas.

### 🌉 2. Puente de Migración (`ResQ Bridge`)
* **Clonación de Estructura:** Escanea y clona la estructura de carpetas del perfil de usuario (`Escritorio`, `Documentos`, `Descargas`, etc.).
* **Migración Transparente:** Diseñado para facilitar la transferencia de archivos personales entre computadoras sin perder el orden.
* **Filtro de Basura:** Omite automáticamente archivos de caché, temporales del sistema y accesos directos rotos (`.lnk`).

### ⚡ 3. 100% Portable
* **Ejecutable Único (.exe):** No requiere instalación previa de Python ni dependencias externas.
* **Rutas Dinámicas:** Se adapta automáticamente a cualquier perfil de usuario en Windows 10 y 11.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.14
* **Interfaz Gráfica:** Tkinter / ttk
* **Procesamiento de Imágenes / Íconos:** Pillow (PIL)
* **Empaquetado:** PyInstaller

---

## ⚖️ Licencia

Este proyecto está bajo la Licencia **GNU General Public License v3.0** (GNU GPLv3).

* **Libertad de uso:** Eres libre de usar, estudiar, compartir y modificar este software.
* **Copyleft:** Cualquier obra derivada o modificación distribuida debe publicarse bajo esta misma licencia y con su código fuente disponible.

Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

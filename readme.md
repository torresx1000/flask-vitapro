# Flask-Vitapro

Sistema web desarrollado con Flask para procesar información operativa mediante archivos **PDF** y **Excel**, almacenarla en base de datos y generar reportes automatizados.

## Características

* 📄 Procesamiento de archivos **PDF**
* 📊 Procesamiento de archivos **Excel (.xlsx y .xlsm)**
* ⚙️ Soporte para **Excel con macros**
* 🗄️ Almacenamiento en base de datos SQLite
* 📈 Dashboard con visualización de datos
* 🔄 Exportación de registros a Excel
* 🧹 Limpieza automática de archivos subidos
* 🛠 Arquitectura modular (routes / services / models)

---

## Arquitectura del Proyecto

```
Proyecto Flask-Vitapro/
│
├── app/
│   ├── routes/        # Endpoints Flask
│   ├── services/      # Lógica de negocio
│   ├── models/        # Modelos SQLAlchemy
│   ├── db/            # Conexión base de datos
│   ├── utils/         # Funciones auxiliares
│   └── config.py      # Configuración global
│
├── templates/         # HTML Jinja2
├── static/            # CSS / JS
├── uploads/           # Archivos procesados
├── database/          # Base de datos SQLite
│
├── run.py             # Punto de entrada de la aplicación
└── requirements.txt   # Dependencias
```

---

## Tecnologías utilizadas

* Python
* Flask
* SQLAlchemy
* OpenPyXL
* PDFPlumber
* SQLite

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/flask-vitapro.git
cd flask-vitapro
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

### 3. Activar entorno virtual

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar la aplicación

```bash
python run.py
```

La aplicación se iniciará en:

```
http://127.0.0.1:5000
```

---

## Funcionalidades principales

### Procesar Excel

Permite subir archivos Excel y completar datos automáticamente usando información almacenada en la base de datos.

Soporta:

* `.xlsx`
* `.xlsm` (Excel con macros)

### Procesar PDF

Extrae información desde reportes PDF y la almacena en la base de datos.

### Dashboard

Visualización de:

* Despachos por código
* Despachos por fecha
* Despachos por turno

### Exportación

Permite exportar todos los registros almacenados en la base de datos a un archivo Excel.

---

## Base de Datos

El sistema utiliza **SQLite** para almacenamiento local.

Archivo:

```
database/bd_vitapro.db
```

---

## Buenas prácticas implementadas

* Arquitectura modular
* Separación de lógica (routes / services)
* Manejo de archivos Excel con macros
* Limpieza automática de archivos subidos
* Validación de extensiones

---

## Licencia

Proyecto de uso educativo / interno.

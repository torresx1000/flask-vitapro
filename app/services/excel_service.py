import os
import os
from io import BytesIO

from openpyxl import Workbook, load_workbook
from sqlalchemy import func

from app.db.database import session
from app.models import Despacho

import os
from openpyxl import load_workbook
from sqlalchemy import func

from app.db.database import session
from app.models import Despacho


def procesar_excel(file_obj, form_data, upload_folder, allowed_extensions):

    filename = file_obj.filename or ""

    if (
        not filename
        or "." not in filename
        or filename.rsplit(".", 1)[1].lower() not in allowed_extensions
    ):
        raise ValueError("Solo se permiten archivos Excel (.xlsx y .xlsm)")

    os.makedirs(upload_folder, exist_ok=True)

    path = os.path.join(upload_folder, filename)

    file_obj.save(path)

    ext = filename.rsplit(".", 1)[1].lower()

    # decidir qué proceso usar
    if ext == "xlsm":
        return procesar_excel_xlsm(path, form_data)
    else:
        return procesar_excel_xlsx(path, form_data)


# -----------------------------
# PROCESAR XLSX
# -----------------------------
def procesar_excel_xlsx(path, form_data):

    wb = load_workbook(path)

    procesar_datos(wb, form_data)

    wb.save(path)
    wb.close()

    return path


# -----------------------------
# PROCESAR XLSM (CON MACROS)
# -----------------------------
def procesar_excel_xlsm(path, form_data):

    wb = load_workbook(path, keep_vba=True)

    procesar_datos(wb, form_data)

    wb.save(path)
    wb.close()

    return path


# -----------------------------
# LOGICA DE PROCESAMIENTO
# -----------------------------
def procesar_datos(wb, form_data):

    col_codigo = form_data["col_codigo"].upper()
    fila_inicio = int(form_data["fila_inicio"])
    fila_final = int(form_data["fila_final"])
    col_resultado = form_data["col_resultado"].upper()
    hoja_nombre = form_data["hoja"]

    if hoja_nombre not in wb.sheetnames:
        raise KeyError(f"La hoja no existe. Hojas disponibles: {wb.sheetnames}")

    sheet = wb[hoja_nombre]

    # 🔹 construir diccionario limpio desde la base de datos
    resultados = {
        str(codigo).strip(): float(valor) if valor is not None else 0
        for codigo, valor in session.query(
            Despacho.codigo,
            func.sum(Despacho.despacho * Despacho.peso_promedio),
        )
        .group_by(Despacho.codigo)
        .all()
    }

    # 🔹 recorrer filas del Excel
    for fila in range(fila_inicio, fila_final + 1):

        codigo = sheet[f"{col_codigo}{fila}"].value

        if not codigo:
            continue

        # normalizar código para evitar errores de tipo
        codigo = str(codigo).strip()

        if codigo in resultados:
            sheet[f"{col_resultado}{fila}"] = resultados[codigo]

def exportar_excel():

    registros = session.query(Despacho).all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Registros"

    headers = [
        "ID",
        "ID Carga",
        "Fecha",
        "Turno",
        "Codigo",
        "Lote",
        "Peso Promedio",
        "Ubicacion",
        "Stock Inicial",
        "Cantidad SAP",
        "Despacho",
        "Saldo",
        "Observaciones",
    ]

    ws.append(headers)

    for r in registros:
        ws.append([
            r.id,
            r.id_carga,
            r.fecha,
            r.turno,
            r.codigo,
            r.lote,
            r.peso_promedio,
            r.ubicacion,
            r.stock_inicial,
            r.cantidad_sap,
            r.despacho,
            r.saldo,
            r.observaciones,
        ])

    bio = BytesIO()

    wb.save(bio)
    wb.close()

    bio.seek(0)

    return bio.getvalue()
import os
import re

import pdfplumber

from app.db.database import session
from app.models import Despacho
from sqlalchemy import func


def procesar_pdf(file_obj, upload_folder: str):
    """Parse a PDF and store extracted rows in the Despacho table."""

    filename = file_obj.filename or ""
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext != 'pdf':
        raise ValueError("Solo se permiten archivos PDF")

    # Save to a temporary path inside uploads
    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, "temp.pdf")
    file_obj.save(path)

    datos = []
    fecha = None
    turno = None

    with pdfplumber.open(path) as pdf:
        primera = pdf.pages[0]
        texto = primera.extract_text() or ""

        fecha_match = re.search(r"FECHA:(\d{4}-\d{2}-\d{2})", texto)
        turno_match = re.search(r"TURNO:(T\d)", texto)

        if fecha_match:
            fecha = fecha_match.group(1)
        if turno_match:
            turno = turno_match.group(1)

        ultimo = session.query(func.max(Despacho.id_carga)).scalar()
        id_carga = 1 if ultimo is None else (ultimo + 1)

        for pagina in pdf.pages:
            tabla = pagina.extract_table()
            if not tabla:
                continue

            for fila in tabla[1:]:
                if not fila or not any(fila):
                    continue
                if str(fila[0]).strip() == "":
                    continue

                try:
                    datos.append({
                        "codigo": fila[0],
                        "lote": fila[1],
                        "peso_promedio": _to_float(fila[2]),
                        "ubicacion": fila[3],
                        "stock": _to_float(fila[4]),
                        "cantidad": _to_float(fila[5]),
                        "despacho": _to_float(fila[6]),
                        "saldo": _to_float(fila[7]),
                        "observaciones": fila[8] if len(fila) > 8 else "",
                    })
                except Exception:
                    continue

    for d in datos:
        registro = Despacho(
            id_carga=id_carga,
            fecha=fecha,
            turno=turno,
            codigo=d["codigo"],
            lote=d["lote"],
            peso_promedio=d["peso_promedio"],
            ubicacion=d["ubicacion"],
            stock_inicial=d["stock"],
            cantidad_sap=d["cantidad"],
            despacho=d["despacho"],
            saldo=d["saldo"],
            observaciones=d["observaciones"],
        )
        session.add(registro)

    session.commit()

    return True


def _to_float(valor):
    try:
        return float(str(valor).replace(",", "."))
    except Exception:
        return 0

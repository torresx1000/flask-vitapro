# -*- coding: utf-8 -*-import os

from flask import Blueprint, request, redirect, url_for, render_template, current_app, flash

from app.services.pdf_service import procesar_pdf
from app.db.database import session
from app.models import Despacho, RecoveryData

pdf_bp = Blueprint("pdf", __name__)


@pdf_bp.route("/subir_pdf", methods=["POST"])
def subir_pdf():

    if "pdf" not in request.files:
        flash("No se envió ningún archivo.")
        return redirect(url_for("dashboard.home"))

    archivo = request.files["pdf"]

    if archivo.filename == "":
        flash("No se seleccionó archivo.")
        return redirect(url_for("dashboard.home"))

    try:
        procesar_pdf(archivo, current_app.config["UPLOAD_FOLDER"])
        flash("PDF procesado correctamente.")
    except ValueError as e:
        flash(f"Error al procesar PDF: {str(e)}")
    except Exception as e:
        flash(f"Error inesperado: {str(e)}")

    return redirect(url_for("dashboard.home"))


@pdf_bp.route("/recovery")
def ver_recovery():

    registros = session.query(RecoveryData).all()

    return render_template(
        "recovery.html",
        registros=registros
    )


@pdf_bp.route("/limpiar_tabla")
def limpiar_tabla():

    try:

        registros = session.query(Despacho).all()

        for r in registros:
            backup = RecoveryData(
                id_carga=r.id_carga,
                fecha=r.fecha,
                turno=r.turno,
                codigo=r.codigo,
                lote=r.lote,
                peso_promedio=r.peso_promedio,
                ubicacion=r.ubicacion,
                stock_inicial=r.stock_inicial,
                cantidad_sap=r.cantidad_sap,
                despacho=r.despacho,
                saldo=r.saldo,
                observaciones=r.observaciones,
            )

            session.add(backup)

        session.query(Despacho).delete()

        session.commit()

        flash("Tabla Despacho limpiada y respaldada correctamente.")

    except Exception as e:

        session.rollback()

        flash(f"Error al limpiar tabla: {str(e)}")

    return redirect(url_for("dashboard.home"))


@pdf_bp.route("/vaciar_recovery")
def vaciar_recovery():

    try:

        session.query(RecoveryData).delete()

        session.commit()

        flash("Tabla Recovery vaciada correctamente.")

    except Exception as e:

        session.rollback()

        flash(f"Error al vaciar recovery: {str(e)}")

    return redirect(url_for("pdf.ver_recovery"))
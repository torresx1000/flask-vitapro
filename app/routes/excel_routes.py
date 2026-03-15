import os

from flask import (
    Blueprint,
    request,
    render_template,
    send_file,
    Response,
    flash,
    redirect,
    url_for,
    current_app,
)

from app.services.excel_service import procesar_excel
from app.services.excel_service import exportar_excel as exportar_excel_service
from app.utils.file_utils import clean_old_files

excel_bp = Blueprint("excel", __name__)

@excel_bp.route("/procesar_excel", methods=["GET", "POST"])
def procesar_excel_route():

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    # limpiar archivos antiguos
    clean_old_files(upload_folder)

    if request.method == "GET":
        return render_template("procesar_excel.html")

    if "excel" not in request.files:
        return "No se subio archivo", 400

    archivo = request.files["excel"]

    if archivo.filename == "":
        return "No se selecciono archivo", 400

    try:
        ruta = procesar_excel(
            archivo,
            request.form,
            upload_folder,
            current_app.config["ALLOWED_EXCEL_EXTENSIONS"],
        )

    except ValueError as e:
        return str(e), 400

    except KeyError as e:
        return str(e), 400

    # detectar extensión del archivo para usar el mimetype correcto
    ext = os.path.splitext(ruta)[1].lower()

    if ext == ".xlsm":
        mimetype = "application/vnd.ms-excel.sheet.macroEnabled.12"
    else:
        mimetype = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # enviar archivo procesado
    return send_file(
        ruta,
        as_attachment=True,
        download_name=os.path.basename(ruta),
        mimetype=mimetype,
    )

@excel_bp.route("/limpiar_archivos")
def limpiar_archivos():

    carpeta = current_app.config["UPLOAD_FOLDER"]

    eliminados = clean_old_files(carpeta, horas=0)

    flash(f"Se eliminaron {eliminados} archivos.")

    return redirect(url_for("dashboard.home"))


@excel_bp.route("/exportar_excel")
def exportar_excel():

    data = exportar_excel_service()

    if not data:
        flash("No hay datos para exportar.")
        return redirect(url_for("dashboard.home"))

    return Response(
        data,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=registros.xlsx"
        },
    )
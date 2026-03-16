from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from sqlalchemy import func

from app.db.database import session
from app.models import Despacho

# Blueprint

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route("/data_despachos")
def data_despachos():
    resultados = session.query(
        Despacho.codigo,
        func.sum(Despacho.despacho),
    ).group_by(Despacho.codigo).all()

    codigos = [r[0] for r in resultados]
    cantidades = [float(r[1]) for r in resultados]

    return jsonify({
        "codigos": codigos,
        "cantidades": cantidades,
    })


@dashboard_bp.route("/dashboard")
def dashboard():
    total_stock = session.query(func.sum(Despacho.stock_inicial)).scalar() or 0
    total_sap = session.query(func.sum(Despacho.cantidad_sap)).scalar() or 0
    total_despacho = session.query(func.sum(Despacho.despacho)).scalar() or 0
    total_saldo = session.query(func.sum(Despacho.saldo)).scalar() or 0

    total_registros = session.query(func.count(Despacho.id)).scalar()
    total_cargas = session.query(func.count(func.distinct(Despacho.id_carga))).scalar()

    return render_template(
        "dashboard.html",
        total_stock=total_stock,
        total_sap=total_sap,
        total_despacho=total_despacho,
        total_saldo=total_saldo,
        total_registros=total_registros,
        total_cargas=total_cargas,
    )


@dashboard_bp.route("/")
def home():
    registros = session.query(Despacho).all()
    return render_template("index.html", registros=registros)


@dashboard_bp.route("/data_fechas")
def data_fechas():
    resultados = session.query(
        Despacho.fecha,
        func.sum(Despacho.despacho),
    ).group_by(Despacho.fecha).order_by(Despacho.fecha).all()

    fechas = [str(r[0]) for r in resultados]
    cantidades = [float(r[1]) for r in resultados]

    return jsonify({
        "fechas": fechas,
        "cantidades": cantidades,
    })


@dashboard_bp.route("/data_turnos")
def data_turnos():
    resultados = session.query(
        Despacho.turno,
        func.sum(Despacho.despacho),
    ).group_by(Despacho.turno).all()

    turnos = [r[0] for r in resultados]
    cantidades = [float(r[1]) for r in resultados]

    return jsonify({
        "turnos": turnos,
        "cantidades": cantidades,
    })


def _form_float(value):
    """Convierte valor de formulario a float; cadena vacía o inválida -> None (evita error SQLAlchemy)."""
    if value is None:
        return None
    s = str(value).strip()
    if s == "":
        return None
    try:
        return float(s.replace(",", "."))
    except (ValueError, TypeError):
        return None


@dashboard_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    registro = session.get(Despacho, id)

    if request.method == "POST":
        registro.codigo = (request.form.get("codigo") or "").strip() or None
        registro.lote = (request.form.get("lote") or "").strip() or None
        registro.peso_promedio = _form_float(request.form.get("peso"))
        registro.ubicacion = (request.form.get("ubicacion") or "").strip() or None
        registro.stock_inicial = _form_float(request.form.get("stock"))
        registro.cantidad_sap = _form_float(request.form.get("cantidad"))
        registro.despacho = _form_float(request.form.get("despacho"))
        registro.saldo = _form_float(request.form.get("saldo"))
        registro.observaciones = (request.form.get("obs") or "").strip() or None

        session.commit()
        return redirect(url_for("dashboard.home"))

    return render_template("editar.html", r=registro)


@dashboard_bp.route("/eliminar/<int:id>")
def eliminar(id):
    registro = session.get(Despacho, id)
    session.delete(registro)
    session.commit()
    return redirect(url_for("dashboard.home"))

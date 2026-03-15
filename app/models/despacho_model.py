from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base
class RecoveryData(Base):

    __tablename__ = "recovery_data"

    id = Column(Integer, primary_key=True)

    id_carga = Column(Integer)

    fecha = Column(String(20))
    turno = Column(String(10))

    codigo = Column(String(20))
    lote = Column(String(20))

    peso_promedio = Column(Float)

    ubicacion = Column(String(50))

    stock_inicial = Column(Float)
    cantidad_sap = Column(Float)

    despacho = Column(Float)
    saldo = Column(Float)

    observaciones = Column(String(200))
    
    def __init__(self, id_carga, fecha, turno, codigo, lote,
                 peso_promedio, ubicacion, stock_inicial,
                 cantidad_sap, despacho, saldo, observaciones):

        self.id_carga = id_carga
        self.fecha = fecha
        self.turno = turno

        self.codigo = codigo
        self.lote = lote

        self.peso_promedio = peso_promedio
        self.ubicacion = ubicacion

        self.stock_inicial = stock_inicial
        self.cantidad_sap = cantidad_sap

        self.despacho = despacho
        self.saldo = saldo

        self.observaciones = observaciones

class Despacho(Base):

    __tablename__ = "despacho"

    id = Column(Integer, primary_key=True)

    id_carga = Column(Integer)

    fecha = Column(String(20))
    turno = Column(String(10))

    codigo = Column(String(20))
    lote = Column(String(20))

    peso_promedio = Column(Float)

    ubicacion = Column(String(50))

    stock_inicial = Column(Float)
    cantidad_sap = Column(Float)

    despacho = Column(Float)
    saldo = Column(Float)

    observaciones = Column(String(200))


    def __init__(self, id_carga, fecha, turno, codigo, lote,
                 peso_promedio, ubicacion, stock_inicial,
                 cantidad_sap, despacho, saldo, observaciones):

        self.id_carga = id_carga
        self.fecha = fecha
        self.turno = turno

        self.codigo = codigo
        self.lote = lote

        self.peso_promedio = peso_promedio
        self.ubicacion = ubicacion

        self.stock_inicial = stock_inicial
        self.cantidad_sap = cantidad_sap

        self.despacho = despacho
        self.saldo = saldo

        self.observaciones = observaciones
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "supersecretkey123"
    DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "database", "bd_vitapro.db")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXCEL_EXTENSIONS = {"xlsx", "xlsm"}
    ALLOWED_PDF_EXTENSIONS = {"pdf"}

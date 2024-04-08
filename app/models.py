from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
#from . import db

db = SQLAlchemy()

class IMCResult(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    weight = db.Column(db.Float, nullable = False)
    height = db.Column(db.Float, nullable = False)
    bmi = db.Column(db.Float, nullable = False)
    calculated_at = db.Column(db.DateTime, default = datetime.utcnow) #utcnow is deprecated

    def __repr__(self):
        return "Resultado do IMC: {self.bmi} calculado em {self.calculated_at}"
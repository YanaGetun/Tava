from datetime import datetime
from app import db

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto_assets.id'), nullable=False)
    model_type = db.Column(db.String(50))  # technical, sentiment, hybrid
    predicted_price = db.Column(db.Float, nullable=False)
    predicted_direction = db.Column(db.String(10))  # up, down, neutral
    confidence = db.Column(db.Float)  # 0.0 to 1.0
    horizon = db.Column(db.String(20))  # 1h, 24h, 7d
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    valid_until = db.Column(db.DateTime)
    
    # РЎРІСЏР·Рё
    risk_assessment = db.relationship('RiskAssessment', backref='prediction', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<Prediction {self.crypto_id} {self.predicted_direction}>'

class RiskAssessment(db.Model):
    __tablename__ = 'risk_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('predictions.id'), nullable=False)
    risk_level = db.Column(db.String(20))  # low, medium, high
    volatility_score = db.Column(db.Float)
    var_95 = db.Column(db.Float)  # Value at Risk 95%
    recommendations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<RiskAssessment {self.risk_level}>'

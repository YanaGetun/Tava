from datetime import datetime
from app import db

class CryptoAsset(db.Model):
    __tablename__ = 'crypto_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, nullable=False)  # BTC, ETH, etc
    name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float)
    market_cap = db.Column(db.Float)
    volume_24h = db.Column(db.Float)
    price_change_24h = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # РЎРІСЏР·Рё
    market_data = db.relationship('MarketData', backref='crypto', lazy='dynamic')
    predictions = db.relationship('Prediction', backref='crypto', lazy='dynamic')
    
    def __repr__(self):
        return f'<CryptoAsset {self.symbol}>'

class MarketData(db.Model):
    __tablename__ = 'market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto_assets.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    open_price = db.Column(db.Float)
    high_price = db.Column(db.Float)
    low_price = db.Column(db.Float)
    close_price = db.Column(db.Float)
    volume = db.Column(db.Float)
    
    def __repr__(self):
        return f'<MarketData {self.crypto_id} {self.timestamp}>'

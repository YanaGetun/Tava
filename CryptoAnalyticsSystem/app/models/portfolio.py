from datetime import datetime
from app import db

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    initial_balance = db.Column(db.Float, default=0.0)
    current_balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # РЎРІСЏР·Рё
    assets = db.relationship('PortfolioAsset', backref='portfolio', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='portfolio', lazy='dynamic')
    
    def calculate_performance(self):
        if self.initial_balance == 0:
            return 0
        return ((self.current_balance - self.initial_balance) / self.initial_balance) * 100
    
    def __repr__(self):
        return f'<Portfolio {self.name}>'

class PortfolioAsset(db.Model):
    __tablename__ = 'portfolio_assets'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto_assets.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=0.0)
    average_buy_price = db.Column(db.Float)
    current_value = db.Column(db.Float)
    
    def __repr__(self):
        return f'<PortfolioAsset {self.portfolio_id}:{self.crypto_id}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'), nullable=False)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto_assets.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # buy, sell
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Transaction {self.type} {self.crypto_id} {self.quantity}>'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.portfolio import portfolio_bp
    from app.routes.predictions import predictions_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
    app.register_blueprint(predictions_bp, url_prefix='/predictions')
    
    # Create tables and add test data
    with app.app_context():
        db.create_all()
        create_test_data()
    
    return app

def create_test_data():
    """Создание тестовых данных при первом запуске"""
    from app.models.user import User
    from app.models.crypto import CryptoAsset
    
    # Проверяем, есть ли уже пользователи
    if User.query.count() == 0:
        # Создаем тестовых пользователей
        test_users = [
            {'username': 'trader', 'email': 'trader@example.com', 'role': 'trader'},
            {'username': 'analyst', 'email': 'analyst@example.com', 'role': 'analyst'},
            {'username': 'manager', 'email': 'manager@example.com', 'role': 'manager'}
        ]
        
        for user_data in test_users:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role']
            )
            user.set_password('password123')
            db.session.add(user)
        
        print("Созданы тестовые пользователи")
    
    # Проверяем, есть ли уже криптовалюты
    if CryptoAsset.query.count() == 0:
        # Создаем тестовые криптовалюты
        test_cryptos = [
            {'symbol': 'BTC', 'name': 'Bitcoin', 'current_price': 45000.0},
            {'symbol': 'ETH', 'name': 'Ethereum', 'current_price': 3000.0},
            {'symbol': 'BNB', 'name': 'Binance Coin', 'current_price': 350.0},
            {'symbol': 'XRP', 'name': 'Ripple', 'current_price': 0.75},
            {'symbol': 'ADA', 'name': 'Cardano', 'current_price': 0.45}
        ]
        
        for crypto_data in test_cryptos:
            crypto = CryptoAsset(
                symbol=crypto_data['symbol'],
                name=crypto_data['name'],
                current_price=crypto_data['current_price']
            )
            db.session.add(crypto)
        
        print("Созданы тестовые криптовалюты")
    
    # Сохраняем все изменения
    try:
        db.session.commit()
        print("Тестовые данные успешно добавлены в базу")
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при добавлении тестовых данных: {e}")
# init_db.py
# Скрипт для инициализации базы данных и создания тестовых данных

from app import create_app, db
from app.models.user import User
from app.models.crypto import CryptoAsset

def init_database():
    """Инициализация базы данных с тестовыми данными"""
    app = create_app()
    
    with app.app_context():
        # Создаем таблицы
        db.create_all()
        print("Таблицы базы данных созданы")
        
        # Создаем тестовых пользователей
        test_users = [
            {'username': 'trader', 'email': 'trader@example.com', 'role': 'trader'},
            {'username': 'analyst', 'email': 'analyst@example.com', 'role': 'analyst'},
            {'username': 'manager', 'email': 'manager@example.com', 'role': 'manager'}
        ]
        
        for user_data in test_users:
            user = User.query.filter_by(username=user_data['username']).first()
            if not user:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    role=user_data['role']
                )
                user.set_password('password123')
                db.session.add(user)
                print(f"Создан пользователь: {user_data['username']} ({user_data['role']})")
        
        # Создаем тестовые криптовалюты
        test_cryptos = [
            {'symbol': 'BTC', 'name': 'Bitcoin', 'current_price': 45000.0},
            {'symbol': 'ETH', 'name': 'Ethereum', 'current_price': 3000.0},
            {'symbol': 'BNB', 'name': 'Binance Coin', 'current_price': 350.0},
            {'symbol': 'XRP', 'name': 'Ripple', 'current_price': 0.75},
            {'symbol': 'ADA', 'name': 'Cardano', 'current_price': 0.45},
            {'symbol': 'SOL', 'name': 'Solana', 'current_price': 100.0},
            {'symbol': 'DOT', 'name': 'Polkadot', 'current_price': 7.5},
            {'symbol': 'DOGE', 'name': 'Dogecoin', 'current_price': 0.15}
        ]
        
        for crypto_data in test_cryptos:
            crypto = CryptoAsset.query.filter_by(symbol=crypto_data['symbol']).first()
            if not crypto:
                crypto = CryptoAsset(
                    symbol=crypto_data['symbol'],
                    name=crypto_data['name'],
                    current_price=crypto_data['current_price']
                )
                db.session.add(crypto)
                print(f"Добавлена криптовалюта: {crypto_data['symbol']} - {crypto_data['name']}")
        
        # Сохраняем изменения
        db.session.commit()
        print("\nБаза данных успешно инициализирована!")
        print("Тестовые пользователи:")
        print("  1. trader / password123 (Трейдер)")
        print("  2. analyst / password123 (Аналитик)")
        print("  3. manager / password123 (Управляющий)")

if __name__ == '__main__':
    init_database()
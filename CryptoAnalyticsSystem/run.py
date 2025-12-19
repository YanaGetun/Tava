from app import create_app, db
from app.models.user import User

app = create_app()

def create_test_users():
    """Создание тестовых пользователей при запуске"""
    with app.app_context():
        # Проверяем, существуют ли уже тестовые пользователи
        users_data = [
            {'username': 'trader', 'email': 'trader@example.com', 'role': 'trader'},
            {'username': 'analyst', 'email': 'analyst@example.com', 'role': 'analyst'},
            {'username': 'manager', 'email': 'manager@example.com', 'role': 'manager'}
        ]
        
        created_count = 0
        for user_data in users_data:
            user = User.query.filter_by(username=user_data['username']).first()
            if not user:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    role=user_data['role']
                )
                user.set_password('password123')  # Общий пароль для всех тестовых пользователей
                db.session.add(user)
                created_count += 1
                print(f"Создан пользователь: {user_data['username']} ({user_data['role']})")
        
        if created_count > 0:
            db.session.commit()
            print(f"Создано {created_count} тестовых пользователя")
        else:
            print("Тестовые пользователи уже существуют")

if __name__ == '__main__':
    print("=" * 60)
    print("Запуск интеллектуальной аналитической системы прогнозирования")
    print("Система включает 5 подсистем:")
    print("1. Сбор и агрегация данных")
    print("2. Хранение и обработка данных")
    print("3. Анализ и моделирование")
    print("4. Управление рисками и рекомендации")
    print("5. Пользовательский интерфейс")
    print("=" * 60)
    print()
    
    # Создаем тестовых пользователей
    create_test_users()
    
    print()
    print("Приложение доступно по адресу: http://localhost:5000")
    print("Тестовые пользователи:")
    print("  - Трейдер: trader / password123")
    print("  - Аналитик: analyst / password123")
    print("  - Управляющий: manager / password123")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
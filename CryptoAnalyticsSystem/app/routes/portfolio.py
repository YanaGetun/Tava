from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/')
@login_required
def portfolio_list():
    # Заглушка для портфелей
    portfolios = [
        {'id': 1, 'name': 'Основной портфель', 'value': 12500, 'profit': 12.5},
        {'id': 2, 'name': 'Агрессивный', 'value': 8500, 'profit': -3.2},
        {'id': 3, 'name': 'Консервативный', 'value': 22000, 'profit': 5.8}
    ]
    
    return render_template('portfolio/list.html', portfolios=portfolios)

@portfolio_bp.route('/<int:portfolio_id>')
@login_required
def portfolio_detail(portfolio_id):
    # Заглушка для активов портфеля
    assets = [
        {'symbol': 'BTC', 'amount': 0.25, 'value': 11250, 'allocation': 35},
        {'symbol': 'ETH', 'amount': 3.5, 'value': 10500, 'allocation': 33},
        {'symbol': 'BNB', 'amount': 25, 'value': 8750, 'allocation': 27},
        {'symbol': 'USDT', 'amount': 1500, 'value': 1500, 'allocation': 5}
    ]
    
    portfolio = {'id': portfolio_id, 'name': f'Портфель #{portfolio_id}', 'total_value': 32000}
    
    return render_template('portfolio/detail.html', portfolio=portfolio, assets=assets)

@portfolio_bp.route('/create', methods=['POST'])
@login_required
def create_portfolio():
    data = request.get_json()
    
    # В реальной системе здесь было бы создание портфеля в БД
    portfolio_id = 4  # Заглушка
    
    return jsonify({
        'success': True,
        'portfolio_id': portfolio_id,
        'message': 'Портфель создан успешно'
    })
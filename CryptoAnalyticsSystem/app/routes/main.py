from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app.services.data_collector import DataCollector
from app.services.prediction_service import PredictionService
from datetime import datetime, timedelta
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    collector = DataCollector()
    top_cryptos = collector.get_top_cryptos(8)
    
    return render_template('main/dashboard.html', 
                         cryptos=top_cryptos,
                         username=current_user.username,
                         role=current_user.role)

@main_bp.route('/market')
@login_required
def market():
    collector = DataCollector()
    all_cryptos = collector.get_top_cryptos(20)
    
    return render_template('main/market.html', cryptos=all_cryptos)

@main_bp.route('/api/crypto/<symbol>')
@login_required
def get_crypto_data(symbol):
    collector = DataCollector()
    service = PredictionService()
    
    # Получение данных
    data = collector.fetch_market_data(f"{symbol}-USD", period='30d', interval='1h')
    
    if data is None or data.empty:
        # Возвращаем тестовые данные, если нет реальных
        timestamps = [(datetime.now() - timedelta(hours=i)).strftime('%Y-%m-%d %H:%M') 
                     for i in range(50, 0, -1)]
        
        # Генерация тестовых цен
        base_price = 45000 if symbol == 'BTC' else 3000 if symbol == 'ETH' else 350 if symbol == 'BNB' else 0.75 if symbol == 'XRP' else 0.45 if symbol == 'ADA' else 100 if symbol == 'SOL' else 7.5 if symbol == 'DOT' else 0.15 if symbol == 'DOGE' else 100
        prices = [base_price * (1 + (random.random() - 0.5) * 0.1) for _ in range(50)]
        
        # Случайное направление с большей вероятностью роста
        direction = 'up' if random.random() > 0.4 else 'down'
        
        response = {
            'symbol': symbol,
            'current_price': float(prices[-1]),
            'prediction': {
                'predicted_price': float(prices[-1] * (1 + (random.uniform(0.02, 0.1) if direction == 'up' else random.uniform(-0.1, -0.02)))),
                'direction': direction,
                'confidence': float(random.uniform(0.6, 0.9))
            },
            'chart_data': {
                'timestamps': timestamps,
                'prices': prices,
                'volume': [random.uniform(1000000, 5000000) for _ in range(50)]
            },
            'indicators': {
                'ma7': float(sum(prices[-7:]) / 7),
                'ma25': float(sum(prices[-25:]) / 25) if len(prices) >= 25 else None,
                'rsi': float(random.uniform(30, 70))
            }
        }
    else:
        # Прогнозирование
        prediction = service.predict(symbol, data)
        
        # Расчет индикаторов
        data_with_indicators = collector.calculate_technical_indicators(data)
        
        response = {
            'symbol': symbol,
            'current_price': float(data['close'].iloc[-1]) if not data.empty else 0,
            'prediction': prediction,
            'chart_data': {
                'timestamps': data.index.strftime('%Y-%m-%d %H:%M').tolist()[-50:],
                'prices': data['close'].tolist()[-50:],
                'volume': data['volume'].tolist()[-50:]
            },
            'indicators': {
                'ma7': float(data_with_indicators['ma7'].iloc[-1]) if 'ma7' in data_with_indicators.columns else None,
                'ma25': float(data_with_indicators['ma25'].iloc[-1]) if 'ma25' in data_with_indicators.columns else None,
                'rsi': float(data_with_indicators['rsi'].iloc[-1]) if 'rsi' in data_with_indicators.columns else None
            }
        }
    
    return jsonify(response)

@main_bp.route('/crypto/<symbol>')
@login_required
def crypto_detail(symbol):
    """Детальная страница криптовалюты"""
    collector = DataCollector()
    service = PredictionService()
    
    # Получаем данные о криптовалюте
    cryptos = collector.get_top_cryptos(50)
    current_crypto = None
    for crypto in cryptos:
        if crypto['symbol'] == symbol:
            current_crypto = crypto
            break
    
    if not current_crypto:
        from flask import abort
        abort(404)
    
    # Получаем прогноз
    data = collector.fetch_market_data(f"{symbol}-USD", period='7d', interval='1h')
    prediction = None
    if data is not None and not data.empty:
        prediction = service.predict(symbol, data)
    
    return render_template('main/crypto_detail.html',
                         crypto=current_crypto,
                         prediction=prediction,
                         symbol=symbol)
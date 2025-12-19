from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from app.services.data_collector import DataCollector
from app.services.prediction_service import PredictionService
from app.services.risk_analyzer import RiskAnalyzer

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/')
@login_required
def predictions_list():
    collector = DataCollector()
    service = PredictionService()
    risk_analyzer = RiskAnalyzer()
    
    cryptos = collector.get_top_cryptos(6)
    predictions = []
    
    for crypto in cryptos:
        symbol = crypto['symbol']
        data = collector.fetch_market_data(f"{symbol}-USD", period='7d', interval='1h')
        
        if data is not None and not data.empty:
            prediction = service.predict(symbol, data)
            
            if prediction:
                # Оценка риска
                historical_prices = data['close'].tolist()
                risk_assessment = risk_analyzer.assess_prediction_risk(prediction, historical_prices)
                
                predictions.append({
                    'crypto': crypto,
                    'prediction': prediction,
                    'risk': risk_assessment
                })
    
    return render_template('predictions/list.html', predictions=predictions)

@predictions_bp.route('/api/generate')
@login_required
def generate_predictions():
    collector = DataCollector()
    service = PredictionService()
    
    symbols = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA']
    results = []
    
    for symbol in symbols:
        data = collector.fetch_market_data(f"{symbol}-USD", period='30d', interval='1d')
        
        if data is not None and not data.empty:
            prediction = service.predict(symbol, data)
            if prediction:
                results.append(prediction)
    
    return jsonify({'predictions': results, 'count': len(results)})
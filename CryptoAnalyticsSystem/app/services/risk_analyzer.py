from typing import Dict, List
import numpy as np
import logging

logger = logging.getLogger(__name__)

class RiskAnalyzer:
    """Подсистема управления рисками"""
    
    def calculate_volatility(self, prices: List[float], window: int = 30) -> float:
        """Расчет волатильности"""
        if len(prices) < 2:
            return 0.0
        
        returns = np.diff(prices) / prices[:-1]  # Это уже корректно
        if len(returns) == 0:
            return 0.0
        
        volatility = np.std(returns) * np.sqrt(365)  # Годовая волатильность
        return float(volatility)
    
    def assess_prediction_risk(self, prediction: Dict, historical_data: List[float]) -> Dict:
        """Оценка риска прогноза"""
        volatility = self.calculate_volatility(historical_data[-30:])
        
        # Определение уровня риска
        if volatility < 0.3:
            risk_level = 'low'
        elif volatility < 0.7:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        # Расчет Value at Risk (упрощенный)
        if len(historical_data) >= 100:
            historical_subset = historical_data[-100:]
            returns = np.diff(historical_subset) / historical_subset[:-1]  # Исправлено
            if len(returns) > 0:
                var_95 = np.percentile(returns, 5) * 100  # В процентах
            else:
                var_95 = volatility * 2
        else:
            var_95 = volatility * 2
        
        # Генерация рекомендаций
        recommendations = self.generate_recommendations(
            risk_level,
            prediction['direction'],
            prediction['confidence']
        )
        
        return {
            'risk_level': risk_level,
            'volatility': round(float(volatility), 4),
            'var_95': round(float(var_95), 2),
            'recommendations': recommendations
        }
    
    def generate_recommendations(self, risk_level: str, direction: str, confidence: float) -> List[str]:
        """Генерация торговых рекомендаций"""
        recommendations = []
        
        if risk_level == 'low':
            if direction == 'up' and confidence > 0.6:
                recommendations.append("Низкий риск: можно покупать")
                recommendations.append("Стоп-лосс: -3% от цены входа")
            elif direction == 'down':
                recommendations.append("Рассмотреть продажу или ожидание")
        elif risk_level == 'medium':
            recommendations.append("Средний риск: осторожно")
            if direction == 'up':
                recommendations.append("Покупать малыми порциями")
                recommendations.append("Стоп-лосс: -5% от цены входа")
            else:
                recommendations.append("Избегать покупок")
        elif risk_level == 'high':
            recommendations.append("Высокий риск: рекомендуется ожидание")
            recommendations.append("Избегать открытия позиций")
            recommendations.append("Рассмотреть хеджирование")
        
        if confidence > 0.8:
            recommendations.append("Высокая уверенность прогноза")
        elif confidence < 0.4:
            recommendations.append("Низкая уверенность: дождаться подтверждения")
        
        return recommendations
    
    def portfolio_risk_assessment(self, portfolio: Dict) -> Dict:
        """Оценка риска портфеля"""
        # В реальной системе здесь была бы сложная логика
        return {
            'total_risk': 'medium',
            'diversification_score': 65,
            'suggested_actions': [
                "Диверсифицировать в разные классы активов",
                "Рассмотреть хеджирование через стейблкоины",
                "Ребалансировать портфель ежеквартально"
            ]
        }
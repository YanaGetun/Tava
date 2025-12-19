import pandas as pd
import numpy as np
from typing import Dict, Optional
from datetime import datetime, timedelta
import logging
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

class PredictionService:
    """РџРѕРґСЃРёСЃС‚РµРјР° Р°РЅР°Р»РёР·Р° Рё РїСЂРѕРіРЅРѕР·РёСЂРѕРІР°РЅРёСЏ"""
    
    def __init__(self):
        self.models = {}
    
    def prepare_features(self, data: pd.DataFrame) -> Optional[pd.DataFrame]:
        """РџРѕРґРіРѕС‚РѕРІРєР° РїСЂРёР·РЅР°РєРѕРІ РґР»СЏ РјРѕРґРµР»Рё"""
        if data is None or len(data) < 30:
            return None
        
        df = data.copy()
        
        # РџСЂРёР·РЅР°РєРё РЅР° РѕСЃРЅРѕРІРµ С†РµРЅ
        df['returns'] = df['close'].pct_change()
        df['volatility'] = df['returns'].rolling(window=7).std()
        
        # РџСЂРёР·РЅР°РєРё РЅР° РѕСЃРЅРѕРІРµ РѕР±СЉРµРјР°
        df['volume_ma'] = df['volume'].rolling(window=7).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']
        
        # РўРµС…РЅРёС‡РµСЃРєРёРµ РёРЅРґРёРєР°С‚РѕСЂС‹
        if 'ma7' in df.columns and 'ma25' in df.columns:
            df['ma_diff'] = df['ma7'] - df['ma25']
            df['ma_signal'] = np.where(df['ma7'] > df['ma25'], 1, -1)
        
        if 'rsi' in df.columns:
            df['rsi_signal'] = np.where(df['rsi'] > 70, -1, np.where(df['rsi'] < 30, 1, 0))
        
        # Р¦РµР»РµРІР°СЏ РїРµСЂРµРјРµРЅРЅР°СЏ (С†РµРЅР° С‡РµСЂРµР· 24 С‡Р°СЃР°)
        df['target'] = df['close'].shift(-24)
        
        # РЈРґР°Р»РµРЅРёРµ NaN
        df = df.dropna()
        
        return df
    
    def train_model(self, symbol: str, data: pd.DataFrame) -> bool:
        """РћР±СѓС‡РµРЅРёРµ РјРѕРґРµР»Рё РґР»СЏ СЃРёРјРІРѕР»Р°"""
        try:
            features = self.prepare_features(data)
            if features is None or len(features) < 50:
                return False
            
            # Р Р°Р·РґРµР»РµРЅРёРµ РЅР° РїСЂРёР·РЅР°РєРё Рё С†РµР»СЊ
            X = features.drop(['target'], axis=1).select_dtypes(include=[np.number])
            y = features['target']
            
            # РњР°СЃС€С‚Р°Р±РёСЂРѕРІР°РЅРёРµ
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # РћР±СѓС‡РµРЅРёРµ РјРѕРґРµР»Рё
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            model.fit(X_scaled, y)
            
            # РЎРѕС…СЂР°РЅРµРЅРёРµ РјРѕРґРµР»Рё
            self.models[symbol] = {
                'model': model,
                'scaler': scaler,
                'features': X.columns.tolist()
            }
            
            logger.info(f"Model trained for {symbol}")
            return True
            
        except Exception as e:
            logger.error(f"Error training model for {symbol}: {str(e)}")
            return False
    
    def predict(self, symbol: str, data: pd.DataFrame) -> Optional[Dict]:
        """РџСЂРѕРіРЅРѕР·РёСЂРѕРІР°РЅРёРµ С†РµРЅС‹"""
        try:
            if symbol not in self.models:
                # Р•СЃР»Рё РјРѕРґРµР»СЊ РЅРµ РѕР±СѓС‡РµРЅР°, РёСЃРїРѕР»СЊР·СѓРµРј РїСЂРѕСЃС‚РѕР№ РјРµС‚РѕРґ
                return self.simple_prediction(data)
            
            features = self.prepare_features(data)
            if features is None:
                return self.simple_prediction(data)
            
            model_data = self.models[symbol]
            latest_features = features.iloc[-1:][model_data['features']]
            
            # РњР°СЃС€С‚Р°Р±РёСЂРѕРІР°РЅРёРµ
            X_scaled = model_data['scaler'].transform(latest_features)
            
            # РџСЂРѕРіРЅРѕР·
            predicted_price = model_data['model'].predict(X_scaled)[0]
            current_price = data['close'].iloc[-1]
            
            # РћРїСЂРµРґРµР»РµРЅРёРµ РЅР°РїСЂР°РІР»РµРЅРёСЏ
            direction = 'up' if predicted_price > current_price else 'down'
            confidence = min(0.95, abs(predicted_price - current_price) / current_price * 10)
            
            return {
                'symbol': symbol,
                'current_price': round(float(current_price), 2),
                'predicted_price': round(float(predicted_price), 2),
                'direction': direction,
                'confidence': round(float(confidence), 2),
                'model_type': 'random_forest'
            }
            
        except Exception as e:
            logger.error(f"Error predicting for {symbol}: {str(e)}")
            return self.simple_prediction(data)
    
    def simple_prediction(self, data: pd.DataFrame) -> Optional[Dict]:
        """РџСЂРѕСЃС‚РѕРµ РїСЂРѕРіРЅРѕР·РёСЂРѕРІР°РЅРёРµ РЅР° РѕСЃРЅРѕРІРµ СЃРєРѕР»СЊР·СЏС‰РёС… СЃСЂРµРґРЅРёС…"""
        if data is None or len(data) < 30:
            return None
        
        current_price = data['close'].iloc[-1]
        
        # Р Р°СЃС‡РµС‚ СЃРєРѕР»СЊР·СЏС‰РёС… СЃСЂРµРґРЅРёС…
        ma7 = data['close'].rolling(window=7).mean().iloc[-1]
        ma25 = data['close'].rolling(window=25).mean().iloc[-1]
        
        # РћРїСЂРµРґРµР»РµРЅРёРµ РЅР°РїСЂР°РІР»РµРЅРёСЏ
        if ma7 > ma25:
            direction = 'up'
            confidence = min(0.8, (ma7 - ma25) / current_price * 5)
        else:
            direction = 'down'
            confidence = min(0.8, (ma25 - ma7) / current_price * 5)
        
        # РџСЂРѕСЃС‚РѕР№ РїСЂРѕРіРЅРѕР· С†РµРЅС‹
        predicted_price = current_price * (1 + (0.01 if direction == 'up' else -0.01))
        
        return {
            'symbol': 'unknown',
            'current_price': round(float(current_price), 2),
            'predicted_price': round(float(predicted_price), 2),
            'direction': direction,
            'confidence': round(float(confidence), 2),
            'model_type': 'simple_ma'
        }

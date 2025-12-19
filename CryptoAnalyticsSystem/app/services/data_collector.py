import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class DataCollector:
    """РџРѕРґСЃРёСЃС‚РµРјР° СЃР±РѕСЂР° РґР°РЅРЅС‹С…"""
    
    def __init__(self):
        self.base_currencies = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'XRP-USD', 'ADA-USD']
    
    def fetch_market_data(self, symbol: str, period: str = '1d', interval: str = '1h') -> Optional[pd.DataFrame]:
        """РџРѕР»СѓС‡РµРЅРёРµ СЂС‹РЅРѕС‡РЅС‹С… РґР°РЅРЅС‹С…"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                logger.warning(f"No data for {symbol}")
                return None
            
            # РћС‡РёСЃС‚РєР° РґР°РЅРЅС‹С…
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            
            return data
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_top_cryptos(self, limit: int = 10) -> List[Dict]:
        """РџРѕР»СѓС‡РµРЅРёРµ СЃРїРёСЃРєР° С‚РѕРї РєСЂРёРїС‚РѕРІР°Р»СЋС‚"""
        try:
            # Р’ СЂРµР°Р»СЊРЅРѕР№ СЃРёСЃС‚РµРјРµ Р·РґРµСЃСЊ Р±С‹Р» Р±С‹ Р·Р°РїСЂРѕСЃ Рє CoinGecko РёР»Рё РґСЂСѓРіРѕРјСѓ API
            top_cryptos = [
                {'symbol': 'BTC', 'name': 'Bitcoin', 'price': 45000, 'change': 2.5},
                {'symbol': 'ETH', 'name': 'Ethereum', 'price': 3000, 'change': 1.8},
                {'symbol': 'BNB', 'name': 'Binance Coin', 'price': 350, 'change': 0.5},
                {'symbol': 'XRP', 'name': 'Ripple', 'price': 0.75, 'change': -0.3},
                {'symbol': 'ADA', 'name': 'Cardano', 'price': 0.45, 'change': 1.2},
                {'symbol': 'SOL', 'name': 'Solana', 'price': 100, 'change': 3.2},
                {'symbol': 'DOT', 'name': 'Polkadot', 'price': 7.5, 'change': 0.8},
                {'symbol': 'DOGE', 'name': 'Dogecoin', 'price': 0.15, 'change': -1.5}
            ]
            return top_cryptos[:limit]
        except Exception as e:
            logger.error(f"Error getting top cryptos: {str(e)}")
            return []
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Р Р°СЃС‡РµС‚ С‚РµС…РЅРёС‡РµСЃРєРёС… РёРЅРґРёРєР°С‚РѕСЂРѕРІ"""
        if data is None or data.empty:
            return data
        
        df = data.copy()
        
        # РЎРєРѕР»СЊР·СЏС‰РёРµ СЃСЂРµРґРЅРёРµ
        df['ma7'] = df['close'].rolling(window=7).mean()
        df['ma25'] = df['close'].rolling(window=25).mean()
        
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        return df

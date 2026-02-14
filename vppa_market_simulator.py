import random
import time
import math
from datetime import datetime, timedelta

class MarketSimulator:
    def __init__(self):
        self.base_price = 15.0  # Base market price
        self.base_generation = 0.0 # Base generation status (0 at night)
        self.time_offset = 0 # To simulate time passage if needed
        self.history = [] # Store last N data points

    def _get_solar_potential(self, hour):
        """シンプリファイドソーラー発電曲線 (6時〜18時)"""
        if 6 <= hour <= 18:
            # 12時をピークとする放物線
            # 修正: 0未満にならないようにmaxをとる
            val = 1 - ((hour - 12) / 6) ** 2
            return max(0, val)
        return 0

    def _get_market_trend(self, hour):
        """典型的なダックカーブ価格傾向"""
        if 8 <= hour <= 10 or 17 <= hour <= 20:
             return 1.5 # High demand
        elif 11 <= hour <= 14:
             return 0.5 # Solar glut (low price)
        else:
             return 1.0

    def get_current_state(self):
        now = datetime.now()
        hour = now.hour + (now.minute / 60)
        
        # 1. Solar Generation Calculation
        # Capacity 500kW * Solar Potential * Random Cloud Factor
        solar_potential = self._get_solar_potential(hour)
        cloud_factor = random.uniform(0.8, 1.0) # 80-100% clear sky
        current_gen = 500 * solar_potential * cloud_factor
        
        # 2. Market Price Calculation
        # Base * Trend * Random Volatility
        market_trend = self._get_market_trend(hour)
        volatility = random.uniform(0.9, 1.1)
        current_price = self.base_price * market_trend * volatility
        
        state = {
            "timestamp": now.strftime("%H:%M:%S"), # Short format for chart
            "generation_kwh": round(current_gen, 1),
            "market_price": round(current_price, 2)
        }
        
        # Update history (keep last 20 points)
        self.history.append(state)
        if len(self.history) > 20:
            self.history.pop(0)
            
        return state

    def get_history(self):
        return self.history

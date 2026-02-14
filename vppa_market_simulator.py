import random
import time
import math
from datetime import datetime, timedelta
from jepx_fetcher import JEPXFetcher

class MarketSimulator:
    def __init__(self):
        self.fetcher = JEPXFetcher(area="東京")
        self.base_generation = 0.0 
        self.history = [] 
        self.last_jepx_price = 15.0 # Fallback

    def _get_solar_potential(self, hour):
        """シンプリファイドソーラー発電曲線 (6時〜18時)"""
        if 6 <= hour <= 18:
            val = 1 - ((hour - 12) / 6) ** 2
            return max(0, val)
        return 0

    def get_current_state(self):
        now = datetime.now()
        hour = now.hour + (now.minute / 60)
        
        # 1. Solar Generation Calculation
        solar_potential = self._get_solar_potential(hour)
        cloud_factor = random.uniform(0.7, 1.0) 
        # Capacity 800kW (Increased for more "vibe")
        current_gen = 800 * solar_potential * cloud_factor
        
        # 2. Market Price Calculation (JEPX Integration)
        jepx_data = self.fetcher.get_latest_price()
        if jepx_data:
            render_price = jepx_data['price']
            self.last_jepx_price = render_price
        else:
            # Fallback with some volatility if JEPX fails
            render_price = self.last_jepx_price * random.uniform(0.95, 1.05)
        
        # 3. Imbalance Simulation (Target vs Actual)
        # 予定発電量に対して±5%程度の誤差
        imbalance_kwh = current_gen * random.uniform(-0.05, 0.05)
        
        state = {
            "timestamp": now.strftime("%H:%M:%S"),
            "generation_kwh": round(current_gen, 1),
            "market_price": round(render_price, 2),
            "imbalance_kwh": round(imbalance_kwh, 2)
        }
        
        # Update history (keep last 30 points for better vibes on chart)
        self.history.append(state)
        if len(self.history) > 30:
            self.history.pop(0)
            
        return state

    def get_history(self):
        return self.history


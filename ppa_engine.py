# PPA取引精算エンジン

class PPAEngine:
    def __init__(self, strike_price, service_fee, env_value_price):
        """
        :param strike_price: 固定単価 (円/kWh)
        :param service_fee: サービス料金単価 (円/kWh)
        :param env_value_price: 環境価値単価 (円/kWh)
        """
        self.strike_price = strike_price
        self.service_fee = service_fee
        self.env_price = env_value_price

    def calculate_virtual_ppa(self, kwh, market_price):
        """バーチャルPPAの差金決済計算"""
        # 1. 差金決済分 (CfD) = (固定価格 - 市場価格) × 発電量
        cfd_adjustment = (self.strike_price - market_price) * kwh
        
        # 2. サービス料 + 環境価値対価
        base_fees = (self.service_fee + self.env_price) * kwh
        
        # 3. 合計精算額
        total_to_cec = base_fees + cfd_adjustment
        
        return {
            "model": "Virtual PPA",
            "generation": f"{kwh} kWh",
            "cfd_adjustment": round(cfd_adjustment, 1),
            "total_payment": round(total_to_cec, 1)
        }

# シミュレーション実行例
engine = PPAEngine(strike_price=25.0, service_fee=1.0, env_value_price=2.0)
print(engine.calculate_virtual_ppa(kwh=1000, market_price=18.5))
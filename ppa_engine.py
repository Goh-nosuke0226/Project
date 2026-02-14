# PPA取引精算エンジン (高度化版)

class PPAEngine:
    def __init__(self, strike_price=25.0, service_fee=1.0, env_value_price=2.0, management_fee_fixed=500, tax_rate=0.10):
        """
        :param strike_price: 固定単価 (円/kWh)
        :param service_fee: サービス料金単価 (円/kWh)
        :param env_value_price: 環境価値単価 (円/kWh)
        :param management_fee_fixed: 固定管理手数料 (円)
        :param tax_rate: 消費税率 (0.10 = 10%)
        """
        self.strike_price = strike_price
        self.service_fee = service_fee
        self.env_price = env_value_price
        self.mgt_fee = management_fee_fixed
        self.tax_rate = tax_rate

    def calculate_virtual_ppa(self, kwh, market_price, imbalance_kwh=0):
        """バーチャルPPAの差金決済詳細計算"""
        
        # 1. 市場価格連動分 (CfD) = (固定価格 - 市場価格) × 発電量
        cfd_amount = (self.strike_price - market_price) * kwh
        
        # 2. サービス料 = サービス料単価 × 発電量
        service_fee_amount = self.service_fee * kwh
        
        # 3. 環境価値対価 = 環境価値単価 × 発電量
        env_value_amount = self.env_price * kwh
        
        # 4. インバランス費用 (簡略化モデル: 差分kWh × 市場価格の1.2倍と仮定)
        imbalance_cost = imbalance_kwh * market_price * 1.2
        
        # 5. 税抜合計
        subtotal = cfd_amount + service_fee_amount + env_value_amount + self.mgt_fee + imbalance_cost
        
        # 6. 消費税
        tax_amount = subtotal * self.tax_rate
        
        # 7. 税込合計
        total_payment = subtotal + tax_amount
        
        return {
            "model": "Advanced Virtual PPA",
            "generation": round(kwh, 2),
            "market_price": round(market_price, 2),
            "breakdown": {
                "cfd_amount": round(cfd_amount, 0),
                "service_fee": round(service_fee_amount, 0),
                "env_value": round(env_value_amount, 0),
                "management_fee": self.mgt_fee,
                "imbalance_cost": round(imbalance_cost, 0),
                "subtotal": round(subtotal, 0),
                "tax": round(tax_amount, 0)
            },
            "total_payment": round(total_payment, 0)
        }

if __name__ == "__main__":
    # シミュレーション実行例
    engine = PPAEngine()
    result = engine.calculate_virtual_ppa(kwh=1000, market_price=18.5, imbalance_kwh=5.5)
    import json
    print(json.dumps(result, indent=4, ensure_ascii=False))

from ppa_engine import PPAEngine
from jepx_fetcher import JEPXFetcher

# 1. エンジンの設定 (固定単価 25.0円, サービス料 1.0円, 環境価値 2.0円)
engine = PPAEngine(strike_price=25.0, service_fee=1.0, env_value_price=2.0)

# 2. 市場価格の取得
fetcher = JEPXFetcher(area="東京")
market_data = fetcher.get_latest_price()

if market_data:
    # 3. バーチャルPPAの精算計算を実行
    # 例として発電量 100kWh で計算
    result = engine.calculate_virtual(kwh=100, market_price=market_data['price'])
    
    print(f"--- PPA自動精算レポート ({market_data['timestamp']}) ---")
    print(f"市場価格: {market_data['price']} 円/kWh")
    print(f"差金決済額(CfD): {result['cfd_adjustment']} 円")
    print(f"CECへの支払総額: {result['total_payment_to_cec']} 円") #
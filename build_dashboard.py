from ppa_engine import PPAEngine
from jepx_fetcher import JEPXFetcher

def build():
    # 1. データの準備 (固定値は適宜変更してください)
    engine = PPAEngine(strike_price=25.0, service_fee=1.0, env_value_price=2.0)
    fetcher = JEPXFetcher(area="東京")
    market_data = fetcher.get_latest_price()

    if not market_data:
        print("市場価格が取得できませんでした。")
        return

    # 2. 計算実行
    gen_kwh = 1240.5
    res = engine.calculate_virtual_ppa(kwh=gen_kwh, market_price=market_data['price'])

    # 3. HTMLの読み込みと置換
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # データを流し込む
    output = content.replace("{{gen_kwh}}", f"{gen_kwh:,}")
    output = output.replace("{{market_price}}", f"{market_data['price']:.1f}")
    output = output.replace("{{total_payment}}", f"{res['total_payment']:,}")

    # 4. 書き出し
    with open("dashboard_live.html", "w", encoding="utf-8") as f:
        f.write(output)
    
    print("生成完了: dashboard_live.html を開いてください")

if __name__ == "__main__":
    build()
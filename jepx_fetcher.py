import requests
import csv
import io
import os
from datetime import datetime

class JEPXFetcher:
    def __init__(self, area="東京", cache_dir="data"):
        self.area = area
        self.cache_dir = cache_dir
        # 2025年度のスポット市場価格データURL
        self.url = "https://www.jepx.org/market/excel/spot_2025.csv"
        self.cache_path = os.path.join(self.cache_dir, "spot_2025.csv")
        
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def sync_data(self):
        """最新のCSVデータをダウンロードしてローカルに保存する"""
        try:
            print(f"Syncing JEPX data from {self.url}...")
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            response.encoding = 'shift_jis'
            
            with open(self.cache_path, "w", encoding="utf-8", newline="") as f:
                f.write(response.text)
            print(f"Data synced and saved to {self.cache_path}")
            return True
        except Exception as e:
            print(f"JEPXデータ同期エラー: {e}")
            return False

    def get_latest_price(self):
        """キャッシュまたは最新データから直近のスポット価格を取得する"""
        # 同期がまだなら一度試みる
        if not os.path.exists(self.cache_path):
            self.sync_data()

        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if not rows:
                    return None
                
                latest_row = rows[-1]
                return {
                    "timestamp": latest_row["時刻"],
                    "price": float(latest_row[self.area])
                }
        except Exception as e:
            print(f"データ読み込みエラー: {e}")
            return None

    def get_price_at(self, date_str, time_str):
        """特定の年月日・時刻の価格を取得する (date_str: YYYY/MM/DD, time_str: HH:mm)"""
        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["年月日"] == date_str and row["時刻"] == time_str:
                        return float(row[self.area])
        except Exception as e:
            print(f"特定価格検索エラー: {e}")
        return None


if __name__ == "__main__":
    fetcher = JEPXFetcher()
    # データを同期
    if fetcher.sync_data():
        latest = fetcher.get_latest_price()
        print(f"最新価格 ({latest['timestamp']}): {latest['price']} 円/kWh")

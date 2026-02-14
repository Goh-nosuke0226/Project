import requests
import csv
import io

class JEPXFetcher:
    def __init__(self, area="東京"):
        self.area = area
        # 2025年度のスポット市場価格データURL
        self.url = "https://www.jepx.org/market/excel/spot_2025.csv"

    def get_latest_price(self):
        """最新のスポット価格（エリアプライス）を取得する"""
        try:
            # JEPXのデータをダウンロード
            response = requests.get(self.url)
            response.encoding = 'shift_jis' # JEPXのCSVはShift-JIS形式
            
            # CSVを読み込む
            f = io.StringIO(response.text)
            reader = csv.DictReader(f)
            rows = list(reader)
            
            if not rows:
                return None
                
            # 一番新しい行（直近のコマ）を取得
            latest_row = rows[-1]
            return {
                "timestamp": latest_row["時刻"],
                "price": float(latest_row[self.area]) # 東京などのエリア価格
            }
        except Exception as e:
            print(f"JEPXデータ取得エラー: {e}")
            return None
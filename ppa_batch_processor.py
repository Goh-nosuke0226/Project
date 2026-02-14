import csv
import os
from ppa_engine import PPAEngine
from jepx_fetcher import JEPXFetcher

def run_batch_settlement(meter_csv_path, area="東京"):
    engine = PPAEngine()
    fetcher = JEPXFetcher(area=area)
    
    # 精算結果のリスト
    settlements = []
    
    if not os.path.exists(meter_csv_path):
        print(f"Error: Meter reading file not found at {meter_csv_path}")
        return

    print(f"--- Starting Batch PPA Settlement for {meter_csv_path} ---")
    
    with open(meter_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['date']
            time = row['time']
            gen_kwh = float(row['gen_kwh'])
            
            # 那覇等のエリアも考慮可能だが、現状は fetcher.area
            market_price = fetcher.get_price_at(date, time)
            
            if market_price is None:
                print(f"Warning: Market price not found for {date} {time}. Skipping.")
                continue
            
            # バッチ処理ではインバランスは一旦 0 と仮定（または実績値があれば代入）
            res = engine.calculate_virtual_ppa(kwh=gen_kwh, market_price=market_price, imbalance_kwh=0)
            
            settlements.append({
                "date": date,
                "time": time,
                "gen_kwh": gen_kwh,
                "market_price": market_price,
                "total_payment": res['total_payment']
            })
            
            print(f"[{date} {time}] Gen: {gen_kwh} kWh | Price: {market_price} Yen | Settlement: {res['total_payment']} Yen")

    # サマリーの計算
    total_gen = sum(s['gen_kwh'] for s in settlements)
    total_payment = sum(s['total_payment'] for s in settlements)
    
    print("\n--- SETTLEMENT SUMMARY ---")
    print(f"Total Generation: {total_gen:.1f} kWh")
    print(f"Total Settlement Amount: {total_payment:,.0f} Yen")
    print("--------------------------")

if __name__ == "__main__":
    sample_meter = os.path.join("data", "meter_readings_sample.csv")
    run_batch_settlement(sample_meter)

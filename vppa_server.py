from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from ppa_engine import PPAEngine
from vppa_market_simulator import MarketSimulator
import uvicorn
import os

app = FastAPI()

# Initialize Simulator and Engine
simulator = MarketSimulator()
# Assuming fixed PPA terms for this demo
engine = PPAEngine(strike_price=25.0, service_fee=1.0, env_value_price=2.0)

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def read_index():
    return FileResponse('vppa_dashboard.html')

@app.get("/api/status")
async def get_status():
    """
    Returns current simulated market status and PPA calculation results.
    """
    # 1. Get current simulated environment data
    state = simulator.get_current_state()
    
    # 2. Calculate PPA settlement based on this data
    # We use the simulated generation, price, and imbalance
    ppa_result = engine.calculate_virtual_ppa(
        kwh=state['generation_kwh'],
        market_price=state['market_price'],
        imbalance_kwh=state.get('imbalance_kwh', 0)
    )
    
    # 3. Combine results
    return {
        "timestamp": state['timestamp'],
        "market_price": state['market_price'],
        "gen_kwh": state['generation_kwh'],
        "imbalance_kwh": state.get('imbalance_kwh', 0),
        "ppa_result": ppa_result, # Full result with breakdown
        "history": simulator.get_history()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


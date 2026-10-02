# ⚡ SmartRescue EMS

## Smart Microgrid Energy Management System

SmartRescue EMS is a software-based Energy Management System designed
to intelligently manage power in a microgrid using solar generation,
battery storage, grid supply, and priority-based loads.

The system continuously monitors available power and automatically
manages loads to protect critical services during power shortages,
grid outages, low-battery conditions, and demand-response events.

---

## 🚀 Key Features

- ☀️ Solar power monitoring
- 🔋 Battery State of Charge (SOC) monitoring
- ⚡ Grid availability monitoring
- 🎯 Priority-based load management
- 🔌 Automatic load shedding
- 🔄 Automatic load restoration
- 🛡️ Critical-load protection
- 📉 Demand-response management
- 📊 Real-time dashboard
- 📈 Performance metrics
- 🧪 Multiple operating scenarios

---

## 🏗️ System Architecture

```text
                    SmartRescue EMS
                           │
                           ▼
                    Streamlit Dashboard
                           │
                           ▼
                    EMS Decision Engine
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
       Microgrid       Battery         Loads
       Simulator       Manager        Controller
            │
      ┌─────┼─────┐
      ▼     ▼     ▼
    Solar  Grid  Demand

## ⚙️ Main Components

| File | Purpose |                            
|------|---------|
| `app.py` | Streamlit dashboard and visualization |
| `simulator.py` | Simulates solar, grid and microgrid conditions |
| `battery.py` | Manages battery SOC, charging and discharging |
| `loads.py` | Defines microgrid loads and their priority levels |
| `controller.py` | Applies priority-based load control and load shedding |
| `demand_response.py` | Handles demand-response events and flexible loads |
| `microgrid.py` | Integrates the complete EMS system |
| `metrics.py` | Calculates system performance metrics |
| `logger.py` | Records simulation events and system activity |
| `scenarios.py` | Provides predefined microgrid operating scenarios | n


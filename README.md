# SmartRescue EMS

## Software-Based Microgrid Energy Management System

SmartRescue EMS is a software-based Energy Management System designed to simulate and manage a microgrid using solar power, battery storage, grid power, and prioritized electrical loads.

## Key Features

- Renewable energy monitoring
- Battery state-of-charge monitoring
- Priority-based load management
- Automatic load shedding
- Automatic load restoration
- Battery reserve protection
- Demand-response control
- Grid outage simulation
- Performance monitoring
- Streamlit dashboard

## Priority Levels

- P0 – Critical loads
- P1 – High-priority loads
- P2 – Medium-priority loads
- P3 – Flexible loads
- P4 – Lowest-priority loads

## Demonstration Scenarios

1. Sunny Day
2. Evening Peak
3. Cloud Event
4. Grid Outage
5. Low Battery

## Technology Stack

- Python
- Streamlit
- Pandas
- Microgrid simulation
- Rule-based EMS control

## Project Structure

```text
smartrescue_ems/
├── ems/
│   ├── app.py
│   ├── battery.py
│   ├── controller.py
│   ├── demand_response.py
│   ├── loads.py
│   ├── logger.py
│   ├── metrics.py
│   ├── microgrid.py
│   ├── scenarios.py
│   └── simulator.py
├── venv/
└── README.md
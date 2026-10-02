import streamlit as st
import pandas as pd

from microgrid import Microgrid
from scenarios import ScenarioManager


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SmartRescue EMS",
    page_icon="⚡",
    layout="wide"
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "microgrid" not in st.session_state:
    st.session_state.microgrid = Microgrid()

if "scenario_manager" not in st.session_state:
    st.session_state.scenario_manager = ScenarioManager(
        st.session_state.microgrid.simulator,
        st.session_state.microgrid.battery
    )

if "history" not in st.session_state:
    st.session_state.history = []

if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = None


microgrid = st.session_state.microgrid
scenario_manager = st.session_state.scenario_manager


# ============================================================
# TITLE
# ============================================================

st.title("⚡ SmartRescue EMS")

st.subheader(
    "Smart Microgrid Energy Management System"
)

st.write(
    "Dashboard is connected to the EMS simulation."
)

st.info(
    "SmartRescue EMS monitors solar generation, grid availability, "
    "battery state of charge and load demand. It automatically "
    "protects critical loads and manages flexible loads during "
    "power shortages and demand-response events."
)

st.success(
    "🟢 EMS Simulation Online • Automatic Power Management Active"
)


# ============================================================
# SYSTEM ARCHITECTURE
# ============================================================

st.subheader("🏛️ System Architecture")

architecture_col1, architecture_col2, architecture_col3, architecture_col4 = st.columns(4)

with architecture_col1:
    st.info("🖥️ Streamlit UI")
    st.caption("Dashboard & visualization")

with architecture_col2:
    st.info("⚙️ EMS Decision Engine")
    st.caption("Priority + control rules")

with architecture_col3:
    st.info("🔋 Microgrid Simulator")
    st.caption("Solar + battery + grid + loads")

with architecture_col4:
    st.info("📊 Event Logger")
    st.caption("Simulation events & metrics")

st.caption(
    "System Flow: Streamlit UI → EMS Decision Engine → "
    "Microgrid Simulator → Solar / Battery / Grid / Loads"
)

st.info(
    "⚡ The EMS continuously monitors the microgrid and applies "
    "priority-based control decisions to maintain reliable power "
    "for critical loads."
)


# ============================================================
# KEY FEATURES
# ============================================================

st.subheader("✨ Key Features")

feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)

with feature_col1:
    st.info("☀️ Renewable Monitoring")
    st.caption("Tracks solar power generation in real time.")

with feature_col2:
    st.info("🔋 Battery Management")
    st.caption("Maintains battery reserve and monitors SOC.")

with feature_col3:
    st.info("⚡ Priority Load Control")
    st.caption("Protects critical loads and sheds lower-priority loads.")

with feature_col4:
    st.info("📉 Demand Response")
    st.caption("Reduces flexible demand during peak periods.")

st.caption(
    "These features work together to monitor power conditions, "
    "protect critical loads, manage battery reserves and reduce "
    "flexible demand during constrained operating conditions."
)


# ============================================================
# SIMULATION SCENARIO
# ============================================================

st.subheader("🎯 Simulation Scenario")

scenarios = [
    "☀️ Sunny Day",
    "🌆 Evening Peak",
    "☁️ Cloud Event",
    "🔌 Grid Outage",
    "🔋 Low Battery"
]

scenario = st.selectbox(
    "Choose a scenario",
    scenarios
)


scenario_descriptions = {
    "☀️ Sunny Day":
        "Normal daytime operation with strong solar generation.",

    "🌆 Evening Peak":
        "Evening peak period where demand-response management is activated.",

    "☁️ Cloud Event":
        "Temporary reduction in solar generation due to cloud cover.",

    "🔌 Grid Outage":
        "Grid supply is unavailable. The EMS protects critical loads using local resources.",

    "🔋 Low Battery":
        "Battery SOC approaches the reserve limit, so lower-priority loads are shed."
}

st.caption(
    scenario_descriptions[scenario]
)


# ============================================================
# APPLY SCENARIO WHEN CHANGED
# ============================================================

if st.session_state.current_scenario != scenario:

    # Create a fresh simulation
    st.session_state.microgrid = Microgrid()

    microgrid = st.session_state.microgrid

    # Create a fresh scenario manager
    st.session_state.scenario_manager = ScenarioManager(
        microgrid.simulator,
        microgrid.battery
    )

    scenario_manager = st.session_state.scenario_manager

    # Clear previous simulation history
    st.session_state.history = []

    # Apply selected scenario
    if scenario == "☀️ Sunny Day":
        scenario_manager.sunny_day()

    elif scenario == "🌆 Evening Peak":
        scenario_manager.evening_peak()

    elif scenario == "☁️ Cloud Event":
        scenario_manager.cloud_event()

    elif scenario == "🔌 Grid Outage":
        scenario_manager.grid_outage()

    elif scenario == "🔋 Low Battery":
        scenario_manager.low_battery()

    st.session_state.current_scenario = scenario

    microgrid = st.session_state.microgrid


# ============================================================
# RESET SIMULATION
# ============================================================

if st.button("🔄 Reset Simulation"):

    st.session_state.microgrid = Microgrid()

    microgrid = st.session_state.microgrid

    st.session_state.scenario_manager = ScenarioManager(
        microgrid.simulator,
        microgrid.battery
    )

    scenario_manager = st.session_state.scenario_manager

    st.session_state.history = []

    # Re-apply selected scenario
    if scenario == "☀️ Sunny Day":
        scenario_manager.sunny_day()

    elif scenario == "🌆 Evening Peak":
        scenario_manager.evening_peak()

    elif scenario == "☁️ Cloud Event":
        scenario_manager.cloud_event()

    elif scenario == "🔌 Grid Outage":
        scenario_manager.grid_outage()

    elif scenario == "🔋 Low Battery":
        scenario_manager.low_battery()

    st.session_state.current_scenario = scenario

    st.rerun()


# ============================================================
# RUN SIMULATION
# ============================================================

if st.button("▶️ Run Simulation Step"):

    event_data = microgrid.run_step()

    st.session_state.history.append(event_data)

    st.success("Simulation step completed!")


# ============================================================
# CURRENT POWER INFORMATION
# ============================================================

st.subheader("⚡ Current Power Information")

if st.session_state.history:

    current = st.session_state.history[-1]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Time",
            current["time"]
        )

    with col2:
        st.metric(
            "Solar Power",
            f'{current["solar"]:.1f} kW'
        )

    with col3:
        st.metric(
            "Grid Power",
            f'{current["grid"]:.1f} kW'
        )

    with col4:
        st.metric(
            "Demand",
            f'{current["demand"]:.1f} kW'
        )

    with col5:
        st.metric(
            "Available Power",
            f'{current["available_power"]:.1f} kW'
        )

else:

    st.info(
        "Run a simulation step to display current power information."
    )


# ============================================================
# BATTERY & POWER STATUS
# ============================================================

st.subheader("🔋 Battery & Power Status")

battery_soc = microgrid.battery.soc

if battery_soc < 20:
    power_status = "EMERGENCY"
elif battery_soc < 35:
    power_status = "LOW BATTERY"
elif battery_soc < 60:
    power_status = "RESTRICTED"
else:
    power_status = "NORMAL"


system_status = "NORMAL"

if st.session_state.history:

    latest = st.session_state.history[-1]

    if latest["demand"] > latest["available_power"]:
        system_status = "POWER SHORTAGE"


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Battery SOC",
        f"{battery_soc:.1f}%"
    )

with col2:
    st.metric(
        "Power Status",
        power_status
    )

with col3:
    st.metric(
        "System Status",
        system_status
    )


# ============================================================
# EMS SYSTEM STATUS
# ============================================================

st.subheader("⚡ EMS System Status")

if system_status == "NORMAL":

    st.success(
        "🟢 Current System Status: NORMAL"
    )

else:

    st.warning(
        f"🟡 Current System Status: {system_status}"
    )


# ============================================================
# DETAILED BATTERY STATUS
# ============================================================

st.subheader("🔋 Detailed Battery Status")

available_energy = (
    microgrid.battery.capacity_kwh
    * microgrid.battery.soc
    / 100
)

battery_capacity = microgrid.battery.capacity_kwh

if battery_soc < 20:
    battery_mode = "EMERGENCY"
elif battery_soc < 35:
    battery_mode = "LOW BATTERY"
elif battery_soc < 60:
    battery_mode = "RESTRICTED"
else:
    battery_mode = "NORMAL"


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Battery SOC",
        f"{battery_soc:.1f}%"
    )

with col2:
    st.metric(
        "Capacity",
        f"{battery_capacity:.1f} kWh"
    )

with col3:
    st.metric(
        "Available Energy",
        f"{available_energy:.1f} kWh"
    )

with col4:
    st.metric(
        "Battery Mode",
        battery_mode
    )


# ============================================================
# LIVE POWER MONITORING
# ============================================================

st.subheader("📈 Live Power Monitoring")

if st.session_state.history:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    chart_columns = [
        "solar",
        "grid",
        "demand",
        "available_power"
    ]

    available_chart_columns = [
        column
        for column in chart_columns
        if column in history_df.columns
    ]

    if available_chart_columns:

        chart_df = history_df.set_index("time")[
            available_chart_columns
        ]

        st.line_chart(
            chart_df,
            width="stretch"
        )

else:

    st.info(
        "Run simulation steps to generate live power data."
    )


# ============================================================
# BATTERY SOC CHART
# ============================================================

st.subheader("🔋 Battery SOC Monitoring")

if st.session_state.history:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    if "battery_soc" in history_df.columns:

        battery_chart = history_df[
            ["time", "battery_soc"]
        ].set_index("time")

        st.line_chart(
            battery_chart,
            width="stretch"
        )

else:

    st.info(
        "Battery SOC history will appear after simulation steps."
    )


# ============================================================
# DEMAND RESPONSE
# ============================================================

st.subheader("📉 Demand Response")

if st.session_state.history:

    latest = st.session_state.history[-1]

    dr_active = latest.get(
        "dr_active",
        False
    )

    dr_reduction = latest.get(
        "dr_reduction_kw",
        0.0
    )

    disconnected_loads = latest.get(
        "loads_disconnected",
        []
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if dr_active:
            st.metric(
                "DR Status",
                "ACTIVE"
            )
        else:
            st.metric(
                "DR Status",
                "INACTIVE"
            )

    with col2:
        st.metric(
            "DR Reduction",
            f"{dr_reduction:.1f} kW"
        )

    with col3:
        st.metric(
            "Disconnected Loads",
            len(disconnected_loads)
        )

    if disconnected_loads:

        st.write("🔴 **Loads Disconnected**")

        for load_name in disconnected_loads:
            st.write(
                f"🔴 {load_name}"
            )

    else:

        st.write(
            "No loads disconnected."
        )

else:

    st.info(
        "Run a simulation step to view demand-response status."
    )


# ============================================================
# LOAD PRIORITY & STATUS
# ============================================================

st.subheader("🔌 Load Priority & Status")

load_data = []

for load in microgrid.loads:

    load_data.append(
        {
            "Load": load.name,
            "Power (kW)": load.power,
            "Priority": f"P{load.priority}",
            "Status": "🟢 ON" if load.is_on else "🔴 OFF"
        }
    )

load_df = pd.DataFrame(load_data)

st.dataframe(
    load_df,
    width="stretch",
    hide_index=True
)


# ============================================================
# PERFORMANCE METRICS
# ============================================================

st.subheader("📊 Performance Metrics")

metrics = microgrid.metrics.get_metrics()

critical_load_reliability = metrics.get(
    "critical_load_reliability",
    0.0
)

shedding_events = metrics.get(
    "shedding_events",
    0
)

renewable_utilisation = metrics.get(
    "renewable_utilisation",
    0.0
)

unserved_energy = metrics.get(
    "unserved_energy",
    0.0
)


# History-based metrics

if st.session_state.history:

    history_df = pd.DataFrame(
        st.session_state.history
    )

    average_battery_soc = history_df[
        "battery_soc"
    ].mean()

    peak_demand = history_df[
        "demand"
    ].max()

    peak_available_power = history_df[
        "available_power"
    ].max()

    peak_reduction = history_df[
        "dr_reduction_kw"
    ].max()

    simulation_steps = len(
        st.session_state.history
    )

else:

    average_battery_soc = 0.0
    peak_demand = 0.0
    peak_available_power = 0.0
    peak_reduction = 0.0
    simulation_steps = 0


metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:

    st.metric(
        "Critical Load Reliability",
        f"{critical_load_reliability:.1f}%"
    )

    st.metric(
        "Shedding Events",
        shedding_events
    )

    st.metric(
        "Simulation Steps",
        simulation_steps
    )


with metric_col2:

    st.metric(
        "Peak Reduction",
        f"{peak_reduction:.1f} kW"
    )

    st.metric(
        "Unserved Energy",
        f"{unserved_energy:.2f} kWh"
    )

    st.metric(
        "Peak Demand",
        f"{peak_demand:.2f} kW"
    )


with metric_col3:

    st.metric(
        "Renewable Utilisation",
        f"{renewable_utilisation:.1f}%"
    )

    st.metric(
        "Average Battery SOC",
        f"{average_battery_soc:.1f}%"
    )

    st.metric(
        "Peak Available Power",
        f"{peak_available_power:.2f} kW"
    )


# ============================================================
# HOW SMARTRESCUE EMS WORKS
# ============================================================

st.subheader("⚙️ How SmartRescue EMS Works")

st.write(
    "SmartRescue EMS continuously monitors the microgrid "
    "and makes automatic power-management decisions."
)


st.markdown("### 1️⃣ Monitor")

st.write("The system monitors:")

st.markdown(
    """
    - ☀️ Solar generation
    - 🔌 Grid availability
    - 🔋 Battery state of charge
    - ⚡ Load demand
    """
)


st.markdown("### 2️⃣ Analyze")

st.write(
    "The EMS evaluates available power, battery condition "
    "and load priorities."
)


st.markdown(
    """
    - Critical loads are protected.
    - Lower-priority loads can be disconnected.
    - Battery reserve is maintained.
    - Flexible loads can participate in demand response.
    """
)


st.markdown("### 3️⃣ Control")

st.write(
    "The EMS automatically applies control actions "
    "according to the operating condition."
)


st.markdown(
    """
    - 🔋 Battery-aware power management
    - 🔌 Priority-based load shedding
    - 📉 Demand-response control
    - 🔄 Load restoration when conditions improve
    """
)


st.markdown("### 4️⃣ Measure")

st.write(
    "The system records simulation events and calculates "
    "performance metrics."
)


st.markdown(
    """
    - Critical-load reliability
    - Renewable utilisation
    - Shedding events
    - Unserved energy
    - Peak demand
    """
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "SmartRescue EMS • Smart Microgrid Energy Management System"
)

st.caption(
    "Software simulation prototype for intelligent microgrid power management."
)
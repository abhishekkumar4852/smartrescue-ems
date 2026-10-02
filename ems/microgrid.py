from simulator import MicrogridSimulator
from loads import Load
from battery import Battery
from controller import EMSController
from demand_response import DemandResponseEvent
from logger import EventLogger
from metrics import PerformanceMetrics


class Microgrid:

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        # -------------------------------------------------
        # SIMULATOR
        # -------------------------------------------------

        self.simulator = MicrogridSimulator()

        # -------------------------------------------------
        # BATTERY
        # -------------------------------------------------

        self.battery = Battery(
            capacity_kwh=50.0,
            soc=80.0,
            min_soc=20.0,
            max_charge_kw=10.0,
            max_discharge_kw=10.0
        )

        # -------------------------------------------------
        # LOADS
        # -------------------------------------------------

        self.loads = [

            Load(
                "Emergency Medical Equipment",
                2.0,
                0
            ),

            Load(
                "Communication System",
                0.5,
                0
            ),

            Load(
                "Water Pump",
                4.0,
                1
            ),

            Load(
                "Vaccine Refrigerator",
                1.0,
                1
            ),

            Load(
                "School/Commercial Lighting",
                3.0,
                2
            ),

            Load(
                "Rice Mill/Workshop",
                8.0,
                2
            ),

            Load(
                "EV Charging",
                5.0,
                3
            ),

            Load(
                "Water Heater",
                3.0,
                3
            ),

            Load(
                "Decorative Lighting",
                1.0,
                4
            )
        ]

        # -------------------------------------------------
        # EMS CONTROLLER
        # -------------------------------------------------

        self.controller = EMSController(
            available_power=0.0,
            battery=self.battery,
            loads=self.loads
        )

        # -------------------------------------------------
        # DEMAND RESPONSE EVENT
        # -------------------------------------------------

        self.dr_event = DemandResponseEvent(
            name="Evening Peak Reduction",
            start_hour=18,
            duration_hours=1,
            required_reduction_kw=10.0
        )

        # -------------------------------------------------
        # LOGGER
        # -------------------------------------------------

        self.logger = EventLogger()

        # -------------------------------------------------
        # PERFORMANCE METRICS
        # -------------------------------------------------

        self.metrics = PerformanceMetrics()

    # =====================================================
    # TOTAL DEMAND
    # =====================================================

    def total_demand(self):

        return sum(
            load.power
            for load in self.loads
            if load.is_on
        )

    # =====================================================
    # APPLY DEMAND RESPONSE
    # =====================================================

    def apply_demand_response(self, current_hour):

        if self.dr_event.is_active(current_hour):

            if not self.dr_event.active:

                self.dr_event.start()

                # -----------------------------------------
                # DISCONNECT FLEXIBLE LOADS
                # -----------------------------------------

                for load in self.loads:

                    if load.priority >= 3 and load.is_on:

                        load.turn_off()

                        self.dr_event.loads_disconnected.append(
                            load.name
                        )

                        self.dr_event.actual_reduction_kw += (
                            load.power
                        )

                        if (
                            self.dr_event.actual_reduction_kw
                            >= self.dr_event.required_reduction_kw
                        ):
                            break

            return True

        else:

            if self.dr_event.active:

                self.dr_event.stop()

                # -----------------------------------------
                # RESTORE DR LOADS
                # -----------------------------------------

                for load in self.loads:

                    if (
                        load.name
                        in self.dr_event.loads_disconnected
                    ):
                        load.turn_on()

            return False

    # =====================================================
    # LOAD SHEDDING
    # =====================================================

    def shed_loads(self, available_power):

        # Lower-priority loads are shed first.
        # P0 critical loads are never shed.

        priorities = [4, 3, 2, 1]

        for priority in priorities:

            for load in self.loads:

                if (
                    load.priority == priority
                    and load.is_on
                ):

                    if self.total_demand() <= available_power:
                        return

                    load.turn_off()

    # =====================================================
    # LOAD RESTORATION
    # =====================================================

    def restore_loads(self, available_power):

        # Restore higher-priority loads first.

        priorities = [1, 2, 3, 4]

        for priority in priorities:

            for load in self.loads:

                if (
                    load.priority == priority
                    and not load.is_on
                ):

                    # Don't restore a load that is still
                    # disconnected by demand response.

                    if (
                        self.dr_event.active
                        and load.name
                        in self.dr_event.loads_disconnected
                    ):
                        continue

                    new_demand = (
                        self.total_demand()
                        + load.power
                    )

                    if new_demand <= available_power:

                        load.turn_on()

    # =====================================================
    # RUN ONE SIMULATION STEP
    # =====================================================

    def run_step(self):

        # -------------------------------------------------
        # GET SIMULATOR DATA
        # -------------------------------------------------

        data = self.simulator.step()

        solar = data["solar"]

        grid_power = self.simulator.get_grid_power()

        demand = self.total_demand()

        # -------------------------------------------------
        # DEMAND RESPONSE
        # -------------------------------------------------

        current_hour = (
            self.simulator.time - 1
        ) % 24

        self.apply_demand_response(
            current_hour
        )

        # Recalculate demand after DR
        demand = self.total_demand()

        # -------------------------------------------------
        # AVAILABLE POWER
        # -------------------------------------------------

        available_power = (
            solar
            + grid_power
        )

        # -------------------------------------------------
        # BATTERY SUPPORT
        # -------------------------------------------------

        if available_power < demand:

            deficit = (
                demand
                - available_power
            )

            if self.battery.soc > self.battery.min_soc:

                discharge_power = min(
                    deficit,
                    self.battery.max_discharge_kw
                )

                discharged_energy = (
                    self.battery.discharge(
                        discharge_power,
                        hours=1
                    )
                )

                available_power += (
                    discharged_energy
                )

        # -------------------------------------------------
        # LOAD SHEDDING
        # -------------------------------------------------

        demand_before_shedding = (
            self.total_demand()
        )

        if available_power < demand_before_shedding:

            self.shed_loads(
                available_power
            )

        # -------------------------------------------------
        # LOAD RESTORATION
        # -------------------------------------------------

        elif available_power > self.total_demand():

            self.restore_loads(
                available_power
            )

        # -------------------------------------------------
        # FINAL DEMAND
        # -------------------------------------------------

        final_demand = self.total_demand()

        # -------------------------------------------------
        # CHECK SHEDDING
        # -------------------------------------------------

        shedding_occurred = (
            final_demand
            < demand_before_shedding
        )

        # -------------------------------------------------
        # CRITICAL LOAD STATUS
        # -------------------------------------------------

        critical_load_served = all(
            load.is_on
            for load in self.loads
            if load.priority == 0
        )

        # -------------------------------------------------
        # UPDATE PERFORMANCE METRICS
        # -------------------------------------------------

        self.metrics.record_step(
            demand=demand_before_shedding,
            solar=solar,
            final_demand=final_demand,
            available_power=available_power,
            shedding_occurred=shedding_occurred,
            critical_load_served=critical_load_served
        )

        # -------------------------------------------------
        # EVENT DATA
        # -------------------------------------------------

        event_data = {

            "time": self.simulator.time,

            "solar": round(
                solar,
                2
            ),

            "grid": round(
                grid_power,
                2
            ),

            "demand": round(
                final_demand,
                2
            ),

            "available_power": round(
                available_power,
                2
            ),

            "battery_soc": round(
                self.battery.soc,
                2
            ),

            "dr_active": self.dr_event.active,

            "dr_reduction_kw": round(
                self.dr_event.actual_reduction_kw,
                2
            ),

            "loads_disconnected":
                self.dr_event.loads_disconnected.copy()
        }

        # -------------------------------------------------
        # LOG EVENT
        # -------------------------------------------------

        self.logger.log(
            event_data
        )

        # -------------------------------------------------
        # RETURN EVENT DATA
        # -------------------------------------------------

        return event_data


# =========================================================
# MAIN PROGRAM
# =========================================================

if __name__ == "__main__":

    microgrid = Microgrid()

    for _ in range(24):

        event = microgrid.run_step()

        print(event)

    print(
        "\n=============================="
    )

    print(
        "FINAL PERFORMANCE METRICS"
    )

    print(
        "=============================="
    )

    print(
        microgrid.metrics.get_metrics()
    )
class PerformanceMetrics:

    def __init__(self):

        self.total_steps = 0
        self.shedding_events = 0
        self.total_unserved_energy = 0.0
        self.critical_load_failures = 0

        self.total_demand = 0.0
        self.total_solar = 0.0


    # =====================================================
    # RECORD ONE SIMULATION STEP
    # =====================================================

    def record_step(
        self,
        demand,
        solar,
        final_demand,
        available_power=None,
        shedding_occurred=False,
        critical_load_served=True
    ):

        self.total_steps += 1

        self.total_demand += demand

        self.total_solar += solar


        # -------------------------------------------------
        # SHEDDING EVENTS
        # -------------------------------------------------

        if shedding_occurred:

            self.shedding_events += 1


        # -------------------------------------------------
        # ACTUAL UNSERVED ENERGY
        # -------------------------------------------------
        #
        # Intentional load shedding is NOT automatically
        # counted as unserved energy.
        #
        # Unserved energy occurs only when the final demand
        # is greater than the power actually available.
        #
        # Each simulation step represents 1 hour, so:
        # kW of unmet demand × 1 hour = kWh.
        # -------------------------------------------------

        if available_power is not None:

            unmet_power = max(
                0.0,
                final_demand - available_power
            )

            self.total_unserved_energy += (
                unmet_power
            )

        else:

            # Backward-compatible fallback
            # if available_power is not supplied.

            self.total_unserved_energy += 0.0


        # -------------------------------------------------
        # CRITICAL LOAD FAILURE
        # -------------------------------------------------

        if not critical_load_served:

            self.critical_load_failures += 1


    # =====================================================
    # GET PERFORMANCE METRICS
    # =====================================================

    def get_metrics(self):

        # -------------------------------------------------
        # RENEWABLE UTILISATION
        # -------------------------------------------------

        if self.total_demand > 0:

            renewable_utilisation = (
                self.total_solar
                / self.total_demand
            ) * 100

        else:

            renewable_utilisation = 0.0


        # -------------------------------------------------
        # CRITICAL LOAD RELIABILITY
        # -------------------------------------------------

        if self.total_steps > 0:

            critical_reliability = (
                1
                - (
                    self.critical_load_failures
                    / self.total_steps
                )
            ) * 100

        else:

            critical_reliability = 100.0


        # -------------------------------------------------
        # RETURN METRICS
        # -------------------------------------------------

        return {

            "critical_load_reliability": round(
                critical_reliability,
                2
            ),

            "shedding_events": (
                self.shedding_events
            ),

            "renewable_utilisation": round(
                renewable_utilisation,
                2
            ),

            "unserved_energy": round(
                self.total_unserved_energy,
                2
            )
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    metrics = PerformanceMetrics()


    metrics.record_step(
        demand=10.0,
        solar=5.0,
        final_demand=10.0,
        available_power=10.0
    )


    metrics.record_step(
        demand=15.0,
        solar=3.0,
        final_demand=12.0,
        available_power=12.0,
        shedding_occurred=True
    )


    print(
        metrics.get_metrics()
    )
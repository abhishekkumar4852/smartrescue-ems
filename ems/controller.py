from loads import create_loads
from battery import Battery


class EMSController:

    def __init__(self, available_power, battery, loads=None):
        self.available_power = available_power
        self.battery = battery
        self.loads = loads if loads is not None else create_loads()

    def total_demand(self):

        total = 0

        for load in self.loads:

            if load.is_on:
                total += load.power

        return total

    def shed_loads(self):

        demand = self.total_demand()

        print("Available power:", self.available_power, "kW")
        print("Initial demand:", demand, "kW")
        print("Battery SOC:", self.battery.soc, "%")

        # Lowest priority first:
        # P4 -> P3 -> P2 -> P1 -> P0

        sorted_loads = sorted(
            self.loads,
            key=lambda load: load.priority,
            reverse=True
        )

        for load in sorted_loads:

            if demand <= self.available_power:
                break

            # P0 must never be shed
            if load.priority == 0:
                continue

            if load.is_on:

                load.turn_off()

                demand -= load.power

                print(
                    "Shed:",
                    load.name,
                    "| Priority:", load.priority,
                    "| Power:", load.power, "kW"
                )

        print("Final demand:", demand, "kW")

    def apply_battery_policy(self):

        print("\nApplying battery policy...")

        # Very low battery
        if self.battery.soc < 20:

            print("EMERGENCY MODE")

            for load in self.loads:

                if load.priority >= 1:
                    load.turn_off()

        # Low battery
        elif self.battery.soc < 35:

            print("LOW BATTERY MODE")

            for load in self.loads:

                if load.priority >= 3:
                    load.turn_off()

        # Moderate battery
        elif self.battery.soc < 60:

            print("BATTERY CONSERVATION MODE")

            for load in self.loads:

                if load.priority >= 4:
                    load.turn_off()

        else:

            print("NORMAL BATTERY MODE")

    def show_status(self):

        print("\nLOAD STATUS")

        for load in self.loads:

            status = "ON" if load.is_on else "OFF"

            print(
                load.name,
                "|",
                load.power,
                "kW | P" + str(load.priority),
                "|",
                status
            )


if __name__ == "__main__":

    # Create battery
    battery = Battery(
        capacity_kwh=50.0,
        soc=30.0
    )

    # Create EMS
    controller = EMSController(
        available_power=10,
        battery=battery
    )

    # Apply battery rules
    controller.apply_battery_policy()

    # Handle power shortage
    controller.shed_loads()

    # Show final status
    controller.show_status()
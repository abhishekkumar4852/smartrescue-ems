class Battery:

    def __init__(
        self,
        capacity_kwh=50.0,
        soc=80.0,
        min_soc=20.0,
        max_charge_kw=10.0,
        max_discharge_kw=10.0
    ):
        self.capacity_kwh = capacity_kwh
        self.soc = soc
        self.min_soc = min_soc
        self.max_charge_kw = max_charge_kw
        self.max_discharge_kw = max_discharge_kw

    def available_energy(self):
        return (self.soc / 100) * self.capacity_kwh

    def available_discharge_energy(self):

        minimum_energy = (
            self.min_soc / 100
        ) * self.capacity_kwh

        return max(
            0,
            self.available_energy() - minimum_energy
        )

    def charge(self, power_kw, hours=1):

        power_kw = min(
            power_kw,
            self.max_charge_kw
        )

        energy_added = power_kw * hours

        new_energy = min(
            self.capacity_kwh,
            self.available_energy() + energy_added
        )

        self.soc = (
            new_energy / self.capacity_kwh
        ) * 100

        return power_kw

    def discharge(self, power_kw, hours=1):

        power_kw = min(
            power_kw,
            self.max_discharge_kw
        )

        available_energy = (
            self.available_discharge_energy()
        )

        energy_used = min(
            power_kw * hours,
            available_energy
        )

        new_energy = (
            self.available_energy()
            - energy_used
        )

        self.soc = (
            new_energy / self.capacity_kwh
        ) * 100

        return energy_used / hours

    def get_mode(self):
        """
        Determines the intelligent battery operating mode
        based on the current state of charge.
        """

        if self.soc >= 60:
            return "NORMAL"

        elif self.soc >= 35:
            return "CONSERVATION"

        elif self.soc >= 20:
            return "RESTRICTED"

        else:
            return "EMERGENCY"

    def get_recommendation(self):
        """
        Returns the recommended EMS action
        based on battery SOC.
        """

        mode = self.get_mode()

        if mode == "NORMAL":
            return "Battery available for normal operation."

        elif mode == "CONSERVATION":
            return "Reduce unnecessary battery discharge."

        elif mode == "RESTRICTED":
            return "Protect battery by disconnecting flexible loads."

        else:
            return "Emergency mode: protect battery reserve and critical loads."

    def status(self):

        return {
            "capacity_kwh": self.capacity_kwh,
            "soc_percent": round(self.soc, 2),
            "energy_kwh": round(
                self.available_energy(),
                2
            ),
            "battery_mode": self.get_mode(),
            "recommendation": self.get_recommendation()
        }


if __name__ == "__main__":

    battery = Battery()

    print("Initial:", battery.status())

    battery.discharge(10)

    print(
        "After 1 hour at 10 kW:",
        battery.status()
    )

    battery.charge(5)

    print(
        "After 1 hour at 5 kW:",
        battery.status()
    )

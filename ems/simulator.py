class MicrogridSimulator:

    def __init__(self):

        # --------------------------------------------------
        # SIMULATION STATE
        # --------------------------------------------------

        self.time = 0

        self.battery_capacity = 50.0

        self.battery_soc = 80.0

        self.grid_available = True

        self.cloud_event = False


    # --------------------------------------------------
    # SOLAR POWER
    # --------------------------------------------------

    def get_solar_power(self):

        hour = self.time % 24

        # No solar during night

        if hour < 6 or hour >= 18:

            return 0.0


        # Normal daytime solar production

        solar_power = 15.0


        # Cloud event reduces solar production

        if self.cloud_event:

            solar_power = 5.0


        return solar_power


    # --------------------------------------------------
    # GRID POWER
    # --------------------------------------------------

    def get_grid_power(self):

        hour = self.time % 24


        # Grid unavailable during evening peak

        if 18 <= hour < 21:

            return 0.0


        # Grid outage

        if not self.grid_available:

            return 0.0


        # Normal grid supply

        return 10.0


    # --------------------------------------------------
    # BATTERY MODE
    # --------------------------------------------------

    def get_battery_mode(self):

        soc = self.battery_soc


        if soc >= 60:

            return "NORMAL"


        elif soc >= 35:

            return "RESTRICTED"


        elif soc >= 20:

            return "CRITICAL"


        else:

            return "EMERGENCY"


    # --------------------------------------------------
    # SIMULATION STEP
    # --------------------------------------------------

    def step(self):

        # Move simulation forward by one hour

        self.time += 1


        # Get current power values

        solar = self.get_solar_power()

        grid = self.get_grid_power()


        # Get battery operating mode

        battery_mode = self.get_battery_mode()


        # Return simulation data

        return {

            "time": self.time,

            "solar": solar,

            "grid": grid,

            "battery_soc": self.battery_soc,

            "battery_mode": battery_mode,

            "grid_available": self.grid_available

        }


    # --------------------------------------------------
    # RESET SIMULATION
    # --------------------------------------------------

    def reset(self):

        self.time = 0

        self.battery_soc = 80.0

        self.grid_available = True

        self.cloud_event = False
class ScenarioManager:

    def __init__(self, simulator, battery):

        self.simulator = simulator
        self.battery = battery


    def sunny_day(self):

        self.simulator.time = 12
        self.simulator.grid_available = True
        self.simulator.cloud_event = False


    def evening_peak(self):

        self.simulator.time = 18
        self.simulator.grid_available = True
        self.simulator.cloud_event = False


    def cloud_event(self):

        self.simulator.time = 14
        self.simulator.grid_available = True
        self.simulator.cloud_event = True


    def grid_outage(self):

        self.simulator.time = 19
        self.simulator.grid_available = False
        self.simulator.cloud_event = False


    def low_battery(self):

        self.simulator.time = 20
        self.simulator.grid_available = True
        self.simulator.cloud_event = False

        self.battery.soc = 25.0
class EventLogger:

    def __init__(self):
        self.events = []

    def log(self, data):
        self.events.append(data)

    def get_events(self):
        return self.events

    def clear(self):
        self.events = []

    def show_last(self):
        if self.events:
            print(self.events[-1])
        else:
            print("No events logged.")


if __name__ == "__main__":

    logger = EventLogger()
    logger.log({
        "time" : 18,
        "solar": 5.18,
        "grid": 10.00,
        "demand":7.5,
        "battery_soc": 100.8,
        "dr_active":True
    })

    logger.show_last()
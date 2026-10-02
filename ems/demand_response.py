class DemandResponseEvent:

    def __init__(
        self,
        name,
        start_hour,
        duration_hours,
        required_reduction_kw
    ):

        self.name = name
        self.start_hour = start_hour
        self.duration_hours = duration_hours
        self.required_reduction_kw = required_reduction_kw

        self.active = False
        self.actual_reduction_kw = 0.0
        self.loads_disconnected = []

    def is_active(self, current_hour):

        end_hour = (
            self.start_hour
            + self.duration_hours
        )

        return (
            self.start_hour
            <= current_hour
            < end_hour
        )

    def start(self):

        self.active = True
        self.actual_reduction_kw = 0.0
        self.loads_disconnected = []

    def stop(self):

        self.active = False

    def status(self):

        return {
            "name": self.name,
            "active": self.active,
            "required_reduction_kw":
                self.required_reduction_kw,
            "actual_reduction_kw":
                self.actual_reduction_kw,
            "loads_disconnected":
                self.loads_disconnected
        }


if __name__ == "__main__":

    event = DemandResponseEvent(
        name="Evening Peak Reduction",
        start_hour=18,
        duration_hours=1,
        required_reduction_kw=10.0
    )

    print(event.status())

    print(
        "18:00 active:",
        event.is_active(18)
    )

    print(
        "19:00 active:",
        event.is_active(19)
    )

    print(
        "20:00 active:",
        event.is_active(20)
    )
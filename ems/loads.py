class Load:
    def __init__(self , name , power , priority):
        self.name = name 
        self.power = power
        self.priority = priority
        self.is_on = True

    def turn_off(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def get_status(self):
        return {
            "name": self.name,
            "power": self.power,
            "priority":self.priority,
            "is_on":self.is_on
        }

def create_loads():
    loads = [
        Load(
            
            "Emergency Medical Equipment",
            2.0,
            0
        ),
        Load (
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
            "Rice Mill/ Workshop",
            8.0,
            2
        ),
        Load(
            "EV Charging",
            5.0,
            3
        ),
        Load(
            "Water Heating",
            3.0,
            3
        ),
        Load(
            "Decorative Lighting",
            1.0,
            4
        ),
        Load(
            "Communication System",
            0.5,
            0
        )

            
         
    ]

    return loads
if __name__ == "__main__":

    loads = create_loads()

    for load in loads:
        print(load.get_status())

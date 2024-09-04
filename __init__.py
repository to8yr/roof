class Rect_building:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height

class Duopitch:
    def __init__(self, building, bay_size, beam_type, pitch, build_method):
        self.building = building
        self.span = building.width
        self.length = building.length
        self.bay_size = bay_size
        self.beam = beam_type
        self.pitch = pitch
        self.method = build_method

    def structural_integrity(self):
        # Calculations to determine structural soundness
        area = self.span * self.length 
        return area

    def parts_list(self):
        parts = [['LFX0001', 4*6],
                 ['LVS0001', 4]]
        # Logic to determine required parts based on variables
        return parts
    

my_building = Rect_building(20, 40, 3)
my_roof = Duopitch(my_building, 2.5, "LV78", 18, "Hand")
integrity = my_roof.structural_integrity()
parts = my_roof.parts_list()
print(integrity)
print(parts)
import math

class Duopitch:
    def __init__(self, lhs, rhs, length, bay_size, beam_type, pitch, build_method):
        self.lhs = lhs + 0.5
        self.rhs = rhs + 0.5
        self.length = length
        self.bay_size = bay_size
        self.beam = beam_type
        self.pitch = pitch
        self.method = build_method
        self.span = math.cos(math.radians(self.pitch)) * (self.lhs + self.rhs)

    def structural_integrity(self):
        # Calculations to determine structural soundness
        area = self.span * self.length 
        return area

    def parts_list(self):
        parts = [['LFX0001', 4*6],
                 ['LVS0001', 4]]
        # Logic to determine required parts based on variables
        return parts


my_roof = Duopitch(10, 10, 40, 2.5, "LV78", 18, "Hand")
integrity = my_roof.structural_integrity()
parts = my_roof.parts_list()
print(integrity)
print(parts)
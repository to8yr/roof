import math
from parts import *

class Duopitch:
    def __init__(self, lhs:int, rhs:int, length:float, bay_size:float, pitch:int, beam_type:str):
        self.lhs = lhs
        self.rhs = rhs
        self.length = length
        self.bay_size = bay_size
        self.beam = beam_type
        self.pitch = pitch
        self.span = math.cos(math.radians(self.pitch)) * (self.lhs + self.rhs)

    def structural_integrity(self):
        # Calculations to determine structural soundness
        area = self.span * self.length 
        return area

    def parts_list(self, build_method:str):
        beamline = duo_beamline(self.lhs, self.rhs, self.pitch, self.beam)
        bay = duo_bay(self.lhs, self.rhs, self.beam, self.bay_size)

        parts = np.row_stack((beamline, bay))

        return parts


my_roof = Duopitch(10, 10, 40, 2572, 18, "78cm")
integrity = my_roof.structural_integrity()
parts = my_roof.parts_list("Hand")
print(parts)
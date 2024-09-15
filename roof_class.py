import math

class reg_duo:
    # initalise regular duoputch
    def __init__(self, lhs=10, rhs=10, length=40, bay_size=2.5, pitch=18, beam_type='D78'):
        self.lhs, self.rhs, self.length = lhs, rhs, length
        self.bay_size, self.pitch, self.beam_type = bay_size, pitch, beam_type
        self.span = math.cos(math.radians(self.pitch)) * (self.lhs + self.rhs)
    
    def integrity(self, weight, wind, snow):
        self.wind = wind
        self.snow = snow
        return weight * wind * snow
    
    def parts(self, build):
        self.build = build
        ...
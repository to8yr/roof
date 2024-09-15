import math
from parts import *


# Regular duopitch with consistant baysizes with number of bays calculated from length parameter
class reg_duo:
    def __init__(self, lhs=10, rhs=10, length=40, bay_size=2.5, pitch=18, beam_type='D78'):
        self.lhs, self.rhs, self.length = lhs, rhs, length
        self.bay_size, self.pitch, self.beam_type = bay_size, pitch, beam_type
        self.span = math.cos(math.radians(self.pitch)) * (self.lhs + self.rhs)
    
    def integrity(self, weight, wind, snow):
        self.wind = wind
        self.snow = snow
        return weight * wind * snow
    
    # Generated parts list and returns dataframe col=[Code, qty]
    def parts_list(self, build='hand'):
        self.build = build
        self.parts = beam_pd(self.beam_type, self.lhs)
        
        return self.parts


roof = reg_duo(lhs=20).parts_list()
print(roof)



# Irregular duopitch with inconsistant baysizes and staggers based on lists of lhs, rhs, bay_size
class irr_duo:
    def __init__(self, lhs=[10, 10, 10, 10], rhs=[10, 10, 10, 10], bay_sizes=[2.5, 2.5, 2.5], pitch=18, beam_type='D78'):
        self.lhs, self.rhs, self.bay_size = lhs, rhs, bay_sizes
        self.pitch, self.beam_type = pitch, beam_type
        self.span = []
        for i in self.lhs:
            self.span.append(math.cos(math.radians(self.pitch)) * (self.lhs[i] + self.rhs[i]))
    
    def integrity(self, weight, wind, snow):
        self.wind = wind
        self.snow = snow
        return weight * wind * snow
    
    def parts(self, build):
        self.build = build
        ...        

# Regular monopitch with consistant baysizes with number of bays calculated from length parameter
class reg_mon:
    ...
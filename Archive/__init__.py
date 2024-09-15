import math
from Archive.mparts import *

class Reg_duo:
    def __init__(self, lhs:int, rhs:int, length:float, bay_size:float, pitch:int, beam_type:str, build_method:str):
        self.lhs = lhs
        self.rhs = rhs
        self.length = length
        self.bay_size = bay_size
        self.beam = beam_type
        self.pitch = pitch
        self.span = math.cos(math.radians(self.pitch)) * (self.lhs + self.rhs)
        self.build_method = build_method

    def structural_integrity(self):
        # Calculations to determine structural soundness
        area = self.span * self.length 
        return area

    def parts_list(self):

        # Create empty parts dataframe from parts.csv
        parts = Parts().read_csv('parts.csv')

        # Retreive individual parts dataframes
        beamline = duo_beamline(self.lhs, self.rhs, self.pitch, self.beam)
        braced_bay = ...
        infill_bay = ...
        support = ...
        tiebar = ...
        df = [beamline, braced_bay, infill_bay, support, tiebar]

        # Calculate number of each
        beamline_ = math.ceil(self.length / self.bay_size)
        bay_ = beamline_ - 1
        if self.build_method == 'hand':
            braced_bay_ = math.ceil((bay_-1) / 5 + 1)
        else:
            braced_bay_ = math.ceil((bay_-1) / 2 + (1 if bay_ % 2 == 1 else 0))
        infill_bay_ = bay_ - braced_bay_
        factor = (beamline_, braced_bay_, infill_bay_, beamline_, beamline_)
        
        # Multiply qty
        dfm = []
        for i, j in enumerate(df):
            j['qty'] = j['qty'].multiply(factor[i])
            dfm.append(j)

        # Combine all individual dataframes
        combine = qty_add(dfm)

        # Add to class csv dataframe
        parts = Parts().add_qty(combine)

        return parts
    
roof = Reg_duo(10, 10, 43, 2.572, 18, 'D78', 'hand')
print(roof.parts_list())
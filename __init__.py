import math
from parts import *

class Parts:
    def __init__(self):
        pass
    
    # Function to initialise Parts dataframe from csv file
    def read_csv(self, csv):
        self.parts = pd.read_csv('parts.csv')
        self.parts['qty'] = 0
        return self

    # Search function that returns dateframe with rows of codes provided
    def search(self, code:list):
        result = pd.DataFrame({})
        for i, c in enumerate(code):
            row = self.parts.loc[self.parts["Code"] == code[i]]
            result = pd.concat([result, row])
        return result
    
    # Adds qty tab to Parts dataframe and 
    def add_qty(self, df):
        self.parts = pd.merge(self.parts, df, on="Code", how="right", suffixes=('', 'y'))
        self.parts['qty'] = self.parts['qty'] + self.parts['qtyy']
        self.parts = self.parts.drop(['qtyy'], axis=1)
        return self



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


beamline = beam('LX133', 26)
beamline['10'] = beamline['qty'].mul(10)
print(beamline)
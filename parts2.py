import numpy as np
import pandas as pd
prefix = ''
spigot_code = ''
pin_code = ''

# object containing parts list as a pandas dataframe with various functions for add qty column, copy to clipboard etc
class Parts:
    def __init__(self):
        pass
    
    # Function to initialise Parts dataframe from csv file
    def read_csv(self, csv):
        self.parts = pd.read_csv(csv)
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
    
    # Remove all rows containing null value in qty coloumn
    def trim(self):
        result = self.parts.loc[self.parts['qty'] != '']
        return result
    
# returns numpy array of beam lengths
def beam_np(beam_type:str, length:int):
    if beam_type in ("D78", "LV78"):
        beam = np.zeros(6)
        if length <= 2:
            beam[length - 1] = 1
        else:
            beam[5] = length // 6
            beam[length % 6 - 1] = 1
    elif beam_type in ("AHD", "LX133"):
        beam = np.zeros(4)
        if length == 1: beam[0] = 1
        else: 
            beam[3] = length // 4
            beam[length % 4 - 1] = 1
    return beam

# returns pandas dataframe of beam_np with part codes including spigots and pins
def beam_pd(beam_type:str, length:int):

    global prefix
    global spigot_code
    global pin_code

    # numpy array of beam lengths
    beam = beam_np(beam_type, length)

    # Define product code prefix
    # Spigot and pin codes with qty
    joints = np.sum(beam) - 1
    spigots = joints * 2
    if beam_type == 'D78':
        prefix = 'BA'
        pins = spigots * 6
        spigot_code = "BS0001"
        pin_code = "AF0001"
    elif beam_type == 'LV78':
        prefix = 'LVB'
        pins = spigots * 6
        spigot_code = "LVS0001"
        pin_code = "LFX0001"
    elif beam_type == 'AHD':
        prefix = 'BD'
        pins = spigots * 8
        spigot_code = "BS0006"
        pin_code = "AF0001"
    elif beam_type == 'LX133':
        prefix = 'LXA'
        pins = spigots * 8
        spigot_code = "LXS0001"
        pin_code = "LFX0001"
    else: ValueError

    # Generate codes for beams and concat with qty
    if beam_type in ("D78", "LV78"):
        beam_lengths = np.arange(1000, 6001, 1000)
    elif beam_type in ("AHD","LX133"):
        beam_lengths = np.arange(1000, 4001, 1000)
    beam_codes = np.empty((len(beam_lengths), 1), dtype=object)
    for i, l in enumerate(beam_lengths):
        beam_codes[i] = prefix + str(l)
    beams = np.column_stack((beam_codes, beam))
    
    # Capture all parts and return data frame containing codes and qty
    joints = np.array([[pin_code, pins], [spigot_code, spigots]], dtype=object)
    parts = np.vstack((beams, joints))
    parts = parts[parts[:, 1] != 0]
    parts = pd.DataFrame(parts, columns=['Code', 'qty'])
    return parts

# Combined dataframes based on Code and sums qty
def qty_add(list):
    parts = pd.DataFrame({'Code': [], 'qty': []})
    for i in list:
        parts = pd.merge(parts, i, on='Code', how='outer', suffixes=('_x', '_y')).fillna(0)
        parts['qty'] = parts['qty_x'] + parts['qty_y']
        parts = parts.drop(['qty_x', 'qty_y'], axis=1)
    return parts

# returns pandas data frame for all components in a single duopitch beamline
def duo_beamline(lhs:int, rhs:int, pitch:int, beam_type:str):
    
    # Beam dataframes using beam function and merge
    lhs_beam, rhs_beam = beam_pd(beam_type, lhs), beam_pd(beam_type, rhs)

    # Ridge beam and associated components
    ridge = pd.DataFrame(
        {'Code':[prefix+'00'+str(pitch),
                spigot_code,
                pin_code],
        'qty':[1, 
               4, 
               6*4 if prefix in ('D78', 'LV78') else 8*4]})
    
    track = pd.DataFrame([])

    parts = qty_add([lhs_beam, rhs_beam, ridge])

    return parts
    
print(duo_beamline(20,20,18,'D78'))  


# returns pandas data frame for all components in a single duopitch bay
def duo_bay(lhs:int, rhs:int, bay_size:float, beam_type:str, sheet_exact:bool):
    ...

def support(support:bool):
    ...

# regular baysize duopitch roof
def reg_duo(lhs:int, rhs:int, length:float, pitch:int, bay_size:float, 
            beam_type:str, sheet_exact:bool, support:str, gable:bool, tiebar:int):
    ...

# regular baysize monopitch roof
def reg_mono(beam:int, length:float, bay_size:float, beam_type:str, 
             sheet_exact:bool, support:str, gable:bool):
    ...

# irregular baysize duopitch roof, input lists for each bay
def irr_duo(lhs:list, rhs:list, bay_sizes:list, beam_type:str, 
            sheet_exact:bool, support:str, gable:bool, tiebar:int):
    ...

# irregular baysize monopitch roof, input list for each bay
def irr_mono(beams:int, bay_sizes:list, beam_type:str, 
             sheet_exact:bool, support:str, gable:bool):
    ...

# regular baysize rolling duopitch roof
def roll_duo(lhs:int, rhs:int, length:float, pitch:int, bay_size:float, 
             beam_type:str, support:str, gable:bool, tiebar:int):
    ...
import numpy as np
import pandas as pd

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

# returns numpy array of beam lengths
def beam_np(beam_type:str, length:int):
    ...

# returns pandas dataframe of beam_np with part codes including spigots and pins
def beam_pd(beam_type:str, length:int):
    ...

# returns pandas data frame for all components in a single duopitch beamline
def duo_beamline(lhs:int, rhs:int, pitch:int, beam_type:str):
    ...

# returns pandas data frame for all components in a single duopitch bay
def duo_bay(lhs:int, rhs:int, bay_size:float, beam_type:str, sheet_exact:bool):
    ...

def support(support:bool):
    ...
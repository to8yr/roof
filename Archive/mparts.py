from archive.olparts import *

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
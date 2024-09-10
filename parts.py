import numpy as np
import pandas as pd

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

def beam(beam_type, length):

    # Define product code prefix
    if beam_type == "D78":
        prefix = "BA"
    elif beam_type == "LV78":
        prefix = "LVB"
    elif beam_type == "AHD":
        prefix = "BD"
    elif beam_type == "LX133":
        prefix = "LXA"
    else:
        print("Invalid input. Please enter a valid number.")

    # Create empty array based on size
    if beam_type in ("D78", "LV78"):
        array = 6
    elif beam_type in ("AHD", "LX133"):
        array = 4
    beam = np.zeros(array)

    # Update empty array based on required sizes
    if beam_type in ("D78", "LV78"):
        if length == 1:
            beam[0] = 1
        elif length == 2:
            beam[1] = 1
        else:
            beam[5] = length // 6
            remainder = length % 6
            if remainder == 1:
                beam[2] = 1
                beam[3] = 1
                beam[5] -= 1
            elif remainder == 2:
                beam[2] = 1
                beam[4] = 1
                beam[5] -= 1
            elif remainder == 3:
                beam[2] = 1
            elif remainder == 4:
                beam[3] = 1
            elif remainder == 5:
                beam[4] = 1
    elif beam_type in ("AHD", "LX133"):
        if 0 < length < 2:
            beam[0] = 1
        else:
            beam[3] = length // 4
            remainder = length % 4
            if remainder == 1:
                beam[0] += 1
            elif remainder == 2:
                beam[1] = 1
            elif remainder == 3:
                beam[2] = 1

    # Generate codes for beams and concat with qty
    if beam_type in ("D78", "LV78"):
        beam_lengths = np.arange(1000, 6001, 1000)
    elif beam_type in ("AHD","LX133"):
        beam_lengths = np.arange(1000, 4001, 1000)
    beam_codes = np.empty((len(beam_lengths), 1), dtype=object)
    for i, l in enumerate(beam_lengths):
        beam_codes[i] = prefix + str(l)
    beams = np.column_stack((beam_codes, beam))

    # Spigot and pin codes and qty based on number of beams
    joint = np.sum(beam) - 1
    spigots = joint * 2
    if beam_type == "D78":
        pins = spigots * 6
        spigot_code = "BS0001"
        pin_code = "AF0001"
    elif beam_type == "LV78":
        pins = spigots * 6
        spigot_code = "LVS0001"
        pin_code = "LFX0001"
    elif beam_type == "AHD":
        pins = spigots * 8
        spigot_code = "BS0006"
        pin_code = "AF0001"
    elif beam_type == "LX133":
        pins = spigots * 8
        spigot_code = "LXS0001"
        pin_code = "LFX0001"

    # Capture all parts and return data frame containing codes and qty
    joints = np.array([[pin_code, pins], [spigot_code, spigots]], dtype=object)
    parts = np.vstack((beams, joints))
    parts = parts[parts[:, 1] != 0]
    parts = pd.DataFrame(parts, columns=['Code', 'qty'])
    return parts

def duo_beamline(lhs, rhs, pitch, beam_type):

    # beam code
    if beam_type == "78cm":
        beam_code = "LBA"
    elif beam_type == "LV78":
        beam_code = "LVB"
    elif beam_type == "LX133":
        beam_code = "LXA"

    # Generate beam length list using dbeam
    lhs_beams, rhs_beams = beam(beam_type, lhs), beam(beam_type, rhs)
    beam_count = np.sum(np.column_stack((lhs_beams, rhs_beams)), axis=1)

    # Create list for beam quantiies
    if beam_type in ("78cm", "LV78"):
        beam_lengths = np.array(["1000", "2000", "3000", "4000", "5000", "6000"])
    elif beam_type == "LX133":
        beam_lengths = np.array(["1000", "2000", "3000", "4000"])
    beam_codes = np.empty((len(beam_lengths), 1), dtype=object)
    for i, l in enumerate(beam_lengths):
        beam_codes[i] = beam_code + l
    beams = np.column_stack((beam_codes, beam_count))

    # Spigot and Pin quantities
    joint = np.sum(beam_count)
    spigots = joint * 2
    if beam_type in ("78cm", "LV78"):
        pins = spigots * 6
        spigot_code = "LVS0001"
    elif beam_type == "LX133":
        pins = spigots * 8
        spigot_code = "LXS0001"
    joints = np.array([["LFX0001", pins], [spigot_code, spigots]], dtype=object)

    # Tracking
    if beam_type == "LX133":
        lhs_track, rhs_track = lhs_beams, rhs_beams
    elif beam_type in ("78cm", "LV78"):
        lhs_track, rhs_track = beam("LX133", lhs), beam("LX133", rhs)
    track_count = np.sum(np.column_stack((lhs_track, rhs_track)), axis=1)
    track_spigots = np.sum(track_count)
    compressors = 2
    tube_holder = 2
    track_codes = np.array(["UT1000", "UT2000", "UT3000", "UT4000"], dtype=object)
    tracks = np.column_stack((track_codes, track_count))
    track_components = np.array([["UA0005", compressors], ["UA0016", tube_holder], ["UA0021", track_spigots]], dtype=object)
    tracks = np.vstack([tracks, track_components])

    # Beamline parts list generation
    parts = np.vstack((beams, joints, tracks))
    parts = parts[parts[:, 1] != 0]

    return parts

def duo_bay(lhs, rhs, beam_type, bay_size):

    fra_qty, pla_qty = 0, 0

    hor, dia, pla, fra = "LHB", "LDB", "LPB", "UK"

    if beam_type == "78cm":
        fra_qty = lhs//2 + rhs//2
        hort_qty = sum((0 if lhs%2==0 else 1, 0 if rhs%2==0 else 1))
        horb_qty = fra_qty + 2
        dia_qty = horb_qty
    elif beam_type == "LV78":
        hort_qty = lhs + rhs
        horb_qty = lhs//2 + rhs//2 + 2
        dia_qty = horb_qty
        pla_qty = hort_qty
    elif beam_type == "LX133":
        hort_qty = lhs + rhs
        horb_qty = lhs//2 + rhs//2
        dia_qty = horb_qty
        pla_qty = hort_qty

    hor_code = hor + str(bay_size)
    pla_code = pla + str(bay_size)
    fra_code = fra + str(bay_size)
    dia_code = dia + str(int((bay_size**2 + 732**2 if beam_type in ("78cm", "LV78") else 1280**2)**0.5))

    parts = np.array([[hor_code, horb_qty+hort_qty],
                     [dia_code, dia_qty],
                     [fra_code, fra_qty],
                     [pla_code, pla_qty]], dtype=object)
    parts = parts[parts[:, 1] != 0]

    return parts
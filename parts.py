import numpy as np

def dbeam(beam_type, length):

    # Determine the number of elements in the beam array based on size
    if beam_type in ("78cm", "LV78"):
        beam = np.array([0, 0, 0, 0, 0, 0])
    elif beam_type == "LX133":
        beam = np.array([0, 0, 0, 0])
    else:
        raise ValueError("Invalid beam size")

    # Calculate the required beams based on size and length
    if beam_type in ("78cm", "LV78"):
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
    elif beam_type == "LX133":
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

    return beam


def duo_beamline(lhs, rhs, pitch, beam_type):

    # beam code
    if beam_type == "78cm":
        beam_code = "LBA"
    elif beam_type == "LV78":
        beam_code = "LVB"
    elif beam_type == "LX133":
        beam_code = "LXA"

    # Generate beam length list using dbeam
    lhs_beams, rhs_beams = dbeam(beam_type, lhs), dbeam(beam_type, rhs)
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
        lhs_track, rhs_track = dbeam("LX133", lhs), dbeam("LX133", rhs)
    track_count = np.sum(np.column_stack((lhs_track, rhs_track)), axis=1)
    track_spigots = np.sum(track_count)
    compressors = 2
    tube_holder = 2
    track_codes = np.array(["UT1000", "UT2000", "UT3000", "UT4000"], dtype=object)
    tracks = np.column_stack((track_codes, track_count))
    track_components = np.array([["UA0005", compressors], ["UA0016", tube_holder], ["UA0021", track_spigots]], dtype=object)
    tracks = np.row_stack([tracks, track_components])

    # Beamline parts list generation
    parts = np.row_stack((beams, joints, tracks))
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
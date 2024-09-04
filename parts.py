def dbeam(beam_type, length):
    # Determine the number of elements in the beam array based on size
    if beam_type in ("78cm", "LV78"):
        beam = [0, 0, 0, 0, 0, 0]
    elif beam_type == "LX133":
        beam = [0, 0, 0, 0]
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
    
    beamline_parts = []

    lhs_beams, rhs_beams = dbeam(beam_type, lhs), dbeam(beam_type, rhs)
    beam_count = [x + y for x, y in zip(lhs_beams, rhs_beams)]

    if beam_type == "78cm":
        beam_codes = ["LBA1000", "LBA2000", "LBA3000", "LBA4000", "LBA5000", "LBA6000"]
    elif beam_type == "LV78":
        beam_codes = ["LVB1000", "LVB2000", "LVB3000", "LVB4000", "LVB5000", "LVB6000"]
    elif beam_type == "LX133":
        beam_codes = ["LXA1000", "LXA2000", "LXA3000", "LXA4000"]
    
    beams = list(zip(beam_codes, beam_count))
    
    return beams


print(duo_beamline(11, 10, 18, "78cm"))
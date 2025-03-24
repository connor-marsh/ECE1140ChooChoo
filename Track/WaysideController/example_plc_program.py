def plc_logic(block_occupancies, switch_positions, light_signals, crossing_signals, previous_occupancies):
    """
    User-defined logic for controlling track switches.
    - True for switches indicates:
    - False for switches indicates:

    -True for lights indicates: GREEN
    -False for lights indicates: RED

    -True for crossings indicates: ACTIVE
    -False for crossings indicates: INACTIVE

    -True for occupancies indicates: OCCUPIED
    -False for occupancies indicates: UNOCCUPIED
    """
    switch_positions[0] = (block_occupancies[0] or block_occupancies[1] or block_occupancies[2]) and not block_occupancies[3]
    switch_positions[1] = block_occupancies[1]
    switch_positions[2] = not block_occupancies[2]

    light_signals[0] = block_occupancies[1]

    crossing_signals[0] = block_occupancies[0]



    return switch_positions, light_signals, crossing_signals, block_occupancies
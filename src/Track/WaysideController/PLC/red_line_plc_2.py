def plc_logic(block_occupancies, switch_positions, light_signals, crossing_signals, previous_occupancies, exit_blocks, clamps):
    """
    User-defined logic for controlling track switches, lights, and crossing signals.

    :param block_occupancies: The current occupancies of the track

        - True for occupancies indicates: OCCUPIED
        - False for occupancies indicates: UNOCCUPIED

    :param switch_positions: The current status of the switch signals

        - True for switches indicates: POSITION eg (1-2)
        - False for switches indicates: POSITION eg (1-3)

    :param light_signals: The current status of the light signals

        - True for lights indicates: GREEN
        - False for lights indicates: RED

    :param crossing_signals: The current status of the crossing signals

        - True for crossings indicates: ACTIVE
        - False for crossings indicates: INACTIVE

    :param previous_occupancies: The occupancies of the track from the previous execution of the PLC program

        - True for occupancies indicates: OCCUPIED
        - False for occupancies indicates: UNOCCUPIED

    :param exit_blocks: A 1 hot vector that selects the current exit block

        - True for exit blocks indicates: SELECTED
        - False for exit blocks indicates: NOT SELECTED
    
    :param clamps: a list of booleans where true indicates the block should be clamped

    :returns switch_positions, light_signals, light_signals crossing_signals, previous_occupancies:
    """

    # For Wayside #2
    # HAS 26 Blocks in its Territory
    # Sections: H[0,17) I[17,18) P[18,21) Q[21,22) R[22,23) S[23,26)
    # Has 3 Switches H33:(33 - 32, 33 - 72) H38:(38 - 39, 38 - 71) H44:(44 - 43, 44 - 67) 
    # Has 6 Lights H32, H39, H43, Q71, R72
    # Has No Crossings

    train_in_h = any(block_occupancies[0:17])
    train_in_i = any(block_occupancies[17:18])
    train_in_P = any(block_occupancies[18:21])
    train_in_q = any(block_occupancies[21:22])
    train_in_r = any(block_occupancies[22:23])
    train_in_s = any(block_occupancies[23:26])
    
    switch_positions[0] = any(block_occupancies[4:9])
    switch_positions[1] = not train_in_h
    switch_positions[2] = not any(block_occupancies[0:15])
    

    return switch_positions, light_signals, crossing_signals, clamps
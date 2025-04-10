def plc_logic(block_occupancies, switch_positions, light_signals, crossing_signals, previous_occupancies, exit_blocks):
    """
    User-defined logic for controlling track switches.

    :param block_occupancies: The current occupancies of the track

        - True for occupancies indicates: OCCUPIED
        - False for occupancies indicates: UNOCCUPIED

    :param switch_positions: The current status of the switch signals

        - True for switches indicates:
        - False for switches indicates:

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
    
    :returns switch_positions, light_signals, light_signals crossing_signals, previous_occupancies:
    """
    # For Wayside #3
    # HAS 40 Blocks in its Territory
    # Sections: L[0, 5) M[5, 8) N[8, 17) O[17, 20) P[20, 29) Q[29, 32) R[32, 33) S[33, 36) T[36, 41)
    # Has 2 Switches
    # Has X Lights
    # Has 1 Crossing

    train_in_o_p_q = any(block_occupancies[17:33])
    train_in_n = any(block_occupancies[8:17])
    train_in_m = any(block_occupancies[5:8])
                    
    switch_positions[0] = train_in_n
    switch_positions[1] = train_in_o_p_q and not (train_in_m and train_in_n)

    return switch_positions, light_signals, crossing_signals


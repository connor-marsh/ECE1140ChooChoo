def plc_logic(block_occupancies, switch_positions, light_signals, crossing_signals, previous_occupancies, exit_blocks, clamps):
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
    # HAS 44 Blocks in its Territory
    # Sections: L[0, 5) M[5, 8) N[8, 17) O[17, 20) P[20, 29) Q[29, 32) R[32, 33) S[33, 36) T[36, 41) U[41,44)
    # Has 2 Switches N77 (77-76, 77-101), N85 (85-86, 85-100)
    # Has 4 Lights M76, Q86, Q100, R101
    # Has 1 Crossing T108

    train_in_o_p_q = any(block_occupancies[17:33])
    train_in_n = any(block_occupancies[8:17])
    train_in_m = any(block_occupancies[5:8])
    train_in_t = any(block_occupancies[36:41])
    train_in_r = any(block_occupancies[32,33])

    switch_positions[0] = train_in_n or train_in_o_p_q  
    light_signals[0] = not switch_positions[0]
    light_signals[2] = not light_signals[0]


    switch_positions[1] = train_in_o_p_q and not train_in_n
    light_signals[1] = not switch_positions[1]
    light_signals[3] = not light_signals[1]

    crossing_signals[0] = train_in_t

    # switch to position 77-101 and train in m
    if switch_positions[0] and train_in_m:
        clamps[6:8] = [True]*len(clamps[6:8])
    else:
        clamps[6:8] = [False]*len(clamps[6:8])
    
  

    return switch_positions, light_signals, crossing_signals, clamps


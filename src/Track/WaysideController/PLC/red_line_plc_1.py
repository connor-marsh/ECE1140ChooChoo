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
    
    # For Wayside #1
    # HAS 36 Blocks in its Territory
    # Sections: A[0,3) B[3,6) C[6,9) D[9, 12) E[12,15) F[15,20) G[20,23) H[23,31) S[31,34) T[34, 35) T[35,36]
    # Has 3 Switches C9:(9 - 10, 9 - 77) F16:(16 - 1, 16 - 1) H27:(27 - 28, 27 - 76) 
    # Has 6 Lights A1, D10, E15, H28, T76, y77
    # Has 1 Crossing D11

    
    
    switch_positions[0] = True



    return switch_positions, light_signals, crossing_signals, clamps
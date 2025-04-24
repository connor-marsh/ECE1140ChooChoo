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
    # Sections: A[0,3) B[3,6) C[6,9) D[9, 12) E[12,15) F[15,20) G[20,23) H[23,31) S[31,34) T[34, 35) y[35,36)
    # Has 3 Switches C9:(9 - 10,9 - 77) F16:(16 - 1, 16 - 1) H27:(27 - 28, 27 - 76) 
    # Has 6 Lights A1, D10, E15, H28, T76, y77
    # Has 1 Crossing D11



    train_in_a = any(block_occupancies[0:3])
    train_in_b = any(block_occupancies[3:6])
    train_in_c = any(block_occupancies[6:9])
    train_in_d = any(block_occupancies[9:12])
    train_in_e = any(block_occupancies[12:15])
    train_in_f = any(block_occupancies[15:20])
    train_in_g = any(block_occupancies[20:23])
    train_in_h = any(block_occupancies[23:31])
    train_in_s = any(block_occupancies[31:34])
    train_in_t = any(block_occupancies[34:35])
    train_in_y = any(block_occupancies[35:36])

    prev_train_in_a = any(previous_occupancies[0:3])
    prev_train_in_b = any(previous_occupancies[3:6])
    prev_train_in_c = any(previous_occupancies[6:9])
    prev_train_in_d = any(previous_occupancies[9:12])
    prev_train_in_e = any(previous_occupancies[12:15])
    prev_train_in_f = any(previous_occupancies[15:20])
    prev_train_in_g = any(previous_occupancies[20:23])
    prev_train_in_h = any(previous_occupancies[23:31])
    prev_train_in_s = any(previous_occupancies[31:34])
    prev_train_in_t = any(previous_occupancies[34:35])
    prev_train_in_y = any(previous_occupancies[35:36])

    switch_positions[0] = not(train_in_a or train_in_b or train_in_c) or exit_blocks[0]
    light_signals[1] = not switch_positions[0]
    light_signals[5] = switch_positions[0]
    
    
    switch_positions[1] = False
    light_signals[0] = not switch_positions[1]
    light_signals[2] = not light_signals[0]


    switch_positions[2] = False
    light_signals[3] = not switch_positions[2]
    light_signals[4] = not light_signals[3]


    crossing_signals[0] = train_in_d
    
    if not switch_positions[0]:
        clamps[35] = True
    else:
        clamps[35] = False

    if switch_positions[0]:
        clamps[10:12] = [True]*len(clamps[10:12])
    else:
        clamps[10:12] = [False]*len(clamps[10:12])
    # update persistent state
    #plc_logic.prev_train_increasing_abc = train_increasing_abc
    #plc_logic.prev_train_decreasing_abc = train_decreasing_abc

    return switch_positions, light_signals, crossing_signals, clamps


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


    if not hasattr(plc_logic, 'prev_train_increasing_abc'):
        plc_logic.prev_train_increasing_abc = False
        plc_logic.prev_train_decreasing_abc = False
        plc_logic.prev_train_decreasing_de = False
        print("RED LINE INITIALIZED PLC LOGIC")


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


    

    train_in_abc = train_in_a or train_in_b or train_in_c

    """
    if train_in_abc:
        if not plc_logic.prev_train_increasing_abc: # only need to do these if its not already true
            train_f_to_a = train_in_a and prev_train_in_f # check if increasing direction
            train_a_to_b = train_in_b and prev_train_in_a
            train_b_to_c = train_in_c and prev_train_in_b

        if not plc_logic.prev_train_decreasing_abc:
            train_d_to_c = train_in_c and prev_train_in_d # check if decreasing direction
            train_c_to_b = train_in_b and prev_train_in_c
            train_b_to_a = train_in_a and prev_train_in_b
            train_y_to_c = train_in_c and prev_train_in_y

        if not plc_logic.prev_train_decreasing_abc:
            train_c_to_d = train_in_d and prev_train_in_c
            train_d_to_e = train_in_e and prev_train_in_d


        train_increasing_abc = train_f_to_a or train_a_to_b or train_b_to_c or plc_logic.prev_train_increasing_abc
        train_decreasing_abc = train_d_to_c or train_c_to_b or train_b_to_a or plc_logic.prev_train_decreasing_abc
        train_decreasing_de = train_c_to_d or train_d_to_e or plc_logic.prev_train_decreasing_de
    else: # reset the values if there are no trains
        train_increasing_abc = False
        train_decreasing_abc = False
        train_decreasing_de = False
    """
    """
    switch_positions[0] = ((not (train_in_abc or train_in_d) or # if no trains are nearby switch to the yard
                          (train_decreasing_abc and not train_in_d) or # if already is a train heading away from the yard
                          (train_increasing_abc)) and # NEED EXIT BLOCK LOGIC HERE MOST LIKELY (CASE FOR TRAIN ENTERING THE YARD)
                          not train_decreasing_de) # finally check if there is not a train trying to exit away from the loop from d or e
    """


    switch_positions[0] = not train_in_abc or train_in_d
    light_signals[1] = not switch_positions[0]
    light_signals[5] = switch_positions[0]
    
    switch_positions[1] = not train_in_f and train_in_abc or train_in_d or train_in_e
    light_signals[0] = not switch_positions[1]
    light_signals[2] = not light_signals[0]

    switch_positions[2] = train_in_t
    light_signals[3] = not switch_positions[2]
    light_signals[4] = not light_signals[3]
    
    crossing_signals[0] = train_in_d
    
    
    if not switch_positions[0]:
        clamps[64] = True
    else:
        clamps[64] = False



    if switch_positions[0]:
        clamps[10:12] = [True]*len(clamps[10:12])
    else:
        clamps[10:12] = [False]*len(clamps[10:12])
    # update persistent state
    #plc_logic.prev_train_increasing_abc = train_increasing_abc
    #plc_logic.prev_train_decreasing_abc = train_decreasing_abc

    return switch_positions, light_signals, crossing_signals, clamps


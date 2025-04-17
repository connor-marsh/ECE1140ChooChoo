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
    # For Wayside #2
    # HAS 66 Blocks in its Territory
    # Sections: I[0,22) J[22,27) K[27,33) L[33,39) U[39,43) V[43,48) W[48,64) y[64,66)
    # Has 2 Switches I57 (57 - 58, 57-152), K63 (63 - 151, 63 - 62) 
    # Has 4 Lights J58, J62, y151, y152
    # Has 0 Crossings



    train_in_i = any(block_occupancies[0:22])

    train_in_j = any(block_occupancies[22:27])

    train_entering_track = block_occupancies[65]

    switch_positions[0] = not train_in_i # add exit block logic here when that gets implemented
    light_signals[0] = not switch_positions[0]
    light_signals[1] = not light_signals[1]
    
    switch_positions[1] = train_in_j and not train_entering_track
    light_signals[2] = switch_positions[1]
    light_signals[3] = not light_signals[2]


    territory_branch_i_l = list(range(0,39))
    territory_branch_u_w = list(range(39,64))

    for i, block_idx in enumerate(territory_branch_i_l):
        if block_occupancies[block_idx]:  # only need to check until overlap section reached or a few blocks before a switch
            distance_to_end = abs(len(territory_branch_i_l) - i)
            if block_occupancies[block_idx] and previous_occupancies[block_idx - 1 if block_idx > 0 else 0]:
                if block_occupancies[block_idx + 2]:
                    clamps[block_idx] = True
            elif block_occupancies[block_idx] and previous_occupancies[block_idx]:
                if block_occupancies[block_idx + 2]:
                    clamps[block_idx] = True
            if clamps[block_idx]:
                if not block_occupancies[block_idx + 2]:
                    clamps[block_idx] = False

    for i, block_idx in enumerate(territory_branch_u_w):
        if block_occupancies[block_idx]:
            distance_to_end = abs(len(territory_branch_i_l) - i)
            if distance_to_end > 2: # only need to check until overlap section reached or a few blocks before a switch
                if block_occupancies[block_idx] and previous_occupancies[block_idx - 1 if block_idx > 0 else 0]:
                    if block_occupancies[block_idx + 2]:
                        clamps[block_idx] = True
                elif block_occupancies[block_idx] and previous_occupancies[block_idx]:
                    if block_occupancies[block_idx + 2]:
                        clamps[block_idx] = True
                if clamps[block_idx]:
                    if not block_occupancies[block_idx + 2]:
                        clamps[block_idx] = False

    # if switch position facing the yard and train in j
    if not switch_positions[1] and train_in_j:
        clamps[25:27] = [True]*len(clamps[25:27])
    else:
        clamps[25:27] = [False]*len(clamps[25:27])
    
    
    return switch_positions, light_signals, crossing_signals, clamps


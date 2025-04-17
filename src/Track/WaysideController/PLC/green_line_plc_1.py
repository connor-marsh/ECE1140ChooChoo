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
    # HAS 54 Blocks in its Territory
    # Sections: A[0,3) B[3,6) C[6,12) D[12,16) E[16,20) F[20,28) G[28,32) H[32,35) I[35,38) W[38,47) X[47,50) Y[50,53) Z[53,54)
    # Has 2 Switches D13 (13 - 12, 13 - 1) F28 (28 - 29, 28 - 150)
    # Has 4 Lights A1, C12, G29, Z150
    # Has 1 Crossing E19

    train_in_a_b_c = any(block_occupancies[0:12])

    train_in_c_end = any(block_occupancies[9:12])

    train_in_d_e_f = any(block_occupancies[12:28])

    train_in_e = any(block_occupancies[16:20])

    train_in_y_z = any(block_occupancies[50:54])
    
  
    switch_positions[0] = train_in_a_b_c and not train_in_d_e_f
    light_signals[0] = switch_positions[0]
    light_signals[1] = not light_signals[0]

    switch_positions[1] = train_in_y_z and not (train_in_d_e_f or train_in_c_end)
    light_signals[2] = not switch_positions[1]
    light_signals[3] = not light_signals[2]

    crossing_signals[0] = train_in_e

    # if the switch position is in the wrong position 13-12 and there is a train in the off section
    if not switch_positions[0] and train_in_a_b_c:
        clamps[0:2] = [True]*len(clamps[0:2]) # clamp the blocks in a just in case
    else:
        clamps[0:2] = [False]*len(clamps[0:2])
    # if the switch is in the wrong position 28-29 and there is a train in the section incoming
    if not switch_positions[1] and train_in_y_z:
        clamps[52:54] = [True]*len(clamps[52:54]) # clamp the blocks in z in case
    else:
        clamps[52:54] = [False]*len(clamps[52:54])

    
     

    
    territory_branch_w_z = list(range(38,54)) # that specify which blocks in the block occupancies list to iterate through
    territory_branch_d_i = list(range(12,38))
    territory_branch_f_a = list(range(27,-1,-1)) 

    # each branch needs to do separate checks.
    for i, block_idx in enumerate(territory_branch_w_z): # block index is a value within the range, but i is just index based on the length of the range
        if block_occupancies[block_idx]: # for any occupied block
            distance_to_end = len(territory_branch_w_z) - i 
            if distance_to_end > 2: # that is not next to the end of the section (overlapping territory in other wayside should account for this, or approaching a switch which is handled differently)
                if block_occupancies[block_idx] and previous_occupancies[block_idx - 1 if block_idx > 0 else 0]: # if traveling 
                    if block_occupancies[block_idx + 2]: # only need to check the blocks that arent right by the switch since switch clamping is handled separate?
                        clamps[block_idx] = True
                elif block_occupancies[block_idx] and previous_occupancies[block_idx]: # if stationary at the block since last cycle
                    if block_occupancies[block_idx + 2]:
                        clamps[block_idx] = True
                
                if clamps[block_idx]: # check any current clamps to make sure the condition is no longer true
                    if not block_occupancies[block_idx + 2]:
                        clamps[block_idx] = False

    for i, block_idx in enumerate(territory_branch_d_i):
        if block_occupancies[block_idx]:
            distance_to_end = len(territory_branch_d_i) - i
            if distance_to_end > 2:
                if block_occupancies[block_idx] and previous_occupancies[block_idx - 1 if block_idx > 0 else 0]: # if traveling 
                    if block_occupancies[block_idx + 2]: # only need to check the blocks that arent right by the switch since switch clamping is handled separate?
                        clamps[block_idx] = True
                elif block_occupancies[block_idx] and previous_occupancies[block_idx]: # if stationary at the block since last cycle
                    if block_occupancies[block_idx + 2]:
                        clamps[block_idx] = True
               
                if clamps[block_idx]: # check any current clamps to make sure the condition is no longer trade
                    if not block_occupancies[block_idx + 2]:
                        clamps[block_idx] = False

    for i, block_idx in enumerate(territory_branch_f_a):
        if block_occupancies[block_idx]:
            distance_to_end = abs(len(territory_branch_f_a) - i)
            if distance_to_end > 2:
                if block_occupancies[block_idx] and previous_occupancies[block_idx + 1 if block_idx < (len(territory_branch_f_a) - 1)  else block_idx]: # if traveling 
                    if block_occupancies[block_idx - 2]: # only need to check the blocks that arent right by the switch since switch clamping is handled separate?
                        clamps[block_idx] = True
                elif block_occupancies[block_idx] and previous_occupancies[block_idx]: # if stationary at the block since last cycle
                    if block_occupancies[block_idx - 2]:
                        clamps[block_idx] = True
                
                if clamps[block_idx]: # check any current clamps to make sure the condition is no longer trade
                    if not block_occupancies[block_idx - 2]:
                        clamps[block_idx] = False
    
        
    return switch_positions, light_signals, crossing_signals, clamps
    

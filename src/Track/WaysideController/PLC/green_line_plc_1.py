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

    train_in_d_e_f = any(block_occupancies[12:28])

    train_in_e = any(block_occupancies[16:20])

    train_in_y_z = any(block_occupancies[50:54])
    
  
    switch_positions[0] = train_in_a_b_c and not train_in_d_e_f
    light_signals[0] = switch_positions[0]
    light_signals[1] = not light_signals[0]

    switch_positions[1] = train_in_y_z and not train_in_d_e_f
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

    
     

     # one way section C B A or [11, 5) DESCENDING
     # two way section D E F [12, 28) == F E D [27, 11)
     # one way section G H I [28 to 38) ASCENDING
     # one way section W X Y Z [38 to 54) ASCENDING

     # handle each of the above separately for clamping? Although that makes it difficult to clamp at the boundaries?
     # scan the array in a different order? could resort the array?
     # start from which section?
     # determine direction by comparing previous previous block occupancies
     # train can occupy either 1 or 2 blocks at the same time
     # use the clamps themselves as an input?
     # clamps are a list, there exists a clamp for each block

    #POTENTIAL CHECK (ITERATE THROUGH WHOLE TERRITORY BUT ACCOUNT THAT CERTAIN SECTIONS REQUIRE CHECKING "BEHIND" THE TRAIN since DESCENDING OR CAN BE BOTH WAYS)
     # locate each train in the territory
     # for two way sections determine the direction of travel?
     # for each train in the territory
        # check if the train was previously clamped?
        # check if there is another train or occupancy ahead of it within 2 block range
        # set clamp if not previously, or continue to clamp? ie clamp at block = True
        # unclamp any previous clamp if the condition no longer holds ie clamp at block = False
        
    return switch_positions, light_signals, crossing_signals, clamps
    

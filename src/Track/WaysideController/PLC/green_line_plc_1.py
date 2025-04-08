def plc_logic(block_occupancies, switch_positions, light_signals, crossing_signals, previous_occupancies, exit_blocks):
    """
    User-defined logic for controlling track switches, lights, and crossing signals.

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
    train_in_a_b_c = any(block_occupancies[0:12])

    train_in_d_e_f = any(block_occupancies[12:28])

    train_in_e = any(block_occupancies[16:20])

    train_in_y_z = any(block_occupancies[47:51])
    
  
    switch_positions[0] = train_in_a_b_c and not train_in_d_e_f
    light_signals[0] = not switch_positions[0]
    light_signals[1] = switch_positions[0]

    switch_positions[1] = train_in_y_z and not train_in_d_e_f
    light_signals[2] = not switch_positions[1]
    light_signals[3] = switch_positions[1]

    crossing_signals[0] = train_in_e
    return switch_positions, light_signals, crossing_signals
    

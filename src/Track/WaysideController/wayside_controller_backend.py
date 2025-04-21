"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class representing a singular Wayside Controller Device. This class runs the user input PLC program.
"""
import importlib.util
import sys
import time
import os
import globals.signals as Signals
from pathlib import Path
from PyQt5.QtCore import pyqtSlot, QObject, QTimer
from Track.TrackModel.track_model_enums import Occupancy
from Track.WaysideController.wayside_controller_collection import WaysideControllerCollection
class WaysideController(QObject):
    """
    Accepts a user created plc program at runtime and executes it.
    """
    def __init__(self, block_count: int, switch_count: int, light_count: int, crossing_count: int, exit_block_count: int, index: int, collection_reference: WaysideControllerCollection):
        """
        :param block_count: Nonnegative Integer number of input blocks to the PLC program
        :param switch_count: Nonnegative Integer number of switches controlled by the PLC program
        :param light_count: Nonnegative Integer number of light signals controlled by the PLC program
        :param crossing_count: Nonnegative Integer number of crossing signals controlled by the PLC program
        :param exit_block_count: Nonnegative integer number of exit blocks that the territory of the wayside has
        :param index: The index of the controller object
        :param collection_reference: Allows the controller to access the constants associated with the track and know which blocks are in its range
        """
        super().__init__()
        self.plc_filename = "" # The name of the plc file, used by the ui to display the name properly, otherwise not really necessary
        self.block_occupancies = [False] * block_count  # List of block occupancies [OCCUPIED == True, UNOCCUPIED == False]
        self.switch_positions = [False] * switch_count  # List of switch positions
        self.light_signals = [False] * light_count # List of light signals [GREEN == True, RED == False]
        self.crossing_signals = [False] * crossing_count # List of crossings [ACTIVE == True, INACTIVE == False]
        self.previous_occupancies = [False] * block_count # List of previous block occupancies [OCCUPIED == True, UNOCCUPIED == False]
        self.exit_blocks = [False] * exit_block_count # List of exit blocks [1 hot vector, SELECTED/CURRENT == True, NOT SELECTED == False ]
        self.suggested_authorities = [None] * block_count # List of the suggested authority to each block BACKEND UI ONLY
        self.suggested_speeds = [None] * block_count # List of the suggested speed to each block UI ONLY BACKEND
        self.commanded_authorities = [None] * block_count # List of the commanded authority to each block UI only BACKEND
        self.commanded_speeds = [None] * block_count # List of the commanded speed to each block UI only BACKEND
        self.to_send_occupancies = {} # Dictionary to send to the ctc
        self.to_send_speeds = {} # Dictionary sent to the track model
        self.to_send_authorities = {} # Dictionary sent to the track model
        self.maintenances = [False] * block_count # True for maintenance false for no maintenace
        self.index = index # allows the controller to lookup information about the track based on which territory it is
        self.collection = collection_reference # 
        self.maintenance_mode = False # A boolean that indicates when the wayside controller is in maintenance mode.
        self.clamps = [False] * block_count # a list of blocks that should have their authority clamped by the plc
        self.program = None # python file uploaded by programmer

        Signals.communication.ctc_suggested.connect(self.handle_suggested_values) # connect signals
        
        self.timer = QTimer() # initialize update timer
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update)
        self.timer.start()


    @pyqtSlot()
    def update(self):
        if self.program != None:
            prev_clamps = self.clamps[:] # only need previous clamps temporarily
            self.previous_occupancies = self.block_occupancies[:] # get what the previous occupancies are
            self.execute_cycle() # make it so that it calls programmers code 3 times and checks
                  
            if self.collection.track_model != None:
                blocks = self.collection.blocks[self.index]
                
                for i, clamp in enumerate(self.clamps):
                    # Also clear out old suggested values while were at it
                    if not self.block_occupancies[i] and (self.suggested_authorities[i] != None or self.suggested_speeds[i] != None):
                        self.suggested_authorities[i] = None
                        self.suggested_speeds[i] = None
                    # if clamp and self.block_occupancies[i]:
                    #     self.to_send_authorities[blocks[i].id] = 0
                    #     self.commanded_authorities[i] = 0 # set ui
                    # elif not clamp and prev_clamps[i] and self.block_occupancies[i]:
                    #     self.commanded_authorities[i] = None
                    #     self.to_send_authorities[blocks[i].id] = None
                                        
                Signals.communication.wayside_block_occupancies.emit(self.to_send_occupancies)
                Signals.communication.wayside_plc_outputs.emit(blocks,self.switch_positions,self.light_signals,self.crossing_signals)

                self.collection.track_model.update_from_plc_outputs(sorted_blocks=blocks,
                                                                    switch_states=self.switch_positions,light_states=self.light_signals,
                                                                    crossing_states=self.crossing_signals)

                if len(self.to_send_authorities) > 0 or len(self.to_send_speeds) > 0:
                    self.collection.track_model.update_from_comms_outputs(wayside_speeds=self.to_send_speeds, wayside_authorities=self.to_send_authorities)
                    self.to_send_authorities = {}
                    self.to_send_speeds = {}


    def set_occupancies(self, occupancies: dict):
        """
        Receives occupancy updates from the track model (called by the track model)

        :param occupancies: A dictionary of block occupancies with keyed with the block id
        """
        if self.collection.track_model != None:
            for i, block in enumerate(self.collection.blocks[self.index]): # index the blocks only in the range of this controller
                occupancy = occupancies.get(block.id, Occupancy.UNOCCUPIED) # read from the dictionary

                if occupancy == Occupancy.UNOCCUPIED:
                    self.block_occupancies[i] = False
                    self.to_send_occupancies[block.id] = False
                else:
                    self.block_occupancies[i] = True # will have to change this with failures but should be fine for now
                    self.to_send_occupancies[block.id] = True

                

    @pyqtSlot(dict, dict)
    def handle_suggested_values(self, speeds, authorities):
        blocks = self.collection.blocks[self.index] # specifies to the list which slice of the track this controller is looking at
        
        # need to enumerate so that I can tell if the current block is occupied or not
        for i, block in enumerate(blocks): # only look at the blocks in this controller's range
            speed = speeds.get(block.id, None) # default to None in the case that there is no value sent
            authority = authorities.get(block.id, None)

            if speed != None: # just suggest the speed doesn't need to be one shot
                newValue = False
                if speed != self.suggested_speeds[i]:
                    newValue = True
                if newValue: # for oneshot
                    self.suggested_speeds[i] = speed # set the value in the ui list
                    self.commanded_speeds[i] = speed if speed <= block.speed_limit else block.speed_limit # clamp to speed limit
                    self.to_send_speeds[block.id] = speed # "commanded speed"

            if authority != None:
                newValue = False
                if authority != self.suggested_authorities[i]:
                    newValue = True
                if newValue: # for oneshot
                    self.suggested_authorities[i] = authority # set ui 
                    self.to_send_authorities[block.id] = authority
                    self.commanded_authorities[i] = authority # set ui

           

        
        
  

    def load_program(self, file_path="Track\WaysideController\example_plc_program.py") -> bool:
        """
        Dynamically load a user-defined Python PLC program.
        
        :param file_path: The file path to the plc program
        """
        try:
            spec = importlib.util.spec_from_file_location("plc_program", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["plc_program"] = module
            spec.loader.exec_module(module)
            
            # Verify that the program has a valid plc_logic function
            if not hasattr(module, "plc_logic") or not callable(module.plc_logic):
                raise ValueError("Error: The PLC program must define a callable 'plc_logic(block_occupancies, switch_positions, light_signals, crossing_signals, previous_occupancies, exit_blocks, clamps)' function.")

          
            self.program = module

            # Run an initial verification test
            self.verify_boolean_io()
            self.test_program_logic()

            print("✅ PLC program loaded successfully!")

        except (FileNotFoundError, ValueError, TypeError, IndexError) as e:
            print(f"\n❌ {e}\nPlease enter a valid PLC program file.")
            self.program = None # make sure there is no program stored
            return False  # Indicate failure
        
        return True  # Indicate success

    def verify_boolean_io(self):
        """Ensure inputs are strictly lists of booleans."""
        if not isinstance(self.block_occupancies, list) or not all(isinstance(value, bool) for value in self.block_occupancies):
            raise TypeError("Error: Block occupancies must be a list of boolean values (True/False).")

        if not isinstance(self.switch_positions, list) or not all(isinstance(value, bool) for value in self.switch_positions):
            raise TypeError("Error: Switch positions must be a list of boolean values (True/False).")
        
        if not isinstance(self.light_signals, list) or not all(isinstance(value, bool) for value in self.light_signals):
            raise TypeError("Error: Light signals must be a list of boolean values (True/False).")
        
        if not isinstance(self.crossing_signals, list) or not all(isinstance(value, bool) for value in self.crossing_signals):
            raise TypeError("Error: Crossing signals must be a list of boolean values (True/False).")
        
        if not isinstance(self.previous_occupancies, list) or not all(isinstance(value, bool) for value in self.previous_occupancies):
            raise TypeError("Error: Previous occupancies must be a list of boolean values (True/False).")
        
        if not isinstance(self.exit_blocks, list) or not all(isinstance(value, bool) for value in self.exit_blocks):
            raise TypeError("Error: Exit blocks must be a list of boolean values (True/False).")
        
        if not isinstance(self.clamps, list) or not all(isinstance(value, bool) for value in self.clamps):
            raise TypeError("Error: Clamps must be a list of boolean values (True/False).")

    def test_program_logic(self):
        """Test if the user-defined PLC logic function modifies only booleans."""
        test_switches, test_lights, test_crossings, test_clamps = self.program.plc_logic(self.block_occupancies, self.switch_positions, 
                                                                                           self.light_signals, self.crossing_signals, 
                                                                                           self.previous_occupancies, self.exit_blocks,
                                                                                           self.clamps)

        # Verify outputs after execution
        if not all(isinstance(value, bool) for value in test_switches):
            raise TypeError("Error: The PLC logic function must only modify switch positions as boolean (True/False).")
        
        if not all(isinstance(value, bool) for value in test_lights):
            raise TypeError("Error: The PLC logic function must only modify light signals as boolean (True/False).")
        
        if not all(isinstance(value, bool) for value in test_crossings):
            raise TypeError("Error: The PLC logic function must only modify crossing signals as boolean (True/False).")
        
        if not all(isinstance(value, bool) for value in test_clamps):
            raise TypeError("Error: The PLC logic function must only modify clamps as boolean (True/False).")



    def execute_cycle(self):
        """Runs one PLC scan cycle"""
        if self.program and hasattr(self.program, "plc_logic"):
            # Run the user-defined PLC logic
            self.switch_positions, self.light_signals, self.crossing_signals, self.clamps = self.program.plc_logic(self.block_occupancies, self.switch_positions, 
                                                                                                                   self.light_signals, self.crossing_signals, 
                                                                                                                   self.previous_occupancies, self.exit_blocks,
                                                                                                                   self.clamps)
       
            #compare these lists of values with the currently stored ones
            #figure out block id's based on index
            #set the updated dictionaries accordingly
            
    
  
    
    def get_user_input(self):
        """Prompts the user to input block occupancies as a list of booleans."""
        while True:
            user_input = input(f"Enter block occupancies ({len(self.block_occupancies)} values, 'True' or 'False', comma-separated): ")
            
            # Split input by commas and strip spaces
            values = [x.strip().lower() for x in user_input.split(',')]

            # Check if all values are either 'true' or 'false'
            if all(value in ['true', 'false'] for value in values):
                # Convert valid 'true'/'false' strings to boolean True/False
                boolean_values = [value == 'true' for value in values]
                
                # Check if the number of values matches the expected length
                if len(boolean_values) == len(self.block_occupancies):
                    return boolean_values
                else:
                    raise ValueError(f"Invalid input. Please enter exactly {len(self.block_occupancies)} values.")
            else:
                raise TypeError("Invalid input. Please enter only 'True' or 'False' values, separated by commas.")



    def run(self):
        """Run the wayside controller in a loop. Used in the case the controller itself is run as main."""
        while True:
            # Try to get new block occupancies from user
            try:
                self.block_occupancies = self.get_user_input()

            except (ValueError, TypeError) as e:
                print(f"\n❌ {e}")
                continue
                      
            self.execute_cycle() # Run a cycle of the PLC with the user inputs


            # Print input and output results to the screen 
            print(f"\n🖥️ PLC Execution Results:")
            print(f"INPUTS:")
            print(f"  Block Occupancies:    {self.block_occupancies}")
            print(f"  Previous Occupancies: {self.previous_occupancies}")
            print(f"  Exit Blocks:          {self.exit_blocks}")
            print(f"OUTPUTS:")
            print(f"  Switch Positions:     {self.switch_positions}")
            print(f"  Light Signals:        {self.light_signals}")
            print(f"  Crossing Signals:     {self.crossing_signals}")

            self.previous_occupancies = self.block_occupancies # Update the previous blocks to be the input to the previous cycle



if __name__ == "__main__":
    # --- Load User PLC Program ---
    controller = WaysideController(block_count=5, switch_count=3, light_count=1, crossing_count=1, exit_block_count=1)

    while True:
        user_file = input("Enter the path to the PLC program file: ")
        if os.path.exists(user_file) and user_file.endswith(".py") and controller.load_program(user_file): #use this to have the wayside controller do nothing when no program exists?
            break  # Exit loop once a valid program is loaded

    # --- Start the Wayside Controller ---
    controller.run()
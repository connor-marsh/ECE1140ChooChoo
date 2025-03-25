import importlib.util
import sys
import time
import os

class WaysideController():
    """
    Accepts a user created plc program at runtime and executes it.
    """
    def __init__(self, scan_time=0.5, block_count=5, switch_count=3, light_count=1, crossing_count=1, exit_block_count=1):
        """
        :param scan_time: PLC scan time
        :param block_count: Nonnegative Integer number of input blocks to the PLC program
        :param switch_count: Nonnegative Integer number of switches controlled by the PLC program
        :param light_count: Nonnegative Integer number of light signals controlled by the PLC program
        :param crossing_count: Nonnegative Integer number of crossing signals controlled by the PLC program
        :param exit_block_count: Nonnegative integer number of exit blocks that the territory of the wayside has
        """
        self.scan_time = scan_time  # PLC scan time
        self.block_occupancies = [False] * block_count  # List of block occupancies [OCCUPIED == True, UNOCCUPIED == False]
        self.switch_positions = [False] * switch_count  # List of switch positions
        self.light_signals = [False] * light_count # List of light signals [GREEN == True, RED == False]
        self.crossing_signals = [False] * crossing_count # List of crossings [ACTIVE == True, INACTIVE == False]
        self.previous_occupancies = [False] * block_count # List of previous block occupancies [OCCUPIED == True, UNOCCUPIED == False]
        self.exit_blocks = [False] * exit_block_count # List of exit blocks [1 hot vector, SELECTED/CURRENT == True, NOT SELECTED == False ]
        self.program = None  # User-defined program

    def load_program(self, file_path="Track\WaysideController\example_plc_program.py"):
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
                raise ValueError("Error: The PLC program must define a callable 'plc_logic(block_occupancies, switch_positions, light_signals, crossing_signals, previous_occupancies, exit_blocks)' function.")

            self.program = module

            # Run an initial verification test
            self.verify_boolean_io()
            self.test_program_logic()

            print("✅ PLC program loaded successfully!")

        except (FileNotFoundError, ValueError, TypeError) as e:
            print(f"\n❌ {e}\nPlease enter a valid PLC program file.")
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

    def test_program_logic(self):
        """Test if the user-defined PLC logic function modifies only booleans."""
        test_switches, test_lights, test_crossings = self.program.plc_logic(self.block_occupancies, self.switch_positions, 
                                                                                           self.light_signals, self.crossing_signals, 
                                                                                           self.previous_occupancies, self.exit_blocks)

        # Verify outputs after execution
        if not all(isinstance(value, bool) for value in test_switches):
            raise TypeError("Error: The PLC logic function must only modify switch positions as boolean (True/False).")
        
        if not all(isinstance(value, bool) for value in test_lights):
            raise TypeError("Error: The PLC logic function must only modify light signals as boolean (True/False).")
        
        if not all(isinstance(value, bool) for value in test_crossings):
            raise TypeError("Error: The PLC logic function must only modify crossing signals as boolean (True/False).")
        
        #if not all(isinstance(value, bool) for value in test_previous):
            #raise TypeError("Error: The PLC logic function must only modify occupancies as boolean (True/False).")



    def execute_cycle(self):
        """Runs one PLC scan cycle"""
        if self.program and hasattr(self.program, "plc_logic"):
            # Run the user-defined PLC logic
            self.switch_positions, self.light_signals, self.crossing_signals = self.program.plc_logic(self.block_occupancies, self.switch_positions, 
                                                                                                                                 self.light_signals, self.crossing_signals, 
                                                                                                                                 self.previous_occupancies, self.exit_blocks)

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
            time.sleep(self.scan_time)  # Simulate PLC scan time


if __name__ == "__main__":
    # --- Load User PLC Program ---
    controller = WaysideController(block_count=5, switch_count=3, light_count=1, crossing_count=1)

    while True:
        user_file = input("Enter the path to the PLC program file: ")
        if os.path.exists(user_file) and user_file.endswith(".py") and controller.load_program(user_file):
            break  # Exit loop once a valid program is loaded

    # --- Start the Wayside Controller ---
    controller.run()

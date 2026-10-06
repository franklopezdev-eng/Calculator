#-------------------------------------------
# ISA
#  System Design:
#   - Four function calculator
#   - Can only operate on numbers stored in registers
#   - Processor receives binary data as 32-bit strings
#   - Returns results to the terminal
#   - Can operate on 10-bit numbers (0 thru 1023)
#   - Results can be negative (5 - 10 = -5)
#  Instruction format:
#   - 32 bit's in length
#   - Binary data will come to the CPU as a string
#   - Registers (32 total on CPU, 0-indexed)
#      - 0 thru 21:  Available for number storage
#        - 0: Constant 0
#      - 22 thru 31: Available for history storage
# +=======+=======+=======+=======+=======+=======+=======+=======+
# | 0: 0  | 1:    | 2:    | 3:    | 4:    | 5:    | 6:    | 7:    |
# +-------+-------+-------+-------+-------+-------+-------+-------+
# | 8:    | 9:    |10:    |11:    |12:    |13:    |14:    |15:    |
# +-------+-------+-------+-------+-------+-------+-------+-------+
# |16:    |17:    |18:    |19:    |20:    |21:    |22: H0 |23: H1 |
# +-------+-------+-------+-------+-------+-------+-------+-------+
# |24: H2 |25: H3 |26: H4 |27: H5 |28: H6 |29: H7 |30: H8 |31: H9 |
# +=======+=======+=======+=======+=======+=======+=======+=======+
#   - Bits 0-5 are OPCODEs
#     - use variable 'opcode' in program
#   - Bits 6-10 & 11-15 are source register locations
#     - use variables 'source_one' and 'source_two' in program
#   - Bits 16-25 are reserved for adding a new value to the registers
#     - use variable 'store' in program
#   - Bits 26-31 are functions
#     - use variable 'function_code' in program
# +--------+----------+-------------------------------------+
# | OPCODE | FUNCTION | Definition                          |
# | 000000 |  100000  | Add two numbers from registers      |
# | 000000 |  100010  | Subtract two numbers from registers |
# | 000000 |  011000  | Multiply two numbers from registers |
# | 000000 |  011010  | Divide two numbers from registers   |
# | 000001 |  000000  | Store value to next register        |
# | 100001 |  000000  | Return previous calculation         |
# +--------+----------+-------------------------------------+

class Calculator:
    def __init__(self, name):
        self.name = name
        self.number_registers = ["0000000000"] * 22
        self.history_registers = ["0000000000"] * 10
        self.number_index = "1"                         #Leaves Register 0 for 0 constant
        self.history_index = "10110"                    #Starts at Register 22
        self.temp_history_index = "10110"
        self.userdisplay = ""
        self.update_userdisplay(f"Hello, {name}")
    #Abstracted Methods
    def update_userdisplay(self, message):
        self.userdisplay = message
        print(f"{self.userdisplay}")
        return None

    def store_number(self, number):
        index = int(self.number_index, 2)
        self.number_registers[index] = number
        self.update_userdisplay(f"Stored the number \"{number}\" into register \"{self.number_index}\"")
        if(index >= 21):
            self.number_index == "1"
        else:
            self.number_index == bin(index + 1)[2:]     #[2:] omits the "0b" at the beginning of binary string
        return None

    def load_number(self, register_address):
        index = int(register_address, 2)
        number = self.number_registers[index]
        self.update_userdisplay(f"Loaded number \"{number}\" from register \"{bin(index)[2:]}\"")
        return number

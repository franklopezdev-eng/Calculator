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
            self.number_index = "1"
        else:
            self.number_index = bin(index + 1)[2:]     #[2:] omits the "0b" at the beginning of binary string
        return None

    #returns binary number
    def load_number(self, register_address):
        index = int(register_address, 2)
        number = self.number_registers[index]           
        self.update_userdisplay(f"Loaded number \"{number}\" from register \"{bin(index)[2:]}\"")
        return number

    def store_history(self, number):
        index = int(self.history_index, 2) - 22
        self.history_registers[index] = number
        self.update_userdisplay(f"Stored the number \"{number}\" into history register \"{self.history_index}\"")
        if(index >= 10):
            self.history_index = "10110"
        else:
            self.history_index = bin(index + 23)[2:] #[2:] omits the "0b" at the beginning of binary string
        self.temp_history_index = self.history_index
        return None

    # Main methods
    def ADD(self, addend1_address, addend2_address):
        addend1 = int(self.load_number(addend1_address), 2)
        addend2 = int(self.load_number(addend2_address), 2)
        sum = addend1 + addend2

        self.update_userdisplay(f"{addend1} + {addend2} = {sum}")
        self.store_history(bin(sum)[2:])
        return bin(sum)[2:]
    
    def SUB(self, minuend_address, subtrahend_address):
        minuend = int(self.load_number(minuend_address), 2)
        subtrahend = int(self.load_number(subtrahend_address), 2)
        difference = minuend - subtrahend

        self.update_userdisplay(f"{minuend} - {subtrahend} = {difference}")
        self.store_history(bin(difference)[2:])
        return bin(difference)[2:]

    def MULT(self, multiplicand_address, multiplier_address):
        multiplicand = int(self.load_number(multiplicand_address), 2)
        multiplier = int(self.load_number(multiplier_address), 2)
        product = multiplicand * multiplier

        self.update_userdisplay(f"{multiplicand} * {multiplier} = {product}")
        self.store_history(bin(product)[2:])
        return bin(product)[2:]

    def DIV(self, dividend_address, divisor_address):
        dividend = int(self.load_number(dividend_address), 2)
        divisor = int(self.load_number(divisor_address), 2)
        if (divisor == 0):
            self.update_userdisplay(f"ZeroDivisionError: Cannot divide {dividend} by 0.")
            return None
        else:
            quotient = int(dividend / divisor)
            self.update_userdisplay(f"{dividend} / {divisor} = {quotient}")
            self.store_history(bin(quotient)[2:])
            return bin(quotient)[2:]

    # Extra functionality
    # Returns previous answer in binary
    def ANS(self):
        return self.history_registers[int(self.history_index, 2) - 23]

    